import robin_stocks as r

class Chaser:
  def __init__(self, username, password):
    self.username=username
    self.password=password
    self.login=None

  def _login_required(function):
    def auth(self, *args, **kwargs) :
      if(self.login==None):
        print("Logging in")
        self.login = r.login(self.username, self.password)
      
      function(self, *args, **kwargs)
    return auth

  @_login_required
  def positions(self):
    print("#positions")