import robin_stocks as r
from models.reit import REIT
from brokers.abstract_broker import AbstractBroker 

class Broker(AbstractBroker):
  def __init__(self, username, password):
    self.username=username
    self.password=password
    self.login=None

  def _login_required(function):
    def auth(self, *args, **kwargs) :
      if(self.login==None):
        print("Logging in")
        self.login = r.login(self.username, self.password)
      
      return function(self, *args, **kwargs)
    return auth

  @_login_required
  def get_current_price(self, symbol):
    data = r.stocks.get_quotes(symbol)
    current_price=data[0]['last_trade_price']
    price = float(current_price)
    return price

  @_login_required
  def broker(self):
    return r

  @_login_required
  def positions(self):
    my_stocks = r.build_holdings()
    return my_stocks