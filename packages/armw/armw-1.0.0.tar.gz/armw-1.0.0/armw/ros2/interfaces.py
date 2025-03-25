"""
Functions to handle importing interface definitions
"""

import importlib
from typing import List, Dict


def import_message(package_name: str, message_name: str):
    if package_name == "std_msgs" and message_name == "Time":
        # ROS changing the name of this causes SO MANY problems
        package_name = "builtin_interfaces"
        message_name = "Time"
    elif package_name == "rosgraph_msgs" and message_name == "Log":
        package_name = "rcl_interfaces"
        message_name = "Log"

    return getattr(importlib.import_module(f"{package_name}.msg"), message_name)


def import_service_(package_name: str, service_name: str):
    service_class = getattr(importlib.import_module(f"{package_name}.srv"), service_name)
    return service_class, service_class.Response, service_class.Request


def deserialze_anymsg(msg_data):
    return msg_data


def get_msg_type_from_object(msg):
    string = str(type(msg))
    useful_bit = string.split("'")[1]
    pkg = useful_bit.split(".")[0]
    msg_name = useful_bit.split(".")[-1].split("_")[-1]
    return f"{pkg}/{msg_name}"


def get_msg_fields_and_types(msg) -> Dict[str, str]:
    return msg.get_fields_and_field_types()


def get_msg_fields(msg) -> List[str]:
    return list(get_msg_fields_and_types(msg).keys())


if __name__ == '__main__':
    print(get_msg_type_from_object(None))
