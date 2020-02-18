import logging
from datetime import datetime
import click

from dividend_chaser.orm import orm
from dividend_chaser.models.position import Position
from dividend_chaser.models.dividendable import Dividendable
from dividend_chaser.brokers.abstract_broker import AbstractBroker
from dividend_chaser.workers.dividend_history import DividendHistory


class Chaser:
  """ Threshold that determines whether to trade out current positions for a new one"""
  MINIMUM_DIVIDEND_DAYS = 4

  """ In order to dercrease effect of volatile stocks,
  this is the threshold that will be used to determine which stocks to pick
  """
  VOLATILITY_THREASHOLD = 0.15

  def __init__(self, broker: AbstractBroker):
    self.broker = broker

  """ Returns list of all support reits that Chaser supports
  """

  def reits(self):
    records = orm.Dividendable.all()
    stocks = list(map(lambda x: x.symbol, records))
    return stocks

  def run(self):
    my_stocks = self.broker.positions()
    for _, position in my_stocks.items():
      self._run(position)

  """ Attempts to find an alternative stock to buy

  If there is another stock that has dividents coming up
  that are worth buying, this will sell the current one
  and buy the new alternative
  """

  def find_better(self):
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
  Position.BooleanResultWithReasons
    Tuple indicating with boolean and reasons of explaning the results
  """

  def _should_exchange(self, position: Position, dividendable: Dividendable):
    if(not dividendable):
      reason = f"No new dividendable available"
      logging.info(reason)
      return Position.BooleanResultWithReasons(result=False, reasons=reason)
    current_time_to_next_dividend = position.time_to_next_dividend().days

    if(current_time_to_next_dividend <= -1):
      reason = f"Dividend for {position.symbol} was paid out recently ({abs(current_time_to_next_dividend)}) days"
      return Position.BooleanResultWithReasons(result=True, reasons=reason)

    days_to_dividend = (dividendable.dividend_date - datetime.today()).days
    difference = days_to_dividend - current_time_to_next_dividend
    doit = (difference <= -Chaser.MINIMUM_DIVIDEND_DAYS)
    if(doit):
      reason = f"Current dividend date is {difference} days LATER than the first available swap"
      logging.info(reason)
      return Position.BooleanResultWithReasons(result=True, reasons=reason)
    reason = f"Current dividend date is {difference} days EARLIER than the first available swap"
    return Position.BooleanResultWithReasons(result=False, reasons=reason)

  """ Finds the next stock with the closest dividend date
  """

  def _next_stock(self):
    upcoming = DividendHistory.upcoming(limit_days=7)
    positions_dic = self.broker.positions()
    positions = list(positions_dic.keys())
    filtered = list(filter(lambda d: d.symbol not in positions, upcoming))
    filtered = list(filter(lambda d: d.volatililty < self.VOLATILITY_THREASHOLD, filtered))
    logging.info(f"Upcoming dividends {filtered}")
    if(len(filtered) == 0):
      return None
    return filtered[0]

  def _run(self, position: Position):
    symbol = position.symbol
    if(symbol in self.reits()):
      logging.info(f"---START {symbol}---")
      res = position.is_allowed_to_sell()
      if(res.result):
        dividendable = self.find_better()
        res = self._should_exchange(position, dividendable)
        if(res.result):
          logging.info(f"Proposal: Sell {position.symbol}, Buy {dividendable.symbol} \n {res.reasons}")
          if click.confirm(f"Do you want to sell {position.symbol} and buy {dividendable.symbol}", default=True):
            logging.info("SWAPPPING")
            self.broker.exchange(position.symbol, dividendable.symbol)
          else:
            logging.info("Skipping swap")
        else:
          logging.info(f"Proposal: Do not sell {position.symbol} \n {res.reasons}")

      else:
        logging.info(f"Not ready to sell \n {res.reasons}")
      logging.info(f"---END {symbol}---\n")
