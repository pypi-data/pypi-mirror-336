class KafkaError(Exception):
    pass


class PartitionEndReached(KafkaError):
    pass


class KafkaBrokerTransportError(Exception):
    pass


class KafkaTopicNotRegistered(Exception):
    pass


class SchemaNotFound(Exception):
    pass


class KafkaMessageDeliveryError(KafkaError):
    def __init__(self, error: str, message):
        self.error = error
        self.message = message
