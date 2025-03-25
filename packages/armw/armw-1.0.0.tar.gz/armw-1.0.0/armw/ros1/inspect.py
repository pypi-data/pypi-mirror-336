"""
Various functions to explore the ROS world
"""

import rosgraph
import rostopic
import rosnode
import rospkg


def check_master():
    return rosgraph.is_master_online()


def get_topic_list():
    master = rosgraph.Master('/rostopic')
    pubs, _ = rostopic.get_topic_list(master=master)
    return [x[0] for x in pubs]


def get_node_list():
    return rosnode.get_node_names()


def get_package_path(package_name: str):
    return rospkg.RosPack().get_path(package_name)
