import logging
import math
import robin_stocks as r
import more_itertools as mit

from dividend_chaser.brokers.abstract_broker import AbstractBroker
from dividend_chaser.helpers.functions import do_if_enabled
from dividend_chaser.models.position import Position
from dividend_chaser.types import PositionsDict


class Broker(AbstractBroker):
  def __init__(self, username, password, dry_run=True):
    self.username = username
    self.password = password
    self.login = None
    self.dry_run = dry_run

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
  def positions(self) -> PositionsDict:
    positions = {}
    broker = self
    robin_positions = r.build_holdings()
    for symbol in robin_positions:
      value = robin_positions[symbol]
      pos = Position(symbol=symbol, bought_price=float(value['average_buy_price']), broker=broker)
      positions[symbol] = pos

    return positions

  @_login_required
  def get_dividends(self):
    return self.broker().account.get_dividends()

  @_login_required
  def buy(self, symbol, amount):
    current_price = self.get_current_price(symbol)
    logging.info(f"Current price for {symbol} is {current_price}")

    # Approximate quantity that we can afford to buy
    quantity = math.floor(amount / current_price)
    logging.info(f"Will buy {quantity} shares")

    do_if_enabled(self.dry_run, symbol, quantity, lambda symbol, quantity: self._buy(symbol, quantity))

  def _buy(self, symbol, quantity):
    logging.info(f"Buying {symbol} - {quantity}")
    data = self.broker().orders.order_buy_market(symbol, quantity)
    ref_id = data['ref_id']
    logging.info(f"Data is {data}")
    if(ref_id):
      logging.info(f"Executed: ref_id {ref_id}")
      return ref_id

    return None

  def sell_all(self, symbol):
    """Request to sell all for the given symbol

    Returns
    --------
    Float | None
      Estimated amount from sold position if sale is possible, else, None
    """
    current_positions = self.positions()
    position = current_positions[symbol]
    quantity = float(position['quantity'])
    equity = do_if_enabled(self.dry_run, symbol, quantity, lambda symbol, quantity: self._sell(symbol, quantity))
    return (equity or 0)

  def exchange(self, old_symbol, new_symbol):
    """
    Because sell orders may not be executed right away,
    before buying, we need to make sure we have enough cash in the account
    """
    equity = self.sell_all(old_symbol)
    self.buy(new_symbol, equity)

  def _sell(self, symbol, quantity):
    logging.info(f"Selling {quantity} of {symbol}")
    # trigger sale order
    data = self.broker().orders.order_sell_market(symbol, quantity)
    price = float(data['price'])
    equity = price * quantity

    # since this is a market order and result are not instaneous
    # this is an estimated amout of equity that will be returned once transaction is
    # completed
    return equity

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
