import robin_stocks as r
from brokers.abstract_broker import AbstractBroker
import logging
import more_itertools as mit


class Broker(AbstractBroker):
  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.login = None

  def _login_required(function):
    def auth(self, *args, **kwargs):
      if(self.login is None):
        logging.info("Logging in to Robinhood 🏹")
        self.login = r.login(self.username, self.password)

      return function(self, *args, **kwargs)
    return auth

  @_login_required
  def get_current_price(self, symbol):
    data = r.stocks.get_quotes(symbol)
    current_price = data[0]['last_trade_price']
    price = float(current_price)
    return price

  @_login_required
  def broker(self):
    return r

  @_login_required
  def positions(self):
    my_stocks = r.build_holdings()
    return my_stocks

  @_login_required
  def get_dividends(self):
    return self.broker().account.get_dividends()

  @_login_required
  def dividend_history_for(self, symbol):
    info = self.broker().stocks.get_instruments_by_symbols(symbol)
    info = list(filter(None, info))

    instrument_ids = list(map(lambda x: x["id"], info))

    all_dividends = self.broker().account.get_dividends()
    relevent_dividends = list(
        filter(
            lambda dividend_info: any(
                dividend_info['instrument'].find(i) > 0 for i in instrument_ids),
            all_dividends))

    return relevent_dividends

  def latest_dividend_for(self, symbol):
    history = self.dividend_history_for(symbol)
    history.sort(key=lambda x: x['payable_date'], reverse=True)
    return mit.first(history, default=None)
