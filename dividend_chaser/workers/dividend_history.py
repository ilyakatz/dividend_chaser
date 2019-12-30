import json
import datetime
import pprint
import logging
from json import JSONDecodeError
from yahoofinancials import YahooFinancials
import numpy as np
from pandas import np
import pandas_datareader as web

from dividend_chaser.models.dividendable import Dividendable

"""Class responsible for maintaining dividend history

DividendHistory retrieves and stores dividend history for 
desires instruments. History is stored in json file for 
easy retrieval
"""


class DividendHistory:
  filename = 'dividends.json'

  def __init__(self, symbol):
    self.symbol = symbol
    self.filename = 'dividends.json'
    self.dividends_data = self.load()

  @classmethod
  def loadStocks(cls):
    with open(DividendHistory.filename) as file:
      obj = json.load(file)
      return obj

  """ Return the annualized stddev of daily log returns of
  """
  @classmethod
  def historical_volatility(cls, sym, days):
    quotes = web.DataReader(sym, 'yahoo')['Close'][-days:]
    logreturns = np.log(quotes / quotes.shift(1))
    return np.sqrt(252 * logreturns.var())

  """ Finds the candidates for positions that have upcoming dividends

  Returns
  -------
  Array[Dividendable]
  """
  @classmethod
  def upcoming(cls):
    stocks = DividendHistory.loadStocks()
    arr = list(stocks.items())
    simplified = list(map(lambda x: Dividendable(
        x[0], x[1]['next_dividend']['formatted_date']), arr))
    simplified.sort(key=lambda x: x.dividend_date, reverse=False)
    filtered = list(
        filter(lambda dividendable: dividendable.is_clearable(), simplified))

    logging.info(f"Upcoming dividends {filtered}")
    return filtered

  def load(self):
    try:
      with open(self.filename) as file:
        obj = json.load(file)
    except JSONDecodeError:
      obj = {
          self.symbol: {}
      }

    if(self.symbol not in obj):
      obj[self.symbol] = {}
    return obj

  def dump(self):
    divs = self._get_dividends()
    self.dividends_data[self.symbol]["dividends"] = divs[self.symbol]
    self._enrich_with_volatililty()
    self._enrich_with_next_dividend()
    self._enrich_with_dividend_yield()

    with open(self.filename, 'w') as fp:
      json.dump(self.dividends_data, fp)

  """
  Returns
  _______
  dateime.date
  """

  def next_dividend(self):
    " TODO maybe can use get_exdividend_date "
    new_date = self.dividends_data[self.symbol]['next_dividend']['formatted_date']
    return datetime.date.fromisoformat(new_date)

  def _calculate_next_dividend(self):
    """ Returns estimated date for the next dividend 

    """
    symbol = self.symbol
    yahoo_financials = YahooFinancials([symbol])
    data = yahoo_financials.get_exdividend_date()
    date_str = data[symbol]
    next_div_date = datetime.date.fromisoformat(date_str)
    today = datetime.date.today()

    " at times, yahoo does not return correct next date "
    if (next_div_date < today):
      logging.info("Next dividend date is not yet known. Estimating ...")
      dates = self._dates()
      maximum = np.max(dates)
      next_div_date = datetime.datetime.fromtimestamp(maximum) + self._average_dividend_interval()

    return next_div_date

  def _enrich_with_next_dividend(self):
    next_dividend_date = self._calculate_next_dividend()
    next_estimate_hash = {
        "date": str(next_dividend_date),
        "formatted_date": next_dividend_date.strftime("%Y-%m-%d")
    }
    self.dividends_data[self.symbol]["next_dividend"] = next_estimate_hash

  def _enrich_with_dividend_yield(self):
    symbol = self.symbol
    yahoo_financials = YahooFinancials([symbol])
    divs = yahoo_financials.get_dividend_yield()
    self.dividends_data[self.symbol]["dividend_yield"] = divs[self.symbol]

  def _enrich_with_volatililty(self):
    self.dividends_data[self.symbol]["volatililty"] = DividendHistory.historical_volatility(self.symbol, 365)

  def _average_dividend_interval(self):
    """ Calculates how often dividends get paid 

    Return:  
    """
    dates = self._dates()
    a = np.array(dates)
    average = np.mean(np.diff(a))
    return datetime.timedelta(seconds=average)

  def _dates(self):
    divs = self.dividends_data[self.symbol]["dividends"]
    return list(map(lambda x: x['date'], divs))

  def _get_dividends(self):
    start_date = '2018-01-15'
    d = datetime.datetime.today()
    end_date = d.strftime("%Y-%m-%d")
    symbol = self.symbol
    yahoo_financials = YahooFinancials([symbol])
    divs = yahoo_financials.get_daily_dividend_data(start_date, end_date)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(f"Dividends {divs}")
    return divs
