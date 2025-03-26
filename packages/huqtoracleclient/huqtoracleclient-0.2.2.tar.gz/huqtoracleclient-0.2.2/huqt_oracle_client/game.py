from dataclasses import dataclass
from typing import Dict, List
from .client import Admin, OrderSide, OrderTif, Trader
from abc import ABC, abstractmethod
from .constants import CURRENCY

import uuid

@dataclass
class GameSymbolConfig:
    initial_position: int
    lower_bound: float
    upper_bound: float

class GameInterface(ABC):
    def __init__(self, url: str, admin_account: str, api_key: str, game_name: str, id: str = None):
        self.admin = Admin(account=admin_account, api_key=api_key, url=url)
        self.account_types = []
        if id == None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.game_name = game_name
        self.partition = self.game_name + self.id
        self.bot_account = "bot" + self.id
        self.admin.register_bot_account(self.bot_account)
        self.bot = Trader(account=self.bot_account, api_key="bot", url=url)
        self.admin.set_position(self.bot_account, CURRENCY, 10000000000)
        self.bot_orders = set()
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
        for account in self.accounts:
            self.admin.add_account_type_to_partition(self.partition, account)
        self.admin.add_account_type_to_partition(self.partition, self.bot_account)
        config = self.get_symbol_config()
        for symbol in config:
            self.admin.add_symbol(self.partition, symbol + self.id, symbol)
            self.init_account_positions(symbol, config[symbol])
        response = self.admin.start_partition(self.partition)
        print(response)
    def settle_game(self, settle_prices: Dict[str, int]):
        return self.admin.settle_partition(self.partition, settle_prices=settle_prices)
    @abstractmethod
    def game_body(self):
        pass
    @abstractmethod
    def game_settlement(self):
        pass
    def run_game(self):
        self.start_game()
        self.game_body()
        self.game_settlement()
        
        