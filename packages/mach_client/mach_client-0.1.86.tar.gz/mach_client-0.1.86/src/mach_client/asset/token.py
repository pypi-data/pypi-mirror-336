from __future__ import annotations
import abc
import dataclasses
from decimal import Decimal
from collections import defaultdict
import typing
from typing import Any, ClassVar, Optional

from ..chain import Chain
from ..chain_client import ChainClient, EthereumClient, SolanaClient, TronClient
from ..account import Account, AccountID
from ..transaction import SentTransaction
from .asset import Asset


NATIVE_COIN_ADDRESS = "native"


# Fungible token
# Caches some frequently accessed metadata
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Token[ChainType: Chain](Asset[ChainType]):
    lookup_cache: ClassVar[defaultdict[Chain, dict[str, Token]]] = defaultdict(dict)

    symbol: str
    decimals: int

    # The client calls this while initializing the configuration, which caches the tokens so that you can look them up by name
    @classmethod
    async def register(
        cls,
        client: ChainClient[ChainType],
        address: str,
        symbol: Optional[str],
        decimals: Optional[int],
    ) -> Token[ChainType]:
        if token := cls.lookup_cache[client.chain].get(address):
            return token

        elif address == NATIVE_COIN_ADDRESS:
            assert (
                symbol and decimals
            ), "Both symbol and decimals must be provided for the native coin"

            match client:
                case EthereumClient():
                    coin_class = ethereum.EthereumNativeCoin
                case SolanaClient():
                    coin_class = solana.SolanaNativeCoin
                case TronClient():
                    coin_class = tron.TronNativeCoin
                case _:
                    raise NotImplementedError(f"Unimplemented chain: {client.chain}")

            token = coin_class(
                client=client,  # type: ignore
                symbol=symbol,
                decimals=decimals,
            )

        else:
            match client:
                case EthereumClient():
                    token = await ethereum.EthereumToken.from_data(
                        client, address, symbol, decimals
                    )
                case SolanaClient():
                    token = await solana.SolanaToken.from_data(
                        client, address, symbol, decimals
                    )
                case TronClient():
                    token = await tron.TronToken.from_data(
                        client, address, symbol, decimals
                    )
                case _:
                    raise NotImplementedError(f"Unimplemented chain: {client.chain}")

        cls.lookup_cache[token.chain].update(
            ((token.symbol, token), (token.address, token))
        )

        return token

    @classmethod
    def try_lookup(cls, chain: ChainType, key: str) -> Optional[Token[ChainType]]:
        return cls.lookup_cache[chain].get(key)

    @classmethod
    def lookup(cls, chain: ChainType, key: str) -> Token[ChainType]:
        return cls.lookup_cache[chain][key]

    @classmethod
    def lookup_symbol(cls, chain: ChainType, symbol: str) -> Token[ChainType]:
        return cls.lookup(chain, symbol)

    @classmethod
    def try_lookup_symbol(
        cls, chain: ChainType, symbol: str
    ) -> Optional[Token[ChainType]]:
        return cls.try_lookup(chain, symbol)

    @classmethod
    def lookup_address(cls, chain: ChainType, address: str) -> Token[ChainType]:
        return cls.lookup(chain, address)

    @classmethod
    def try_lookup_address(
        cls, chain: ChainType, address: str
    ) -> Optional[Token[ChainType]]:
        return cls.lookup_cache[chain].get(address)

    @classmethod
    def from_str(cls, string: str) -> Token[ChainType]:
        chain, symbol = string.split("-")
        return cls.lookup_symbol(Chain.from_str(chain), symbol)  # type: ignore

    @classmethod
    def from_id_str(cls, id: str) -> Token[ChainType]:
        chain_id, rest = id.split("/")
        chain = Chain.from_id_str(chain_id)
        _asset_namespace, address = rest.split(":")
        return cls.lookup_address(chain, address)  # type: ignore

    @property
    @typing.override
    def asset_reference(self) -> str:
        return self.address

    @property
    @abc.abstractmethod
    def address(self) -> str:
        pass

    @abc.abstractmethod
    def encode_address(self) -> bytes:
        pass

    @abc.abstractmethod
    async def get_balance(self, account_id: AccountID[ChainType]) -> int:
        pass

    async def get_balance_in_coins(self, account_id: AccountID[ChainType]) -> Decimal:
        return Decimal(await self.get_balance(account_id)) / 10**self.decimals

    def to_coins(self, amount: int) -> Decimal:
        return Decimal(amount) / 10**self.decimals

    def format_amount(self, amount: int) -> str:
        return f"{self.to_coins(amount)} {self}"

    @abc.abstractmethod
    async def transfer(
        self,
        sender: Account[ChainType],
        recipient: AccountID[ChainType],
        amount: int,
    ) -> tuple[SentTransaction[ChainType], Any]:
        pass

    async def transfer_checked(
        self,
        sender: Account[ChainType],
        recipient: AccountID[ChainType],
        amount: int,
    ) -> tuple[SentTransaction[ChainType], Any]:
        assert (
            await self.get_balance(sender.downcast()) >= amount
        ), "Insufficient balance"
        return await self.transfer(sender, recipient, amount)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    def __str__(self) -> str:
        return f"{self.chain}-{self.symbol}"

    def is_native(self) -> bool:
        return self.address == NATIVE_COIN_ADDRESS

    def is_stablecoin(self) -> bool:
        return self.symbol in ("FRAX", "DAI", "MIM") or any(
            map(
                lambda symbol: symbol in self.symbol,
                ("USD", "EUR", "JPY", "GPB", "CHF"),
            )
        )

    def is_chf_stablecoin(self) -> bool:
        return "CHF" in self.symbol

    def is_eur_stablecoin(self) -> bool:
        return "EUR" in self.symbol

    def is_gbp_stablecoin(self) -> bool:
        return "GBP" in self.symbol

    def is_jpy_stablecoin(self) -> bool:
        return "JPY" in self.symbol

    def is_usd_stablecoin(self) -> bool:
        return "USD" in self.symbol or self.symbol in ("FRAX", "DAI", "MIM")

    def is_btc(self) -> bool:
        return "BTC" in self.symbol

    def is_eth(self) -> bool:
        return "ETH" in self.symbol


# The gas token/native asset for a chain
@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class NativeCoin[ChainType: Chain](Token[ChainType]):
    # https://chainagnostic.org/CAIPs/caip-20
    @property
    @typing.override
    def asset_namespace(self) -> str:
        return "slip44"

    # TODO: We might want to raise NotImplementedError here, but we're doing this for compatibility with the asset server
    @property
    @typing.override
    def address(self) -> str:
        return NATIVE_COIN_ADDRESS
    
    @typing.override
    def encode_address(self) -> bytes:
        raise NotImplementedError(f"Address not encodable: {self.address}")


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class ApprovableToken[ChainType: Chain](Token[ChainType]):
    @abc.abstractmethod
    async def get_allowance(
        self,
        owner: AccountID[ChainType],
        spender: AccountID[ChainType],
    ) -> int:
        pass

    @abc.abstractmethod
    async def approve(
        self,
        owner: Account[ChainType],
        spender: AccountID[ChainType],
        amount: int,
    ) -> Any:
        pass


# Avoid a circular import
from . import ethereum, solana, tron  # noqa: E402
