from datetime import datetime
import numpy as np


class Dividendable:
  CLEARANCE_DAYS = 2
  """
  Parameters
  ----------
  symbol : str
    Ticker Symbol
  dividend_date : str 
    Date of the next dividend in %Y-%m-%d format
  """

  # pylint: disable=R0913
  def __init__(self, symbol, dividend_date, dividend_yield, volatililty, average_volume):
    self.symbol = symbol
    self.dividend_date = datetime.strptime(dividend_date, "%Y-%m-%d")
    self.dividend_yield = dividend_yield
    self.volatililty = volatililty
    self.average_volume = average_volume

  def is_clearable(self):
    today = datetime.now().strftime('%Y-%m-%d')
    date = self.dividend_date.strftime('%Y-%m-%d')
    return np.busday_count(today, date) > Dividendable.CLEARANCE_DAYS

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return f"""<Dividedable \
symbol={self.symbol} \
volatililty={self.volatililty} \
dividend_yield={self.dividend_yield} \
average_volume={self.average_volume} \
dividend_date={self.dividend_date.strftime('%Y-%m-%d')} \
/>"""
