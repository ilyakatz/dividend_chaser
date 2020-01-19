from abc import ABC, abstractmethod
import datetime
import logging
import numpy as np


class BaseDataService(ABC):
  # pylint: disable=R0903
  def __init__(self, symbols, dividends_data=None):
    self.symbols = symbols
    self.fin_data = {}
    self.dividends_data = dividends_data
    for symbol in symbols:
      self.fin_data[symbol] = {}

  def calculate_next_dividend(self):
    next_dividend_dates = self._calculate_next_dividend(self.symbols)
    for symbol in self.symbols:
      next_dividend_date = next_dividend_dates[symbol]

      value = next_dividend_date["value"]
      actual = next_dividend_date["actual"]

      next_estimate_hash = {
          "date": str(value),
          "formatted_date": value.strftime("%Y-%m-%d"),
          "actual": actual
      }
      self.fin_data[symbol]["next_dividend"] = next_estimate_hash

  @abstractmethod
  def _calculate_next_dividend(self, symbols):
    pass

  def _next_div(self, data, symbol):
    date_str = data[symbol]
    next_div_date = datetime.date.fromisoformat(date_str)
    today = datetime.date.today()

    " at times, yahoo does not return correct next date "
    if (next_div_date < today):
      logging.info(f"Next dividend date is not yet known for {symbol}. Estimating ...")
      next_div_date = self._estimate_next_date(next_div_date, symbol)
      actual = False
    else:
      actual = True

    obj = {
        "value": next_div_date,
        "actual": actual
    }

    return obj

  def _estimate_next_date(self, next_div_date, symbol):
    dates = self._dates(symbol)
    next_div_date_in_seconds = next_div_date.strftime('%s')
    dates.append(int(next_div_date_in_seconds))
    maximum = np.max(dates)
    return datetime.datetime.fromtimestamp(maximum) + self._average_dividend_interval(symbol)

  def _dates(self, symbol):
    divs = self.dividends_data[symbol]["dividends"]
    return list(map(lambda x: x['date'], divs))

  def _average_dividend_interval(self, symbol):
    """ Calculates how often dividends get paid

    Return:
    """
    dates = self._dates(symbol)
    a = np.array(dates)
    average = np.mean(np.diff(a))
    return datetime.timedelta(seconds=average)