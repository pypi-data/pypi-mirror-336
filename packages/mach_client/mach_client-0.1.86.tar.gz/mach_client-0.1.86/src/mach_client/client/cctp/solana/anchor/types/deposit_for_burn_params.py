from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class DepositForBurnParamsJSON(typing.TypedDict):
    amount: int
    destination_domain: int
    mint_recipient: str


@dataclass
class DepositForBurnParams:
    layout: typing.ClassVar = borsh.CStruct(
        "amount" / borsh.U64,
        "destination_domain" / borsh.U32,
        "mint_recipient" / BorshPubkey,
    )
    amount: int
    destination_domain: int
    mint_recipient: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "DepositForBurnParams":
        return cls(
            amount=obj.amount,
            destination_domain=obj.destination_domain,
            mint_recipient=obj.mint_recipient,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "amount": self.amount,
            "destination_domain": self.destination_domain,
            "mint_recipient": self.mint_recipient,
        }

    def to_json(self) -> DepositForBurnParamsJSON:
        return {
            "amount": self.amount,
            "destination_domain": self.destination_domain,
            "mint_recipient": str(self.mint_recipient),
        }

    @classmethod
    def from_json(cls, obj: DepositForBurnParamsJSON) -> "DepositForBurnParams":
        return cls(
            amount=obj["amount"],
            destination_domain=obj["destination_domain"],
            mint_recipient=Pubkey.from_string(obj["mint_recipient"]),
        )
