from __future__ import annotations
import dataclasses
import typing
from typing import Optional

from tronpy import AsyncContract, Tron
from tronpy.async_contract import AsyncContractMethod

from .. import config
from ..account import TronAccount, TronAccountID
from ..chain import TronChain
from ..chain_client import TronClient
from ..utility import tron
from ..transaction import TronSentTransaction, TronTransaction
from .token import ApprovableToken, NativeCoin


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class TronNativeCoin[Chain: TronChain](NativeCoin[Chain]):
    client: TronClient[Chain]

    @property
    @typing.override
    def chain(self) -> Chain:
        return self.client.chain

    @typing.override
    async def get_balance(self, account_id: TronAccountID[Chain]) -> int:
        return int(
            await self.client.native.get_account_balance(account_id.address) * 1_000_000
        )

    @typing.override
    async def transfer(
        self,
        sender: TronAccount[Chain],
        recipient: TronAccountID[Chain],
        amount: int,
    ) -> tuple[TronSentTransaction[Chain], dict]:
        builder = self.client.native.trx.transfer(
            sender.address, recipient.address, amount
        )

        transaction = await TronTransaction.from_builder(
            self.client, builder, sender, 0
        )

        sent_transaction = await transaction.broadcast()
        return await sent_transaction.wait_for_receipt()


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class TronToken[Chain: TronChain](ApprovableToken[Chain]):
    client: TronClient
    contract: AsyncContract

    @classmethod
    async def from_data(
        cls,
        client: TronClient[Chain],
        address: str,
        symbol: Optional[str],
        decimals: Optional[int],
    ) -> TronToken[Chain]:
        contract = await client.native.get_contract(address)
        assert contract.address
        contract.abi = config.trc20_abi

        if not symbol:
            symbol = typing.cast(str, await contract.functions.symbol())

        if not decimals:
            decimals = typing.cast(int, await contract.functions.decimals())

        return cls(client=client, contract=contract, symbol=symbol, decimals=decimals)

    @property
    @typing.override
    def chain(self) -> Chain:
        return self.client.chain

    @property
    @typing.override
    def asset_namespace(self) -> str:
        return "trc20"

    @property
    @typing.override
    def address(self) -> str:
        return self.contract.address  # type: ignore

    @typing.override
    def encode_address(self) -> bytes:
        return tron.encode_address(self.address)

    @typing.override
    async def get_balance(self, account_id: TronAccountID[Chain]) -> int:
        return await self.contract.functions.balanceOf(account_id.address)

    async def create_transfer_transaction(
        self,
        sender: TronAccount[Chain],
        recipient: TronAccountID[Chain],
        amount: int,
    ) -> TronTransaction[Chain]:
        return await TronTransaction.from_contract_method(
            self.client,
            sender,
            typing.cast(AsyncContractMethod, self.contract.functions.transfer),
            recipient.address,
            amount,
        )

    @typing.override
    async def transfer(
        self,
        sender: TronAccount[Chain],
        recipient: TronAccountID[Chain],
        amount: int,
    ) -> tuple[TronSentTransaction[Chain], dict]:
        transaction = await self.create_transfer_transaction(sender, recipient, amount)
        sent_transaction = await transaction.broadcast()
        return sent_transaction, await sent_transaction.wait_for_receipt()

    @typing.override
    async def get_allowance(
        self, owner: TronAccountID[Chain], spender: TronAccountID[Chain]
    ) -> int:
        return await self.contract.functions.allowance(owner.address, spender.address)

    async def create_approval_transaction(
        self,
        owner: TronAccount[Chain],
        spender: TronAccountID[Chain],
        amount: int,
    ) -> TronTransaction[Chain]:
        return await TronTransaction.from_contract_method(
            self.client,
            owner,
            typing.cast(AsyncContractMethod, self.contract.functions.approve),
            spender.address,
            amount,
        )

    @typing.override
    async def approve(
        self,
        owner: TronAccount[Chain],
        spender: TronAccountID[Chain],
        amount: int,
    ) -> dict:
        transaction = await self.create_approval_transaction(owner, spender, amount)
        sent_transaction = await transaction.broadcast()
        return await sent_transaction.wait_for_receipt()
