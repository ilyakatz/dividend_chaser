from abc import ABC, abstractmethod

class AbstractBroker(ABC):
  @abstractmethod
  def get_current_price(self, symbol):
    pass