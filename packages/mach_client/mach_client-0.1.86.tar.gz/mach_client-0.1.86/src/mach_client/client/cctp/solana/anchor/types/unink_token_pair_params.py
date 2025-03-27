from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class UninkTokenPairParamsJSON(typing.TypedDict):
    pass


@dataclass
class UninkTokenPairParams:
    layout: typing.ClassVar = borsh.CStruct()

    @classmethod
    def from_decoded(cls, obj: Container) -> "UninkTokenPairParams":
        return cls()

    def to_encodable(self) -> dict[str, typing.Any]:
        return {}

    def to_json(self) -> UninkTokenPairParamsJSON:
        return {}

    @classmethod
    def from_json(cls, obj: UninkTokenPairParamsJSON) -> "UninkTokenPairParams":
        return cls()
