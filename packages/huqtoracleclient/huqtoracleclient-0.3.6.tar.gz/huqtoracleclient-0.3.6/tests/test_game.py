from typing import Dict
from huqt_oracle_client.client import OrderSide, OrderTif
from huqt_oracle_client.game import GameInterface, GameSymbolConfig
from random import randint
import asyncio
import time
class NumberGame(GameInterface):
    def __init__(self, url: str, admin_account: str, api_key: str, id: str = None):
        super().__init__(url=url, admin_account=admin_account, api_key=api_key, id=id)
        self.num = randint(10, 20)
    def get_game_name(self):
        return "number"
    def get_initial_usd(self) -> int:
        return 200000
    def get_symbol_config(self) -> Dict[str, GameSymbolConfig]:
        return {
                "NUM": GameSymbolConfig(initial_position=0, lower_bound=-100, upper_bound=100),
                "MUN": GameSymbolConfig(initial_position=0, lower_bound=-100, upper_bound=100)
                }
    def game_body(self):
        response = self.send_public_message("I have a secret number n from 10 and 20 inclusive. NUM will be valued at n and MUN will be valued at 30-n. My bots know the value of n and will trade accordingly.")
        print(response)
        for _ in range(20):
            time.sleep(1)
            # there is a listener that continuously updates the order book
            print(self.orderbook)
            self.bot_order("NUM", size = 10, price = self.num * 100, side = OrderSide.BUY, tif = OrderTif.IOC)
            self.bot_order("NUM", size = 10, price = self.num * 100, side = OrderSide.SELL, tif = OrderTif.IOC)
            self.bot_order("MUN", size = 10, price = (30 - self.num) * 100, side = OrderSide.BUY, tif = OrderTif.IOC)
            self.bot_order("MUN", size = 10, price = (30 - self.num) * 100, side = OrderSide.SELL, tif = OrderTif.IOC)
    def game_settlement(self):
        response = self.send_public_message("NUM was " + str(self.num) + " and MUN was " + str(30-self.num) + ".")
        print(response)
        self.settle_game({
            "NUM": self.num * 100,
            "MUN": (30 - self.num) * 100
        })
    def post_game_processing(self):
        print(self.get_usd_positions())

game = NumberGame(url='huqt-oracle-rust.fly.dev:443', admin_account="account", api_key="sigma", id="FRIGMA")
game.set_accounts(["andrew018.gu@gmail.com"])
asyncio.run(game.run_game())
