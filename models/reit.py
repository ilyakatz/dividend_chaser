import robin_stocks
from yahoofinancials import YahooFinancials
import pprint

pp = pprint.PrettyPrinter(indent=4)

class REIT:
  THREADSHOLD: 0.5
  """Object that representation an instance of an REIT and operations that can be take on it
  """
  def __init__(self, symbol, broker):
    self.symbol=symbol
    self.bought_price=None
    self.broker=broker
    self.current_price=None

  def get_details(self):
    my_stocks = robin_stocks.build_holdings()
    for key,value in my_stocks.items():
      if(key==self.symbol):
        self.bought_price=value['average_buy_price']
        print(f"Bought {key} for ${self.bought_price}")
    self.get_current_price()

  def is_allowed_to_sell(self):
    """Returns an indication that the current stock can be sold.

    A stock can be sold if it's current price is greater than the 
    price at which it was bought within a certain range

    Returns
    -------
    boolean
      True or False indicating that this stock can be sold
    """
    return ( self.current_price - self.bought_price ) > -THREADSHOLD 

  def get_current_price(self):
    self.current_price=self.broker.get_current_price(self.symbol)
    current_price=self.broker.get_current_price(self.symbol)
    print(f"Current price ${current_price}")
