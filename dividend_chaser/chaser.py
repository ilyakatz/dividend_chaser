from dividend_chaser.models.position import Position
from dividend_chaser.models.dividendable import Dividendable
from dividend_chaser.brokers.abstract_broker import AbstractBroker
from dividend_chaser.workers.dividend_history import DividendHistory
import logging
from datetime import datetime


class Chaser:
  """ Threshold that determines whether to trade out current positions for a new one"""
  MINIMUM_DIVIDEND_DAYS = 4

  def __init__(self, broker: AbstractBroker):
    self.broker = broker

  """ Returns list of all support reits that Chaser supports
  """

  def reits(self):
    return list(DividendHistory.loadStocks().keys())

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

  """ Determines if current position should be traded for new one

  Parameters
  ----------
  position: Position
    Currently held position

  dividendanble: Dividendable
    Dividendable being considered for exchange

  Returns
  -------
  Boolean
    True or False if the current position should be traded out
  """

  def _should_exchange(self, position: Position, dividendable: Dividendable):
    current_time_to_next_dividend = position.time_to_next_dividend().days
    days_to_dividend = (dividendable.dividend_date - datetime.today()).days
    difference = current_time_to_next_dividend - days_to_dividend
    doit = (difference > Chaser.MINIMUM_DIVIDEND_DAYS)
    if(not doit):
      logging.info(
          f"New dividend date is only {difference} days away from current ( less than {Chaser.MINIMUM_DIVIDEND_DAYS} )")
    return doit

  """ Finds the next stock with the closest dividend date
  """

  def _next_stock(self):
    res = DividendHistory.upcoming()
    return res[0]

  def _run(self, symbol):
    if(symbol in self.reits()):
      logging.info(f"---START {symbol}---")
      position = Position(symbol, self.broker)
      res = position.is_allowed_to_sell()
      if(res.result):
        dividendable = self.find_better(position.symbol)
        if(self._should_exchange(position, dividendable)):
          logging.info(f"Proposal: Sell {position.symbol}, Buy {dividendable.symbol}")
        else:
          logging.info(f"Proposal: Do not sell {position.symbol}")

      else:
        logging.info(f"Not ready to sell \n {res.reasons}")
      logging.info(f"---END {symbol}---\n")
