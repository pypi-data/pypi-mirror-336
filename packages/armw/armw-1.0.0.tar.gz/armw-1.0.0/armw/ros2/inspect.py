"""
Various functions to explore the ROS world
"""

import armw.globals
from armw.ros2.util import canonicalize_name, ns_join
from ament_index_python.packages import get_package_share_directory


def check_master():
    return True


def get_topic_list():
    names_types = armw.globals.NODE.get_topic_names_and_types()
    return [x[0] for x in names_types]


def get_node_list():
    node_namespaces = armw.globals.NODE.get_node_names_and_namespaces()
    return [canonicalize_name(ns_join(x[1], x[0])) for x in node_namespaces]


def get_package_path(package_name: str):
    return get_package_share_directory(package_name)
