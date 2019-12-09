from models.position import Position
from brokers.abstract_broker import AbstractBroker
from workers.dividend_history import DividendHistory
import logging


class Chaser:

  def __init__(self, broker: AbstractBroker):
    self.broker = broker

  def reits(self):
    return ["STWD", "MPW"]

  def run(self):
    my_stocks = self.broker.positions()
    for key, _ in my_stocks.items():
      self._run(key)

  """ Attempts to find an alternative stock to buy

  If there is another stock that has dividents coming up
  that are worth buying, this will sell the current one
  and buy the new alternative
  """

  def find_better(self, symbol):
    next_stock = self._next_stock()
    return next_stock

  """ Finds the next stock with the closest dividend date
  """

  def _next_stock(self):
    res = DividendHistory.upcoming()
    return res[0]

  def _run(self, symbol):
    if(symbol in self.reits()):
      logging.info(f"---START {symbol}---")
      reit = Position(symbol, self.broker)
      res = reit.is_allowed_to_sell()
      if(res.result):
        logging.info(
            f"Proposal: Sell {reit.symbol}, Buy {self.find_better(reit.symbol).symbol}")
      else:
        logging.info(f"Not ready to sell \n {res.reasons}")
      logging.info(f"---END {symbol}---\n")
