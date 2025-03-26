import armw

SEP = '/'


def namespace(*args):
    return armw.NODE().get_namespace()


def ns_join(part_1, part_2):
    return f"{part_1}{SEP}{part_2}"


def is_private(name):
    return name.startswith("~")


def canonicalize_name(name):
    """
    Put name in canonical form. Double slashes '//' are removed and
    name is returned without any trailing slash, e.g. /foo/bar
    @param name: ROS name
    @type  name: str
    """

    # Straight up copied from here: https://docs.ros.org/en/melodic/api/rospy/html/rospy.names-pysrc.html

    if not name or name == SEP:
        return name
    elif name[0] == SEP:
        return '/' + '/'.join([x for x in name.split(SEP) if x])
    else:
        return '/'.join([x for x in name.split(SEP) if x])


def resolve_name(name):
    if not name:  # empty string resolves to namespace
        return namespace()

    name = str(name)  # enforce string conversion else struct.pack might raise UnicodeDecodeError (see #3998)

    name = canonicalize_name(name)

    if name[0] == SEP:  # global name
        resolved_name = name
    elif is_private(name):  # ~name
        resolved_name = ns_join(namespace(), name[1:])
    else:  # relative
        resolved_name = ns_join(namespace(), name)

    # Just in case, because I'm pretty sure we might add double slashes by accident
    return canonicalize_name(resolved_name)
