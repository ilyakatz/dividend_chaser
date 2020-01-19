import logging
import datetime
from iexfinance.stocks import Stock

from dividend_chaser.services.base_data_service import BaseDataService


class IExcloudService(BaseDataService):
  def __init__(self, symbols, dividends_data):
    super().__init__(symbols, dividends_data)

  def next_dividend(self, symbol):
    return self.fin_data[symbol]["next_dividend"]

  def _calculate_next_dividend(self, symbols):
    """ Returns estimated date for the next dividend

    Returns
    -------
    If date is unknown, returns beginning of epoch
    """
    next_div_dates = {}
    for symbol in symbols:
      logging.debug("IExcloudService - Fetching get_dividends")
      stock = Stock(symbol)
      logging.debug("IExcloudService - Finished fetching get_dividends")

      logging.error("IExcloud does not return dividend dates correctly")
      div_data = stock.get_dividends()
      if div_data:
        data = {symbol: div_data[0]['exDate']}
      else:
        epoch = datetime.datetime(1970, 1, 1).date()
        data = {symbol: epoch.strftime("%Y-%m-%d")}

      dividends = self._next_div(data, symbol)
      next_div_dates[symbol] = dividends

    return next_div_dates
