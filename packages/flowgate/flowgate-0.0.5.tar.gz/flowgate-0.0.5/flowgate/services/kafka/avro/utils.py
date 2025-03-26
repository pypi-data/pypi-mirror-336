from collections import defaultdict
from functools import wraps
import zlib

import structlog
from confluent_kafka import KafkaError, KafkaException

from flowgate.services.kafka.avro.exceptions import (
    PartitionEndReached,
    KafkaBrokerTransportError,
)

logger = structlog.get_logger(__name__)


def retry_exception(exceptions, retries=3):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            retry_count = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if any([isinstance(exc, e) for e in exceptions]):
                        logger.warning("Retrying exception", exc=exc, retry=retry_count)
                        retry_count += 1
                        if retry_count < retries:
                            continue
                    raise

        return wrapped

    return decorator


def default_partitioner(key, num_partitions):
    return zlib.crc32(key) % num_partitions


def default_key_filter(key, message_key):
    return key == message_key


def find_duplicated_messages(messages, logger=logger):
    duplicates = defaultdict(list)
    for i, message in enumerate(messages):
        duplicates[message].append(i)

    for message, pos in sorted(duplicates.items()):
        if len(pos) > 1:
            logger.critical("Duplicated messages found", message=message, pos=pos)


def default_error_handler(kafka_error):
    code = kafka_error.code()
    if code == KafkaError._PARTITION_EOF:
        logger.debug("Reached end of partition")
        raise PartitionEndReached
    elif code == KafkaError._TRANSPORT:
        raise KafkaBrokerTransportError(kafka_error)
    else:
        raise KafkaException(kafka_error)
