import json
import datetime
import pprint
import logging
import sys
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

  def __init__(self, symbols):
    self.symbols = symbols
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
    # pylint: disable=W0702
    logging.debug("Fetching historical volatility from yahoo")
    try:
      data = web.DataReader(sym, 'yahoo')
    except:
      return None

    quotes = data['Close'][-days:]
    logreturns = np.log(quotes / quotes.shift(1))
    return np.sqrt(252 * logreturns.var())

  """ Finds the candidates for positions that have upcoming dividends

  Parameters
  ----------
  limit_days: int
     Limit to number of days in the future of when the next dividend is expected

  Returns
  -------
  Array[Dividendable]
  """
  @classmethod
  def upcoming(cls, limit_days=14):
    stocks = DividendHistory.loadStocks()
    arr = list(stocks.items())
    simplified = list(map(lambda x: Dividendable(
        x[0],
        x[1]['next_dividend']['formatted_date'],
        x[1]['dividend_yield'],
        x[1]['volatililty'],
        x[1].get('average_volume')), arr))
    simplified = list(filter(lambda d: d.dividend_date.date() < (
        datetime.date.today() + datetime.timedelta(days=limit_days)), simplified))

    simplified.sort(key=lambda x: x.dividend_date, reverse=False)
    filtered = list(
        filter(lambda dividendable: dividendable.is_clearable(), simplified))

    return filtered

  @classmethod
  def load_from_db(cls):
    try:
      with open(DividendHistory.filename) as file:
        obj = json.load(file)
    except JSONDecodeError:
      obj = {
      }
    return obj

  def load(self):
    obj = DividendHistory.load_from_db()

    for symbol in self.symbols:
      if(symbol not in obj):
        obj[symbol] = {}

    return obj

  def dump(self):
    # pylint: disable=W0702
    divs = self._get_dividends(self.symbols)
    for symbol in self.symbols:
      self.dividends_data[symbol]["dividends"] = divs[symbol]

    try:
      self._enrich(self.symbols)
      with open(self.filename, 'w') as fp:
        json.dump(self.dividends_data, fp)
    except:
      print("Unexpected error:", sys.exc_info()[0])

  def _enrich(self, symbols):
    logging.debug("Starting _enrich")
    self._enrich_with_volatililty(symbols)
    self._enrich_with_volume(symbols)
    self._enrich_with_next_dividend(symbols)
    self._enrich_with_dividend_yield(symbols)
    logging.debug("Finished _enrich")

  """
  Returns
  _______
  dateime.date
  """

  @classmethod
  def next_dividend(cls, symbol):
    " TODO maybe can use get_exdividend_date "
    data = DividendHistory.load_from_db()
    new_date = data[symbol]['next_dividend']['formatted_date']
    return datetime.date.fromisoformat(new_date)

  """
  Returns
  -------
  Hash[String: datetime.date]
  """

  def _calculate_next_dividend(self, symbols):
    """ Returns estimated date for the next dividend

    """
    yahoo_financials = YahooFinancials(symbols)
    logging.debug("Fetching get_exdividend_date")
    data = yahoo_financials.get_exdividend_date()
    logging.debug("Finished fetching get_exdividend_date")
    next_div_dates = {}
    for symbol in symbols:
      dividends = self._next_div(data, symbol)
      next_div_dates[symbol] = dividends

    return next_div_dates

  def _next_div(self, data, symbol):
    date_str = data[symbol]
    next_div_date = datetime.date.fromisoformat(date_str)
    today = datetime.date.today()

    " at times, yahoo does not return correct next date "
    if (next_div_date < today):
      logging.info("Next dividend date is not yet known. Estimating ...")
      next_div_date = self._estimate_next_date(next_div_date, symbol)

    return next_div_date

  def _estimate_next_date(self, next_div_date, symbol):
    dates = self._dates(symbol)
    next_div_date_in_seconds = next_div_date.strftime('%s')
    dates.append(int(next_div_date_in_seconds))
    maximum = np.max(dates)
    return datetime.datetime.fromtimestamp(maximum) + self._average_dividend_interval(symbol)

  def _enrich_with_next_dividend(self, symbols):
    next_dividend_dates = self._calculate_next_dividend(symbols)
    for symbol in symbols:
      next_dividend_date = next_dividend_dates[symbol]
      print(next_dividend_date)
      next_estimate_hash = {
          "date": str(next_dividend_date),
          "formatted_date": next_dividend_date.strftime("%Y-%m-%d")
      }
      self.dividends_data[symbol]["next_dividend"] = next_estimate_hash

  def _enrich_with_dividend_yield(self, symbols):
    yahoo_financials = YahooFinancials(symbols)
    logging.debug("Fetching get_dividend_yield")
    divs = yahoo_financials.get_dividend_yield()
    logging.debug("Finished fetching get_exdividend_date")
    for symbol in symbols:
      self.dividends_data[symbol]["dividend_yield"] = divs[symbol]

  def _enrich_with_volatililty(self, symbols):
    for symbol in symbols:
      self.dividends_data[symbol]["volatililty"] = DividendHistory.historical_volatility(symbol, 365)

  def _enrich_with_volume(self, symbols):
    yahoo_financials = YahooFinancials(symbols)
    logging.debug("Fetching three_month_avg_daily_volume")
    res = yahoo_financials.get_three_month_avg_daily_volume()
    logging.debug("Finished fetching three_month_avg_daily_volume")
    for symbol in symbols:
      self.dividends_data[symbol]["average_volume"] = res[symbol]

  def _average_dividend_interval(self, symbol):
    """ Calculates how often dividends get paid

    Return:
    """
    dates = self._dates(symbol)
    a = np.array(dates)
    average = np.mean(np.diff(a))
    return datetime.timedelta(seconds=average)

  def _dates(self, symbol):
    divs = self.dividends_data[symbol]["dividends"]
    return list(map(lambda x: x['date'], divs))

  def _get_dividends(self, symbols):
    start_date = '2018-01-15'
    d = datetime.datetime.today()
    end_date = d.strftime("%Y-%m-%d")
    yahoo_financials = YahooFinancials(symbols)
    divs = yahoo_financials.get_daily_dividend_data(start_date, end_date)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(f"Dividends {divs}")
    return divs
