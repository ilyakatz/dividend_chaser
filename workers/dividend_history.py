import pprint
import json
from yahoofinancials import YahooFinancials 
import numpy as np
import datetime

"""Class responsible for maintaining dividend history

DividendHistory retrieves and stores dividend history for 
desires instruments. History is stored in json file for 
easy retrieval
"""
class DividendHistory:
  def __init__(self, symbol):
    self.symbol=symbol
    self.filename='dividends.json'
    self.dividends_data=self.load()

  def load(self):
    file=open(self.filename)
    obj = json.load(file)
    return obj

  def dump(self):
    divs = self._get_dividends()
    self.dividends_data[self.symbol]=divs[self.symbol]
    with open(self.filename, 'w') as fp:
        json.dump(self.dividends_data, fp)

  def next_dividend(self):
    """ Returns estimated date for the next dividend 

    This can probably be replaced with real date from another data source
    """
    dates = self._dates()
    maximum = np.max(dates)
    return datetime.datetime.fromtimestamp(maximum) + self._average_dividend_interval()

  def _average_dividend_interval(self):
    """ Calculates how often dividends get paid 

    Return:  
    """
    dates = self._dates()
    a = np.array(dates)
    average = np.mean(np.diff(a))
    return datetime.timedelta(seconds=average)  

  def _dates(self):
    divs = self.dividends_data[self.symbol]
    return list(map(lambda x: x['date'], divs))

  def _get_dividends(self):
    start_date = '2019-01-15'
    end_date = '2019-09-15'
    symbol = self.symbol
    yahoo_financials = YahooFinancials([symbol])
    divs = yahoo_financials.get_daily_dividend_data(start_date, end_date)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(f"Dividends {divs}")
    return divs
