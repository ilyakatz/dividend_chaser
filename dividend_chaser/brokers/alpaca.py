import os
import alpaca_trade_api as tradeapi

from dividend_chaser.brokers.abstract_broker import AbstractBroker
from dividend_chaser.models.position import Position

CLIENT_ID = os.getenv("ALPACA_CLIENT_ID")
CLIENT_SECRET = os.getenv("ALPACA_CLIENT_SECRET")
ALPACA_URL = os.getenv("ALPACA_URL")

# account = api.get_account()
# api.list_positions()


class Broker(AbstractBroker):
  def __init__(self, dry_run=True):
    self.login = None
    self.api = None
    self.dry_run = dry_run

  def get_current_price(self, symbol):
    return None

  def _login_required(function):
    def auth(self, *args, **kwargs):
      if(not self.api):
        self.api = tradeapi.REST(CLIENT_ID, CLIENT_SECRET, ALPACA_URL, api_version='v2')  # or use ENV Vars shown below

      return function(self, *args, **kwargs)
    return auth

  @_login_required
  def broker(self):
    return self.api

  @_login_required
  def positions(self):
    positions = {}
    broker = self
    alpaca_positions = self.api.list_positions()
    for position in alpaca_positions:
      pos = Position(symbol=position.symbol, bought_price=float(position.avg_entry_price), broker=broker)
      positions[position.symbol] = pos
    return positions

  @_login_required
  def get_dividends(self):
    return []

  @_login_required
  def buy(self, symbol, amount):
    return []

  def sell_all(self, symbol):
    return symbol

  def exchange(self, old_symbol, new_symbol):
    return old_symbol == new_symbol
