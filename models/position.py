import pprint
from brokers.abstract_broker import AbstractBroker
from workers.dividend_history import DividendHistory
import datetime
import collections
import logging

pp = pprint.PrettyPrinter(indent=4)


class Position:
  PRICE_THREADSHOLD = 0.5
  DAYS_THREASHOLD = 5

  """ Tuple that holds result and reasons for results"""
  BooleanResultWithReasons = collections.namedtuple(
      'BooleanResultWithReasons', "result reasons")

  """Object that representation an instance of an REIT and operations that can be take on it
  """

  def __init__(self, symbol, broker: AbstractBroker):
    self.symbol = symbol
    self.bought_price = None
    self.broker = broker
    self.current_price = None
    self.details = None

  def get_details(self):
    my_stocks = self.broker.positions()
    for key, value in my_stocks.items():
      if(key == self.symbol):
        self.bought_price = float(value['average_buy_price'])
        logging.info(f"Bought {key} for ${self.bought_price}")
    self.get_current_price()

  def _details_required(function):
    def details(self, *args, **kwargs):
      if(self.details is None):
        logging.info("Getting details")
        self.details = self.get_details()

      return function(self, *args, **kwargs)
    return details

  @_details_required
  def is_allowed_to_sell(self):
    """Returns an indication that the current stock can be sold.

    A stock can be sold if it's current price is greater than the 
    price at which it was bought within a certain range

    Returns
    -------
    Position.BooleanResultWithReasons
      Tuple indicating with boolean and reasons of explaning the results
    """

    price_threshold_met = (self.current_price - self.bought_price) > -Position.PRICE_THREADSHOLD
    to_sell = True
    reasons = []
    if(not price_threshold_met):
      to_sell = False
      reasons.append(
          f"Current price is not within {Position.PRICE_THREADSHOLD}")

    # TODO: self.time_to_next_dividend().days rounds down
    next_dividend_days = self.time_to_next_dividend().days
    next_dividend_met = next_dividend_days > Position.DAYS_THREASHOLD
    if(not next_dividend_met):
      to_sell = False
      reasons.append(
          f"Next dividend is only {next_dividend_days} days away (less than {Position.DAYS_THREASHOLD} )")

    return Position.BooleanResultWithReasons(result=to_sell, reasons=reasons)

  def get_current_price(self):
    self.current_price = self.broker.get_current_price(self.symbol)
    current_price = self.broker.get_current_price(self.symbol)
    logging.info(f"Current price ${current_price}")
    return current_price

  """Calculate time untl next dividend is to be paid out

  Returns
  -------
  datetime.timedelta
  """

  def time_to_next_dividend(self):
    next_date = DividendHistory(self.symbol).next_dividend()
    res = next_date - datetime.datetime.now()
    logging.info(f"Time to next dividend {res}")
    return res

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return f"<Dividedable symbol={self.symbol} >"