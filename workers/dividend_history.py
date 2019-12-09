import pprint
import json
from models.dividendable import Dividendable
from yahoofinancials import YahooFinancials
import numpy as np
import datetime
from json import JSONDecodeError
import logging

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
  def loadStocks(self):
    file = open(DividendHistory.filename)
    obj = json.load(file)
    return obj

  """ Finds the candidates for positions that have upcoming dividends

  Returns
  -------
  Array[Dividendable]
  """
  @classmethod
  def upcoming(self):
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
      file = open(self.filename)
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
    self._enrich_with_next_dividend()

    with open(self.filename, 'w') as fp:
      json.dump(self.dividends_data, fp)

  def next_dividend(self):
    """ Returns estimated date for the next dividend 

    This can probably be replaced with real date from another data source
    """
    dates = self._dates()
    maximum = np.max(dates)
    return datetime.datetime.fromtimestamp(maximum) + self._average_dividend_interval()

  def _enrich_with_next_dividend(self):
    next_dividend_date = self.next_dividend()
    next_estimate_hash = {
        "date": str(next_dividend_date),
        "formatted_date": next_dividend_date.strftime("%Y-%m-%d")
    }
    self.dividends_data[self.symbol]["next_dividend"] = next_estimate_hash

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
