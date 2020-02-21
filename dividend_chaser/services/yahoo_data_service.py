import datetime
import logging
from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np
import pandas_datareader as web

from dividend_chaser.services.base_data_service import BaseDataService
from dividend_chaser.models.data_service_configuration import DataServiceConfiguration


class YahooDataService(BaseDataService):
  def __init__(self, symbols, dividends_data, config=DataServiceConfiguration()):
    super().__init__(symbols, dividends_data, config)

  def volatililty(self, symbol):
    return self.fin_data[symbol]["volatililty"]

  def average_volume(self, symbol):
    return self.fin_data[symbol].get("average_volume")

  def next_dividend(self, symbol):
    return self.fin_data[symbol]["next_dividend"]

  def dividend_yield(self, symbol):
    return self.fin_data[symbol]["dividend_yield"]

  def calculate_dividend_yield(self):
    yahoo_financials = YahooFinancials(self.symbols)
    logging.debug("[calculate_dividend_yield] YahooFinancials - Fetching get_dividend_yield")
    divs = yahoo_financials.get_dividend_yield()
    logging.debug("[calculate_dividend_yield] YahooFinancials - Finished fetching get_exdividend_date")
    for symbol in self.symbols:
      self.fin_data[symbol]["dividend_yield"] = divs[symbol]

  def calculate_average_volume(self):
    if(self.config.is_skip_average_volume()):
      logging.info("[calculate_average_volume] Skipping calculate_average_volume")
      return

    yahoo_financials = YahooFinancials(self.symbols)
    logging.debug("YahooFinancials - Fetching get_three_month_avg_daily_volume")
    yahoo_data = yahoo_financials.get_three_month_avg_daily_volume()
    logging.debug("YahooFinancials - Finished fetching get_three_month_avg_daily_volume")
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
    logging.debug("YahooFinancials - Fetching historical volatility from yahoo")
    try:
      data = web.DataReader(symbol, 'yahoo')
    except:
      return None
    legacy_quotes = data['Close'][-days:]
    logreturns_old = np.log(legacy_quotes / legacy_quotes.shift(1))
    legacy_res = np.sqrt(252 * logreturns_old.var())
    return legacy_res

  def _calculate_next_dividend(self, symbols):
    """ Returns estimated date for the next dividend

    """
    yahoo_financials = YahooFinancials(symbols)
    logging.debug("[_calculate_next_dividend] Fetching get_exdividend_date")
    data = yahoo_financials.get_exdividend_date()
    logging.debug("[_calculate_next_dividend] Finished fetching get_exdividend_date")
    next_div_dates = {}
    for symbol in symbols:
      dividends = self._next_div(data, symbol)
      next_div_dates[symbol] = dividends

    return next_div_dates
