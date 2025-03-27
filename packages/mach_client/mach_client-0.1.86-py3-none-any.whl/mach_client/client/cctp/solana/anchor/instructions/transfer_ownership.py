from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class TransferOwnershipArgs(typing.TypedDict):
    params: types.transfer_ownership_params.TransferOwnershipParams


layout = borsh.CStruct(
    "params" / types.transfer_ownership_params.TransferOwnershipParams.layout
)


class TransferOwnershipAccounts(typing.TypedDict):
    owner: Pubkey
    token_messenger: Pubkey
    event_authority: Pubkey
    program: Pubkey


def transfer_ownership(
    args: TransferOwnershipArgs,
    accounts: TransferOwnershipAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["owner"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["token_messenger"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"A\xb1\xd7I5-c/"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
