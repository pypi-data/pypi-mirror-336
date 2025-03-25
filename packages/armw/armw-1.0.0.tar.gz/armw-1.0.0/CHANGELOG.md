# Change Log

## [v1.0.0] 2025-03-24

Breaking Changes
================
- `wait_for_service` returns a `canonicalize_name` for service.
- `package_and_msg_name(name)` replaces `/msg/` and `/srv/` with `/`.

New Features / Improvements
===========================
- Added a default argument `persistent=False` to `create_service_client()` callback.
- Added support for reading ros params from a dictionary.
- Added additional helper methods and `rosgraph` inspection tools.
  - `check_master()`: is the ros master online.
  - `get_topic_list()`: returns a list of topics.
  - `get_node_list()`: returns a list of node names.
  - `has_param(parameter_name)`: `bool` if param server has named param.
  - `get_param(parameter_name, default=None)`: returns param value.
  - `namespace(*args)`: returns own, namespace.
  - `is_private(name)`: `bool` for checking if topic, param or service is a private namespace.
  - `resolve_name(name)`: `bool` get full namespace path for topic, param or service.
  - `get_msg_fields(msg)`: returns list of fields in a `rosmsg`.
  - `get_msg_fields_and_types(msg)`: returns a dict of field names and field types.
  - `get_topic_type(topic)`: Returns `rosmsg` type for topic.
  - `get_msg_type_from_object(msg)`: returns ros type as `str`.
  - `get_package_path(package_name)`: returns path for a rospackage.
- Added additional shutdown logic to `base_node.py` 
- Added `rospack` package inspection.

Bugfixes
========
- Correctly initializing the parameter server by calling `parameter_callback([])` at the end of `start()` in `ros2_parameter_server.py`.
- Changed service callback groups from `MutuallyExclusiveCallbackGroup` to `ReentrantCallbackGroup` to avoid deadlocking issues.
- Added a `timeout_sec=1` default arg to service call timeout executor.
- Fixed bug where `get_param(parameter_name, default=None)` would crash when `parameter_name=""`. Now returns `default`

