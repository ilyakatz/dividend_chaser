from abc import ABC, abstractmethod
from typing import List

from dividend_chaser.models.payable_dividend import PayableDividend
from dividend_chaser.types import PositionsDict

class AbstractBroker(ABC):

  @abstractmethod
  def positions(self) -> PositionsDict:
    pass

  @abstractmethod
  def get_current_price(self, symbol) -> float:
    pass

  """ Returns all known dividends pay to the account
  """
  @abstractmethod
  def dividend_history_for(self, symbol: str) -> List[PayableDividend]:
    pass

  @abstractmethod
  def buy(self, symbol, amount):
    pass

  @abstractmethod
  def sell_all(self, symbol):
    pass
