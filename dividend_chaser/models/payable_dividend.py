import datetime
from typing import Union

class PayableDividend:
  def __init__(self, symbol: str, state: Union["pending","paid"], amount: float, payable_date: datetime.datetime.date):
    self.symbol=symbol
    self.state=state
    self.amount=amount
    self.payable_date=payable_date


  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return f"<PayableDividend symbol={self.symbol} state={self.state} amount={self.amount} payable_date={self.payable_date} >"