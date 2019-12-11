from abc import ABC, abstractmethod


class AbstractBroker(ABC):
  @abstractmethod
  def get_current_price(self, symbol):
    pass

  """ Returns all known dividends pay to the account
  """
  @abstractmethod
  def get_dividends(self):
    pass
