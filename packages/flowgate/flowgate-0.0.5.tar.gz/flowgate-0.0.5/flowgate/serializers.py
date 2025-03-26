from flowgate.services.kafka.avro.message import Message as ConfluentKafkaMessage

from flowgate.message import Message, message_factory

try:
    from cnamedtuple import namedtuple
except ImportError:
    from collections import namedtuple


def from_message_to_dto(message: ConfluentKafkaMessage, is_new=True) -> Message:
    data, class_name = message.value["data"], message.value["class"]
    data["Meta"] = message._meta

    message_cls = namedtuple(class_name, data.keys())
    dto = message_factory(message_cls, is_new=is_new)(**data)

    return dto


def to_message_from_dto(dto: Message) -> dict:
    message = {"class": dto._class, "data": dto.to_dict()}

    return message
