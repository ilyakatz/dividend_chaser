from dividend_chaser.models.position import Position
from dividend_chaser.models.dividendable import Dividendable
from dividend_chaser.chaser import Chaser
from dividend_chaser.workers.dividend_history import DividendHistory

import datetime  
from freezegun import freeze_time
import datetime as dt
import re

broker = None
dividendable = Dividendable("AGNC", "2020-01-07", "0.01", 0.11, 2000)
chaser = Chaser(broker)
position = Position("APPLE", broker)

positions_dic = {
    'MAA':
    {'price': '132.240000', 'quantity': '3.00000000', 'average_buy_price': '130.5000', 'equity': '396.72', 'percent_change': '1.33', 'equity_change': '5.220000',
     'type': 'reit', 'name': 'Mid-America Apartment Communities', 'id': '1d8c69f9-4835-45c7-852f-a8cc163f29fd', 'pe_ratio': '56.308000', 'percentage': '6.87'},
    'UDR':
    {'price': '46.060000', 'quantity': '22.00000000', 'average_buy_price': '45.8600', 'equity': '1013.32', 'percent_change': '0.44',
     'equity_change': '4.400000', 'type': 'reit', 'name': 'UDR', 'id': '36396dd5-d024-45a3-be64-aec99317aba7', 'pe_ratio': '76.724700', 'percentage': '17.56'}
}


@freeze_time("2020-01-06 12:00:01")
def test_next_dividend_too_far_away(mocker):
  dividendable = Dividendable("AGNC", "2020-01-29", "0.01", 0.11, 2000)
  mocker.patch.object(position, 'time_to_next_dividend', return_value=datetime.timedelta(days=8), autospec=True)

  res = chaser._should_exchange(position, dividendable)

  assert res.result == False
  assert re.search('14 days EARLIER', res.reasons)


@freeze_time("2020-01-06 12:00:01")
def test_next_dividend_closer_than_current(mocker):
  mocker.patch.object(position, 'time_to_next_dividend', return_value=datetime.timedelta(days=8), autospec=True)

  res = chaser._should_exchange(position, dividendable)

  assert res.result == True
  assert re.search('8 days LATER', res.reasons)


def test_next_stock_does_not_include_existing(mocker):
  """ Next stock should not be one of the stock that is already bought
  """

  broker = mocker.Mock()
  chaser = Chaser(broker)

  upcoming = [
      Dividendable("MAA", "2020-01-28", 0.0830, 0.24804521107634905, 2000),
      Dividendable("AGNC", "2020-01-29", 0.108, 0.13090305500556784, 2000),
      Dividendable("EPR", "2020-01-29", 0.064, 0.1714829852718327, 200),
  ]

  mocker.patch.object(broker, 'positions', return_value=positions_dic)
  mocker.patch.object(DividendHistory, 'upcoming', return_value=upcoming)
  next_one = chaser._next_stock()

  assert next_one.symbol == "AGNC"


def test_threshold(mocker):
  """ Filter out all stocks that have a very high violatility index
  """

  broker = mocker.Mock()
  chaser = Chaser(broker)

  upcoming = [
      Dividendable("HIGH", "2020-01-28", 1, 0.24804521107634905, 2000),
      Dividendable("LOW", "2020-01-28", 1, 0.13090305500556784, 2000),
      Dividendable("EPR", "2020-01-29", 1, 0.1714829852718327, 2000),
  ]

  mocker.patch.object(broker, 'positions', return_value=positions_dic)
  mocker.patch.object(DividendHistory, 'upcoming', return_value=upcoming)
  next_one = chaser._next_stock()

  assert next_one.symbol == "LOW"
