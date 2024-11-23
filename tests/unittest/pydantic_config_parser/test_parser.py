import datetime
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
    f: datetime.datetime = datetime.datetime.now(tz=datetime.UTC)
    g: bool = True
    h: float = 1.0
    i: str | None = "None"


def test_recursive_override_each_fields_override_int():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"a": 2}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert result == base_model.model_copy(update={"a": 2})


def test_recursive_override_each_fields_override_str():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"b": "test2"}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert result == base_model.model_copy(update={"b": "test2"})


def test_recursive_override_each_fields_override_list():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"c": [4, 5, 6]}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert result == base_model.model_copy(update={"c": [4, 5, 6]})


def test_recursive_override_each_fields_override_dict():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"d": {"c": 3, "d": 4}}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert result == base_model.model_copy(update={"d": {"c": 3, "d": 4}})


def test_recursive_override_each_fields_override_sub_model():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"e": {"a": 2}}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert result == base_model.model_copy(
        update={
            "e": HelperClassElement(a=2, b=base_model.e.b, c=base_model.e.c, d=base_model.e.d),
        }
    )


def test_recursive_override_each_fields_override_datetime():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"f": "2024-01-01T00:00:00Z"}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert result == base_model.model_copy(update={"f": datetime.datetime(2024, 1, 1, 0, 0, tzinfo=datetime.UTC)})


def test_recursive_override_each_fields_override_bool():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"g": False}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert result == base_model.model_copy(update={"g": False})


def test_recursive_override_each_fields_override_float():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"h": 2.0}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert result == base_model.model_copy(update={"h": 2.0})


def test_recursive_override_each_fields_override_none():
    base_model = HelperClassRoot()
    override_mapping = json_loads_as_dict(json.dumps({"i": None}))
    result = recursive_override_each_fields(base_model, override_mapping)
    assert result == base_model.model_copy(update={"i": None})
