"""
Functions to handle importing interface definitions
"""

import importlib
from collections import OrderedDict
from typing import List, Dict

import roslib.message


def import_message(package_name: str, message_name: str):
    return getattr(importlib.import_module(f"{package_name}.msg"), message_name)


def import_service_(package_name: str, service_name: str):
    service_class = getattr(importlib.import_module(f"{package_name}.srv"), service_name)
    service_request = getattr(importlib.import_module(f"{package_name}.srv"), f"{service_name}Request")
    service_response = getattr(importlib.import_module(f"{package_name}.srv"), f"{service_name}Response")

    return service_class, service_response, service_request


def deserialze_anymsg(msg_data):
    topic_type = msg_data._connection_header['type']
    topic_class = roslib.message.get_message_class(topic_type)
    msg = topic_class()
    msg.deserialize(msg_data._buff)
    return msg


def get_msg_type_from_object(msg) -> str:
    return msg._type


def get_msg_fields_and_types(msg) -> Dict[str, str]:
    slot_names = msg.__slots__
    slot_types = msg._slot_types

    return OrderedDict(zip(slot_names, slot_types))


def get_msg_fields(msg) -> List[str]:
    return msg.__slots__
