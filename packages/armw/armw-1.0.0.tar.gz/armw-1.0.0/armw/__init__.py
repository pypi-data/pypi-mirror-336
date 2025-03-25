import armw.globals
import armw.base_node
import armw.base_parameter_server
import armw.doc_int_enum

# Figure out the middleware version

MIDDLEWARE = ""

try:
    import rospy

    MIDDLEWARE = "ros1"
except:
    pass

try:
    import rclpy

    MIDDLEWARE = "ros2"
except:
    pass

# Do some stuff with it
if MIDDLEWARE == "ros1":
    import armw.ros_common
    import armw.ros1.ros1_node
    from armw.ros1.ros1_parameter_server import Ros1ParameterServer
    import armw.ros1.interfaces
    import armw.ros1.inspect

    # function and class names
    ArmwNode = armw.ros1.ros1_node.Ros1Node
    ParameterServer = armw.ros1.ros1_parameter_server.Ros1ParameterServer
    Publisher = rospy.Publisher

    Time = rospy.Time
    Duration = rospy.Duration
    Rate = rospy.Rate
    AnyMsg = rospy.AnyMsg

    InterruptException = rospy.ROSInterruptException

    main = armw.ros1.ros1_node.main
    init_node = armw.ros1.ros1_node.init_node
    run_node = armw.ros1.ros1_node.run_node
    is_shutdown = rospy.is_shutdown
    sleep = rospy.sleep
    get_time = rospy.get_time
    import_message = armw.ros1.interfaces.import_message
    import_service_ = armw.ros1.interfaces.import_service_
    deserialze_anymsg = armw.ros1.interfaces.deserialze_anymsg
    get_msg_type_from_object = armw.ros1.interfaces.get_msg_type_from_object
    get_msg_fields = armw.ros1.interfaces.get_msg_fields
    get_msg_fields_and_types = armw.ros1.interfaces.get_msg_fields_and_types
    canonicalize_name = rospy.names.canonicalize_name
    resolve_name = rospy.names.resolve_name
    package_and_msg_name = armw.ros_common.package_and_msg_name
    get_package_path = armw.ros1.inspect.get_package_path

    check_master = armw.ros1.inspect.check_master
    get_topic_list = armw.ros1.inspect.get_topic_list
    get_node_list = armw.ros1.inspect.get_node_list

    # Log levels
    DEBUG = rospy.DEBUG
    INFO = rospy.INFO
    WARN = rospy.WARN
    ERROR = rospy.ERROR
elif MIDDLEWARE == "ros2":
    import rclpy.publisher

    import time
    import armw.ros_common
    import armw.ros2.ros2_node
    import armw.ros2.ros2_parameter_server
    import armw.ros2.interfaces
    import armw.ros2.time
    import armw.ros2.util
    import armw.ros2.inspect

    # function and class names
    ArmwNode = armw.ros2.ros2_node.Ros2Node
    ParameterServer = armw.ros2.ros2_parameter_server.Ros2ParameterServer
    Publisher = rclpy.publisher.Publisher

    Time = armw.ros2.time.Time
    Duration = armw.ros2.time.Duration
    Rate = armw.ros2.time.Rate
    AnyMsg = None

    InterruptException = Exception

    main = armw.ros2.ros2_node.main
    init_node = armw.ros2.ros2_node.init_node
    run_node = armw.ros2.ros2_node.run_node
    is_shutdown = lambda: not rclpy.ok()
    sleep = time.sleep
    get_time = armw.ros2.time.get_time
    import_message = armw.ros2.interfaces.import_message
    import_service_ = armw.ros2.interfaces.import_service_
    deserialze_anymsg = armw.ros2.interfaces.deserialze_anymsg
    get_msg_type_from_object = armw.ros2.interfaces.get_msg_type_from_object
    get_msg_fields = armw.ros2.interfaces.get_msg_fields
    get_msg_fields_and_types = armw.ros2.interfaces.get_msg_fields_and_types
    canonicalize_name = armw.ros2.util.canonicalize_name
    resolve_name = armw.ros2.util.resolve_name
    package_and_msg_name = armw.ros_common.package_and_msg_name
    get_package_path = armw.ros2.inspect.get_package_path

    check_master = armw.ros2.inspect.check_master
    get_topic_list = armw.ros2.inspect.get_topic_list
    get_node_list = armw.ros2.inspect.get_node_list

    # Log levels
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
else:
    print("No middleware available")
    # exit(1)

ParameterEnum = armw.doc_int_enum.DocIntEnum


def import_service(package_name: str, service_name: str):
    if service_name.endswith("Request"):
        service_name = service_name[:-7]
        _, _, req = armw.import_service_(package_name, service_name)
        return req
    elif service_name.endswith("Response"):
        service_name = service_name[:-8]
        _, resp, _ = armw.import_service_(package_name, service_name)
        return resp
    else:
        return armw.import_service_(package_name, service_name)


def import_message_from_name(name):
    pkg, msg = armw.package_and_msg_name(name)
    return armw.import_message(pkg, msg)


def NODE() -> armw.base_node.BaseNode:
    return armw.globals.NODE


def fill_time(dest_object, source_object) -> armw.Time:
    """
    Attempts to get around some time weirdness by doing lots of python weirdness
    """

    seconds_fields = ["sec", "secs", "seconds"]
    nanoseconds_fields = ["nsec", "nsecs", "nanosec", "nanosecs", "nanoseconds"]

    seconds = None
    nanoseconds = None

    for field in seconds_fields:
        if hasattr(source_object, field):
            seconds = getattr(source_object, field)
            break

    for field in nanoseconds_fields:
        if hasattr(source_object, field):
            nanoseconds = getattr(source_object, field)
            break

    if seconds is None:
        raise Exception(f"Source {source_object} does not have field encoding seconds")
    if nanoseconds is None:
        raise Exception(f"Source {source_object} does not have field encoding nanoseconds")

    wrote_seconds = False
    wrote_nanoseconds = False

    for field in seconds_fields:
        if hasattr(dest_object, field):
            setattr(dest_object, field, seconds)
            wrote_seconds = True
            break

    for field in nanoseconds_fields:
        if hasattr(dest_object, field):
            setattr(dest_object, field, nanoseconds)
            wrote_nanoseconds = True
            break

    if not wrote_seconds:
        raise Exception(f"Destination {dest_object} does not have field encoding seconds")
    if not wrote_nanoseconds:
        raise Exception(f"Destination {source_object} does not have field encoding nanoseconds")

    return dest_object


def get_time_object(time_object):
    if "duration" in str(type(time_object)).lower():
        return fill_time(armw.Duration(), time_object)
    else:
        return fill_time(armw.Time(), time_object)
