from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class AcceptOwnershipParamsJSON(typing.TypedDict):
    pass


@dataclass
class AcceptOwnershipParams:
    layout: typing.ClassVar = borsh.CStruct()

    @classmethod
    def from_decoded(cls, obj: Container) -> "AcceptOwnershipParams":
        return cls()

    def to_encodable(self) -> dict[str, typing.Any]:
        return {}

    def to_json(self) -> AcceptOwnershipParamsJSON:
        return {}

    @classmethod
    def from_json(cls, obj: AcceptOwnershipParamsJSON) -> "AcceptOwnershipParams":
        return cls()
