from models.reit import REIT
from brokers.abstract_broker import AbstractBroker

class Chaser:
  def __init__(self, broker: AbstractBroker):
    self.broker=broker

  def reits(self):
    return ["STWD", "MPW"]

  def positions(self):
    my_stocks = self.broker.positions()
    for key,value in my_stocks.items():
      if(key in self.reits()):
        print(key)
        reit = REIT(key, self.broker)
        reit.get_details()
        print(f"Can sell {reit.is_allowed_to_sell()}")
        print("------")