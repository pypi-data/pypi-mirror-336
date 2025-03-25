def package_and_msg_name(name):
    """
    https://docs.ros.org/en/diamondback/api/roslib/html/python/roslib.names-pysrc.html#package_resource_name
    """
    name.replace('/msg/', '/')
    name.replace('/srv/', '/')
    if "/" in name:
        val = tuple(name.split("/"))
        if len(val) != 2:
            raise ValueError("invalid name [%s]" % name)
        else:
            return val
    else:
        return '', name