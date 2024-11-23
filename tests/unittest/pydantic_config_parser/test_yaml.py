from pydantic_config_parser import yaml_loads_as_json


def test_yaml_loads_as_json_str():
    yaml_s = """
    a: 1
    """
    assert yaml_loads_as_json(yaml_s) == {"a": 1}


def test_yaml_loads_as_json_int():
    yaml_s = """
    a: 1
    """
    assert yaml_loads_as_json(yaml_s) == {"a": 1}


def test_yaml_loads_as_json_bool():
    yaml_s = """
    a: true
    """
    assert yaml_loads_as_json(yaml_s) == {"a": True}


def test_yaml_loads_as_json_float():
    yaml_s = """
    a: 1.0
    """
    assert yaml_loads_as_json(yaml_s) == {"a": 1.0}


def test_yaml_loads_as_json_none():
    yaml_s = """
    a: null
    """
    assert yaml_loads_as_json(yaml_s) == {"a": None}


def test_yaml_loads_as_json_list():
    yaml_s = """
    a: [1, 2, 3]
    """
    assert yaml_loads_as_json(yaml_s) == {"a": [1, 2, 3]}


def test_yaml_loads_as_json_dict():
    yaml_s = """
    a: {"b": 1, "c": 2}
    """
    assert yaml_loads_as_json(yaml_s) == {"a": {"b": 1, "c": 2}}


def test_yaml_loads_as_json_nested():
    yaml_s = """
    a: {"b": {"c": 1, "d": 2}, "e": 3}
    """
    assert yaml_loads_as_json(yaml_s) == {"a": {"b": {"c": 1, "d": 2}, "e": 3}}


def test_yaml_loads_as_json_datetime():
    """Not parse to datetime.datetime, just return string."""
    yaml_s = """
    a: 2024-01-01T00:00:00Z
    """
    assert yaml_loads_as_json(yaml_s) == {"a": "2024-01-01T00:00:00Z"}
