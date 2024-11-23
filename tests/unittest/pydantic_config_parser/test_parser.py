import json

from pydantic import BaseModel

from pydantic_config_parser import json_loads_as_dict
from pydantic_config_parser import recursive_override_each_fields


class HelperClassElement(BaseModel):
    a: int = 1
    b: str = "test"
    c: list[int] = [1, 2, 3]
    d: dict[str, int] = {"a": 1, "b": 2}


class HelperClassRoot(BaseModel):
    a: int = 1
    b: str = "test"
    c: list[int] = [1, 2, 3]
    d: dict[str, int] = {"a": 1, "b": 2}
    e: HelperClassElement = HelperClassElement()


def test_recursive_override_each_fields_override_int():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"a": 2}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert (result.a, result.b, result.c, result.d, result.e) == (2, base_model.b, base_model.c, base_model.d, base_model.e)


def test_recursive_override_each_fields_override_str():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"b": "test2"}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert (result.a, result.b, result.c, result.d, result.e) == (base_model.a, "test2", base_model.c, base_model.d, base_model.e)


def test_recursive_override_each_fields_override_list():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"c": [4, 5, 6]}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert (result.a, result.b, result.c, result.d, result.e) == (base_model.a, base_model.b, [4, 5, 6], base_model.d, base_model.e)


def test_recursive_override_each_fields_override_dict():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"d": {"c": 3, "d": 4}}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert (result.a, result.b, result.c, result.d, result.e) == (base_model.a, base_model.b, base_model.c, {"c": 3, "d": 4}, base_model.e)


def test_recursive_override_each_fields_override_sub_model():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"e": {"a": 2}}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert (result.a, result.b, result.c, result.d, result.e) == (
        base_model.a,
        base_model.b,
        base_model.c,
        base_model.d,
        HelperClassElement(a=2, b=base_model.e.b, c=base_model.e.c, d=base_model.e.d),
    )
