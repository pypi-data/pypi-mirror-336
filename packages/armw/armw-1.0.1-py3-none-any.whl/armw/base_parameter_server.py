"""
Base class to provide a reasonable API to set up runtime-reconfigurable parameters
"""

from armw.base_node import BaseNode


class BaseParameterServer(object):
    def __init__(self, node_object: BaseNode, namespace: str = ""):
        self.node = node_object
        self.namespace = namespace

    def add_parameter(self, name, description, default_value, min_value=None, max_value=None, parameter_type=None):
        raise NotImplementedError

    def start(self, callback):
        raise NotImplementedError



