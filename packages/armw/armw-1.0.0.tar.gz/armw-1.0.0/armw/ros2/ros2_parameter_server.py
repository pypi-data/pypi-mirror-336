import inspect
from typing import List

import rclpy
from rcl_interfaces.msg import SetParametersResult

from armw.ros2.ros2_node import Ros2Node
from armw.doc_int_enum import DocIntEnum
from armw.base_parameter_server import BaseParameterServer


class Ros2ParameterServer(BaseParameterServer):
    def __init__(self, node_object: Ros2Node, namespace: str = ""):
        super().__init__(node_object, namespace)
        self.node = node_object

        self.parameter_values = {}

        self.callback = None

    def add_parameter(self, name, description, default_value, min_value=None, max_value=None, parameter_type=None):
        if inspect.isclass(parameter_type) and issubclass(parameter_type, DocIntEnum):
            # TODO: no idea yet
            pass

        if not self.node.has_parameter(name):
            self.node.declare_parameter(name, default_value)

        self.parameter_values[name] = self.node.get_parameter(name).value

    def start(self, callback):
        self.node.add_on_set_parameters_callback(self.parameter_callback)

        # Save what callback we need to run when a parameter is changed
        self.callback = callback

        # Run the callback with all the startup values so we ensure that they get set to whatever we just got from the parameter server
        self.parameter_callback([])

    def parameter_callback(self, params: List[rclpy.Parameter]):
        for param in params:
            self.parameter_values[param.name] = param.value

        if self.callback is not None:
            self.callback(self.parameter_values, {})
            return SetParametersResult(successful=True)
        else:
            return SetParametersResult(successful=False)
