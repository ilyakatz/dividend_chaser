import robin_stocks
from yahoofinancials import YahooFinancials

pp = pprint.PrettyPrinter(indent=4)

class REIT:
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

  def get_current_price(self):
    data = robin_stocks.stocks.get_quotes("STWD")
    current_price=data[0]['last_trade_price']
    self.current_price=float(current_price)
    print(f"Current price ${self.current_price}")
