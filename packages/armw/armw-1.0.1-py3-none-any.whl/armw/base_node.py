"""
Base node class that contains all the interfaces needed for the abstract middleware
"""

import inspect

import armw.globals


class BaseNode(object):
    def __init__(self):
        # Set the global node object before we run the rest of the constructor
        armw.globals.NODE = self

        self.update_rate = 1
        self.stop_commanded = False

    def spin(self):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def loop_once(self):
        pass

    def stop_running(self):
        self.stop_commanded = True

    def shutdown(self):
        pass

    def log(self, level, message):
        """
        Abstract function to log to console
        :param level: 0 for info, 1 for warn, 2 for error
        :param message: String to log
        :return: None
        """
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def log_debug(self, message, *args):
        self.log(-1, message % args)

    def log_info(self, message, *args):
        self.log(0, message % args)

    def log_warn(self, message, *args):
        self.log(1, message % args)

    def log_error(self, message, *args):
        self.log(2, message % args)

    def log_fatal(self, message, *args):
        self.log(3, message % args)

    def log_throttle(self, interval: int, level: int, message: str):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def log_debug_throttle(self, interval, message, *args):
        self.log_throttle(interval, -1, message % args)

    def log_info_throttle(self, interval, message, *args):
        self.log_throttle(interval, 0, message % args)

    def log_warn_throttle(self, interval, message, *args):
        self.log_throttle(interval, 1, message % args)

    def log_error_throttle(self, interval, message, *args):
        self.log_throttle(interval, 2, message % args)

    def get_name(self):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def get_namespace(self):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def search_param(self, parameter_name):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def has_param(self, parameter_name):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def get_param(self, parameter_name, default=None):
        """
        Returns the value for a given parameter name, or None if it can't find it
        """
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def set_param(self, parameter_name, value):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def delete_param(self, parameter_name):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def get_topic_type(self, topic):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def publish(self, topic: str, message_type, queue_size=1, latch=False):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def subscribe(self, topic: str, message_type, callback, queue_size=1):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def create_service_server(self, name: str, service_type, callback):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def create_service_client(self, name: str, service_type, persistent=False):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def wait_for_message(self, topic, message_type, timeout=None):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")

    def wait_for_service(self, name, timeout=None):
        raise NotImplementedError(f"armw.BaseNode.{inspect.stack()[0][3]}() not implemented")
