from dataclasses import dataclass
from typing import Dict, List
from .client import Admin, OrderSide, OrderTif, PublicOrder, Trader, Listener
from abc import ABC, abstractmethod
from .constants import CURRENCY
from .protos import marketdata_pb2 as marketdata
import asyncio

import uuid

@dataclass
class GameSymbolConfig:
    initial_position: int
    lower_bound: float
    upper_bound: float

class GameInterface(ABC):
    def __init__(self, url: str, admin_account: str, api_key: str, id: str = None):
        self.url = url
        self.admin = Admin(account=admin_account, api_key=api_key, url=url)
        self.account_types = []
        if id == None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.game_name = self.get_game_name()
        self.partition = self.game_name + self.id
        self.bot_account = "bot" + self.partition
        self.admin.register_bot_account(self.bot_account)
        self.bot = Trader(account=self.bot_account, api_key="bot", url=url)
        self.admin.set_position(self.bot_account, CURRENCY, 10000000000)
        self.bot_orders = set()
        self.orderbook = {}
        self.reset_orderbook()
    @abstractmethod
    def get_game_name(self) -> str:
        pass
    def bot_order(self, symbol: str, size: int, price: int, side: OrderSide, tif: OrderTif):
        response = self.bot.submit_order(symbol=symbol, size=size, price=price, side=side, tif=tif)
        id = response.message
        self.bot_orders.add(id)
        return response
    def bot_cancel(self, order_id: str):
        try:
            self.bot_orders.remove(order_id)
        except KeyError:
            pass
        return self.bot.cancel_order(order_id=order_id)
    def bot_cancel_all(self):
        ids = list(self.bot_orders)
        self.bot_orders.clear()
        return self.bot.cancel_orders(order_ids=ids)
    def get_symbols(self) -> List[str]:
        return list(self.get_symbol_config().keys())
    @abstractmethod
    def get_symbol_config(self) -> Dict[str, GameSymbolConfig]:
        pass
    @abstractmethod
    def get_initial_usd(self) -> int:
        pass
    def set_accounts(self, accounts: List[str]):
        self.accounts = accounts
    def init_account_positions(self, symbol: str, config: GameSymbolConfig):
        for account in self.accounts:
            self.admin.set_position(account, symbol, config.initial_position)
            self.admin.set_position_limits(account, symbol, config.lower_bound, config.upper_bound)
    def send_private_message(self, account: str, message: str):
        return self.admin.send_private_message(account, message)
    def send_public_message(self, message: str):
        return self.admin.send_public_message(self.partition, message)
    def start_game(self):
        self.admin.add_partition(self.partition)
        usd_pos = self.get_initial_usd()
        for account in self.accounts:
            self.admin.add_account_type_to_partition(self.partition, account)
            self.admin.set_position(account, CURRENCY, usd_pos)
        self.admin.add_account_type_to_partition(self.partition, self.bot_account)
        config = self.get_symbol_config()
        for symbol in config:
            self.admin.add_symbol(self.partition, self.name_to_id(symbol), symbol)
            self.init_account_positions(self.name_to_id(symbol), config[symbol])
            
        response = self.admin.start_partition(self.partition)
        print(response)
    def settle_game(self, settle_prices: Dict[str, int]):
        prices = {}
        for symbol in settle_prices:
            prices[self.name_to_id(symbol)] = settle_prices[symbol]
        return self.admin.settle_partition(self.partition, settle_prices=prices)
    @abstractmethod
    def game_body(self):
        pass
    @abstractmethod
    def game_settlement(self):
        pass
    def get_usd_positions(self) -> Dict[str, int]:
        pos = {}
        for account in self.accounts:
            pos[account] = self.admin.get_position(account, CURRENCY)
        return pos
    def name_to_id(self, symbol) -> str:
        return self.partition + symbol
    def reset_orderbook(self):
        config = self.get_symbol_config()
        for symbol in config:
            book = {}
            book['bids'] = []
            book['asks'] = []
            self.orderbook[symbol] = book
    async def listen(self):
        # Build your subscription request. Adjust fields as needed.
        listener = Listener(self.bot_account, api_key="bot", url=self.url)
        try:
            request = marketdata.SubscriptionRequest(
                api_key="bot",
                account=self.bot_account
            )

            # Calling the streaming RPC method.
            stream = listener.stub.StreamStatus(request)
            # Iterate over the stream of responses.
            async for market_data in stream:
                field = market_data.WhichOneof("response")
                if field == "orderbook":
                    orderbook = market_data.orderbook
                    symbol = orderbook.symbol
                    book = {}
                    book['bids'] = list(map(lambda x: PublicOrder(x.symbol, int(x.size), int(x.price)), orderbook.book.bids))
                    book['asks'] = list(map(lambda x: PublicOrder(x.symbol, int(x.size), int(x.price)), orderbook.book.bids))
                    self.orderbook[symbol] = book
        except asyncio.CancelledError:
            raise
    @abstractmethod
    def post_game_processing(self):
        pass
    async def run_game(self):
        self.start_game()
        task1 = asyncio.create_task(self.listen())
        # Run the synchronous run() in an executor.
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.game_body)
        task1.cancel()
        try:
            await task1
        except asyncio.CancelledError:
            pass
        self.game_settlement()
        self.reset_orderbook()
        self.post_game_processing()
        
        