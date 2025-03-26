import socket
import uuid

KAFKA_PRODUCER_DEFAULT_CONFIG = {
    "client.id": socket.gethostname(),
    "log.connection.close": False,
    "enable.idempotence": True,
    "max.in.flight": 1,
    "linger.ms": 1000,
}
AVRO_LOADER_DEFAULT_CONFIG = {
    "log.connection.close": False,
    "log.thread.name": False,
    "default.topic.config": {"auto.offset.reset": "earliest"},
    "fetch.wait.max.ms": 10,
    "fetch.min.bytes": 1000,
    "offset.store.method": "none",
    "enable.auto.commit": False,
    "fetch.error.backoff.ms": 0,
    "group.id": str(uuid.uuid4()),
    "client.id": socket.gethostname(),
    "enable.partition.eof": True,
}
