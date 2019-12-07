import robin_stocks
from yahoofinancials import YahooFinancials
import pprint
from brokers.abstract_broker import AbstractBroker

pp = pprint.PrettyPrinter(indent=4)

THREADSHOLD =  0.5

class REIT:
  """Object that representation an instance of an REIT and operations that can be take on it
  """
  def __init__(self, symbol, broker: AbstractBroker):
    self.symbol=symbol
    self.bought_price=None
    self.broker=broker
    self.current_price=None
    self.details=None

  def get_details(self):
    my_stocks = self.broker.positions()
    for key,value in my_stocks.items():
      if(key==self.symbol):
        self.bought_price=float(value['average_buy_price'])
        print(f"Bought {key} for ${self.bought_price}")
    self.get_current_price()

  def _details_required(function):
    def details(self, *args, **kwargs) :
      if(self.details==None):
        print("Getting details")
        self.details=self.get_details()
      
      return function(self, *args, **kwargs)
    return details

  @_details_required
  def is_allowed_to_sell(self):
    """Returns an indication that the current stock can be sold.

    A stock can be sold if it's current price is greater than the 
    price at which it was bought within a certain range

    Returns
    -------
    boolean
      True or False indicating that this stock can be sold
    """
    return ( self.current_price - self.bought_price ) > 0-THREADSHOLD

  def get_current_price(self):
    self.current_price=self.broker.get_current_price(self.symbol)
    current_price=self.broker.get_current_price(self.symbol)
    print(f"Current price ${current_price}")
