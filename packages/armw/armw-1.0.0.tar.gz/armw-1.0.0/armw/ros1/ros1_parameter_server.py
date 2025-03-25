import inspect

try:
    from ddynamic_reconfigure_python.ddynamic_reconfigure import DDynamicReconfigure
except Exception as e:
    print(e)

from armw.base_node import BaseNode
from armw.doc_int_enum import DocIntEnum
from armw.base_parameter_server import BaseParameterServer


class Ros1ParameterServer(BaseParameterServer):
    def __init__(self, node_object: BaseNode, namespace: str = ""):
        super().__init__(node_object, namespace)

        self.server = DDynamicReconfigure(namespace)

    def add_parameter(self, name, description, default_value, min_value=None, max_value=None, parameter_type=None):
        edit_method = ""
        if inspect.isclass(parameter_type) and issubclass(parameter_type, DocIntEnum):
            option_list = []
            for value in parameter_type:
                option_list.append(self.server.const(parameter_type.get_field_name(value), "int", int(value), parameter_type.get_description(value)))
            edit_method = self.server.enum(option_list, parameter_type.__name__)

        self.server.add_variable(name, description, default=default_value, min=min_value, max=max_value, edit_method=edit_method)

    def start(self, callback):
        self.server.start(callback)
