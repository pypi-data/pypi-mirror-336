from __future__ import annotations

import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Literal


@dataclass
class TypeWithDep:
    type: str
    dep: str | None = None

    def get_python_type(self) -> type:
        """Get the Python type from the type string for typing annotation in Python."""
        if self.type == "str":
            return str
        elif self.type == "int":
            return int
        elif self.type == "float":
            return float
        elif self.type == "bool":
            return bool
        elif self.type == "bytes":
            return bytes
        elif self.type == "dict":
            return dict
        elif self.type == "datetime":
            return datetime.datetime
        else:
            raise ValueError(f"Unknown type: {self.type}")


@dataclass
class DataType:
    type: Literal["str", "int", "datetime", "float", "bool", "bytes", "dict"]
    is_list: bool = False
    parent: DataType | None = None

    def get_python_type(self) -> TypeWithDep:
        if self.type in ["str", "int", "float", "bool", "bytes", "dict"]:
            return TypeWithDep(type=self.type)
        if self.type == "datetime":
            return TypeWithDep(type="datetime", dep="datetime.datetime")
        raise NotImplementedError(self.type)

    def get_sqlalchemy_type(self) -> TypeWithDep:
        if self.type in ["str", "int", "float", "bool", "bytes"]:
            return TypeWithDep(type=self.type)
        if self.type == "dict":
            return TypeWithDep(type="JSON")
        if self.type == "datetime":
            return TypeWithDep(type="datetime", dep="datetime.datetime")
        raise NotImplementedError(self.type)
