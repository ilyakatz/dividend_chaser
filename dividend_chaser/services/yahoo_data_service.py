import datetime
import logging
from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np
import pandas_datareader as web


class YahooDataService:
  def __init__(self, symbols):
    self.symbols = symbols
    self.fin_data = {}
    for symbol in symbols:
      self.fin_data[symbol] = {}

  def volatililty(self, symbol):
    return self.fin_data[symbol]["volatililty"]

  def average_volume(self, symbol):
    return self.fin_data[symbol]["average_volume"]

  def calculate_average_volume(self):
    yahoo_financials = YahooFinancials(self.symbols)
    logging.debug("Fetching get_three_month_avg_daily_volume")
    yahoo_data = yahoo_financials.get_three_month_avg_daily_volume()
    logging.debug("Finished detching get_three_month_avg_daily_volume")
    for symbol in self.symbols:
      self.fin_data[symbol]["average_volume"] = yahoo_data[symbol]

  def calculate_historical_volatility(self):
    symbols = self.symbols

    end_date = datetime.date.today() 
    # 163 was added to accomodate for legacy historical volatility
    # i believe this accomodates for holidays
    start_date = end_date - datetime.timedelta(days=365 + 163)

    end_date_str = end_date.strftime("%Y-%m-%d")
    start_date_str = start_date.strftime("%Y-%m-%d")

    yahoo_financials = YahooFinancials(symbols)
    yahoo_data = yahoo_financials.get_historical_price_data(start_date_str, end_date_str, 'daily')

    for symbol in self.symbols:
      self.fin_data[symbol]["volatililty"] = self._historical_volatility(symbol, yahoo_data)

  """ Return the annualized stddev of daily log returns of
  """

  def _historical_volatility(self, symbol, yahoo_data):
    prices = yahoo_data[symbol]['prices']
    close_prices = {}
    for x in prices:
      close_prices[x["formatted_date"]] = x["close"]

    quotes = pd.Series(close_prices, name="Close")

    logreturns = np.log(quotes / quotes.shift(1))
    res = np.sqrt(252 * logreturns.var())

    return res

  def legacy_volatililty(self, symbol):
    # pylint: disable = W0702
    days = 365
    logging.debug("Fetching historical volatility from yahoo")
    try:
      data = web.DataReader(symbol, 'yahoo')
    except:
      return None
    legacy_quotes = data['Close'][-days:]
    logreturns_old = np.log(legacy_quotes / legacy_quotes.shift(1))
    legacy_res = np.sqrt(252 * logreturns_old.var())
    return legacy_res
