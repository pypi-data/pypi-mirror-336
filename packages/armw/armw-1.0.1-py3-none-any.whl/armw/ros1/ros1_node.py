"""
ROS1 version
"""

import rospy
import rostopic

import armw.globals
from armw.base_node import BaseNode


class Ros1Node(BaseNode):
    def __init__(self):
        super().__init__()

    def spin(self):
        # Issue status periodically.
        rate = armw.Rate(self.update_rate)
        while not armw.is_shutdown() and not self.stop_commanded:
            self.loop_once()

            try:
                rate.sleep()
            except rospy.ROSInterruptException:
                self.log_warn(f"{armw.globals.NODE_NAME} Shutting down")

        self.shutdown()

    def log(self, level: int, message: str):
        if level == -1:
            rospy.logdebug(message)
        elif level == 0:
            rospy.loginfo(message)
        elif level == 1:
            rospy.logwarn(message)
        elif level == 2:
            rospy.logerr(message)
        elif level == 3:
            rospy.logfatal(message)

    def log_throttle(self, interval: int, level: int, message: str):
        if level == -1:
            rospy.logdebug_throttle(interval, message)
        elif level == 0:
            rospy.loginfo_throttle(interval, message)
        elif level == 1:
            rospy.logwarn_throttle(interval, message)
        elif level == 2:
            rospy.logerr_throttle(interval, message)

    def get_name(self):
        return rospy.get_name()

    def get_namespace(self):
        return rospy.get_namespace()

    def search_param(self, parameter_name):
        return rospy.search_param(parameter_name)

    def has_param(self, parameter_name):
        return rospy.has_param(parameter_name)

    def get_param(self, parameter_name, default=None):
        """
        Returns the value for a given parameter name, or None if it can't find it
        """
        return rospy.get_param(parameter_name, default)

    def set_param(self, parameter_name, value):
        rospy.set_param(parameter_name, value)

    def delete_param(self, parameter_name):
        rospy.delete_param(parameter_name)

    def get_topic_type(self, topic):
        topic_type, _, _ = rostopic.get_topic_class(topic)
        return topic_type

    def publish(self, topic: str, message_type, queue_size=1, latch=False):
        return rospy.Publisher(topic, message_type, queue_size=queue_size, latch=latch)

    def subscribe(self, topic: str, message_type, callback, queue_size=1):
        if message_type is None:
            from rospy import AnyMsg
            message_type = AnyMsg

        return rospy.Subscriber(topic, message_type, callback)

    def create_service_server(self, name, service_type, callback):
        return rospy.Service(name, service_type, callback)

    def create_service_client(self, name: str, service_type, persistent=False):
        return rospy.ServiceProxy(name, service_type, persistent=persistent)

    def wait_for_message(self, topic, message_type, timeout=None):
        if message_type is None:
            from rospy import AnyMsg
            message_type = AnyMsg

        if timeout is None:
            return rospy.wait_for_message(topic, message_type)
        else:
            return rospy.wait_for_message(topic, message_type, timeout=timeout)

    def wait_for_service(self, name, timeout=None):
        if timeout is None:
            rospy.wait_for_service(name)
        else:
            return rospy.wait_for_service(name, timeout=timeout)


def init_node(node_name):
    rospy.init_node(node_name)


def run_node(node_object):
    armw.globals.NODE = node_object
    try:
        armw.globals.NODE.spin()
        rospy.loginfo(f"{armw.globals.NODE_NAME} shutdown")
    except rospy.ROSInterruptException:
        rospy.loginfo(f"{armw.globals.NODE_NAME} shutdown (interrupt)")


def main(node_class: type(BaseNode), node_name: str):
    rospy.init_node(node_name)

    armw.globals.NODE_NAME = node_name
    armw.globals.NODE = node_class()

    try:
        armw.globals.NODE.spin()
        rospy.loginfo(f"{node_name} shutdown")
    except rospy.ROSInterruptException:
        rospy.loginfo(f"{node_name} shutdown (interrupt)")
