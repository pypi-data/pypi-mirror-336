from unittest.mock import ANY, Mock

import pytest
from confluent_kafka import KafkaError as ConfluentKafkaError
from confluent_kafka import KafkaException

from flowgate.services.kafka.avro.consumer import default_error_handler, get_message
from flowgate.services.kafka.avro.exceptions import (
    PartitionEndReached,
    KafkaBrokerTransportError,
)

from tests.services.kafka.avro.kafka import KafkaError, KafkaMessage


class TestAvroConsumer:
    def test_init(self, avro_consumer, confluent_avro_consumer):
        assert avro_consumer.topics == ["a"]
        confluent_avro_consumer.subscribe.assert_called_once_with(["a"])
        confluent_avro_consumer.assert_called_once()

    def test_consume_messages(self, avro_consumer):
        with pytest.raises(RuntimeError):
            with avro_consumer as consumer:
                for message in consumer:
                    assert message.value == b"foobar"

    def test_context_manager_close_consumer(self, mocker, avro_consumer):
        mock_consumer = mocker.spy(avro_consumer, "consumer")
        with avro_consumer:
            pass
        mock_consumer.close.assert_called_once()
        mock_consumer.reset_mock()

        with pytest.raises(ZeroDivisionError):
            with avro_consumer:
                1 / 0
        mock_consumer.close.assert_called_once()

    def test_context_manager_close_generator(self, mocker, avro_consumer):
        mock_generator = mocker.spy(avro_consumer, "_generator")
        with avro_consumer:
            pass
        mock_generator.close.assert_called_once()
        mock_generator.reset_mock()

        with pytest.raises(ZeroDivisionError):
            with avro_consumer:
                1 / 0
        mock_generator.close.assert_called_once()


class TestGetMessage:
    def setup_method(self, *args):
        self.message = KafkaMessage
        self.consumer = Mock()
        self.consumer.poll.return_value = self.message(_error=True)

    def test_retries_on_kafkatransporterror(self):
        error_handler = Mock(side_effect=KafkaBrokerTransportError)
        with pytest.raises(KafkaBrokerTransportError):
            get_message(self.consumer, error_handler)
        assert self.consumer.poll.call_count == 3

    def test_raises_endofpartition_when_stop_on_eof_is_true(self):
        error_handler = Mock(side_effect=PartitionEndReached)
        with pytest.raises(PartitionEndReached):
            get_message(self.consumer, error_handler, stop_on_eof=True)

    def test_returns_none_when_stop_on_eof_is_false(self):
        error_handler = Mock(side_effect=PartitionEndReached)
        message = get_message(self.consumer, error_handler)
        assert message is None


class TestErrorHandler:
    def test_raises_endofpartition_on_kafkaerror_partition_eof(self):
        error = KafkaError(_code=ConfluentKafkaError._PARTITION_EOF)
        with pytest.raises(PartitionEndReached):
            default_error_handler(error)

    @pytest.mark.parametrize(
        "code",
        [
            (ConfluentKafkaError._ALL_BROKERS_DOWN),
            (ConfluentKafkaError._NO_OFFSET),
            (ConfluentKafkaError._TIMED_OUT),
        ],
    )
    def test_raises_kafkaexception_on_other_errors(self, code):
        error = KafkaError(_code=code)
        with pytest.raises(KafkaException):
            default_error_handler(error)
