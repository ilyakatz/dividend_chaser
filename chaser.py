
import robin_stocks as r
from reit import REIT

class Chaser:
  def __init__(self, username, password):
    self.username=username
    self.password=password
    self.login=None

  def reits(self):
    return ["STWD"]

  def _login_required(function):
    def auth(self, *args, **kwargs) :
      if(self.login==None):
        print("Logging in")
        self.login = r.login(self.username, self.password)
      
      function(self, *args, **kwargs)
    return auth

  @_login_required
  def broker(self):
    return r

  @_login_required
  def positions(self):
    my_stocks = r.build_holdings()
    for key,value in my_stocks.items():
      if(key in self.reits()):
        print(key)
        reit = REIT(key, self)
        reit.get_details()
