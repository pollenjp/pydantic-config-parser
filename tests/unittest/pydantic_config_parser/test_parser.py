import datetime
import typing as t
from dataclasses import dataclass

import pytest
from pydantic import BaseModel

from pydantic_config_parser import JsonValueType
from pydantic_config_parser import recursive_override_each_fields


class HelperClassE(BaseModel):
    a: int = 1
    b: str = "test"
    c: list[int] = [1, 2, 3]
    d: dict[str, int] = {"a": 1, "b": 2}


class HelperClassRoot(BaseModel):
    a: int = 1
    b: str = "test"
    c: list[int] = [1, 2, 3]
    d: dict[str, int] = {"a": 1, "b": 2}
    e: HelperClassE = HelperClassE()
    f: datetime.datetime = datetime.datetime.now(tz=datetime.UTC)
    g: bool = True
    h: float = 1.0
    i: str | None = "None"


@dataclass
class Param:
    override_mapping: dict[str, JsonValueType]
    expected_value: t.Any


@pytest.mark.parametrize(
    "params",
    [
        Param(override_mapping={"a": 2}, expected_value={"a": 2}),
        Param(override_mapping={"b": "test2"}, expected_value={"b": "test2"}),
        Param(override_mapping={"c": [4, 5, 6]}, expected_value={"c": [4, 5, 6]}),
        Param(override_mapping={"d": {"c": 3, "d": 4}}, expected_value={"d": {"c": 3, "d": 4}}),
        Param(
            override_mapping={"e": {"a": 2}},
            expected_value={"e": HelperClassE().model_copy(update={"a": 2})},
        ),
        Param(
            override_mapping={"f": "2024-01-01T00:00:00Z"},
            expected_value={"f": datetime.datetime(2024, 1, 1, 0, 0, tzinfo=datetime.UTC)},
        ),
        Param(override_mapping={"g": False}, expected_value={"g": False}),
        Param(override_mapping={"h": 2.0}, expected_value={"h": 2.0}),
        Param(override_mapping={"i": None}, expected_value={"i": None}),
    ],
)
def test_recursive_override_each_fields(params: Param) -> None:
    base_model = HelperClassRoot()
    result = recursive_override_each_fields(base_model, params.override_mapping)
    assert result == base_model.model_copy(update=params.expected_value)
