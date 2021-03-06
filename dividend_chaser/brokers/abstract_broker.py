from abc import ABC, abstractmethod


class AbstractBroker(ABC):

  @abstractmethod
  def positions(self):
    pass

  @abstractmethod
  def get_current_price(self, symbol):
    pass

  """ Returns all known dividends pay to the account
  """
  @abstractmethod
  def get_dividends(self):
    pass

  @abstractmethod
  def buy(self, symbol, amount):
    pass

  @abstractmethod
  def sell_all(self, symbol):
    pass
