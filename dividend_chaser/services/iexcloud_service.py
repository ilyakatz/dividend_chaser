from iexfinance.stocks import Stock
import logging


class IExcloudService: 
  def __init__(self, symbols):
    self.symbols = symbols
    self.fin_data = {}
    for symbol in symbols:
      self.fin_data[symbol] = {}

  def next_dividend(self, symbol):
    return self.fin_data[symbol]["next_dividend"]

  def calculate_next_dividend(self):
    for symbol in self.symbols:
      logging.debug("IExcloudService - Fetching get_dividends")
      stock = Stock(symbol)
      logging.debug("IExcloudService - Finished fetching get_dividends")

      div_data = stock.get_dividends()

      self.fin_data[symbol]["next_dividend"] = div_data[0]['exDate']
