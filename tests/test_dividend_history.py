from dividend_chaser.workers.dividend_history import DividendHistory
from dividend_chaser.models.dividendable import Dividendable

import datetime  
from freezegun import freeze_time
import datetime as dt
import re
import unittest
from unittest.mock import patch


def test_estimate_next_date(mocker):
  dh = DividendHistory([])
  res = [1523021400, 1531143000, 1539091800, 1547044200, 1554730200, 1562679000, 1570627800, 1578580200]
  mocker.patch.object(dh, '_dates', return_value=res, autospec=True)

  mocker.patch.object(dh, '_average_dividend_interval',
                      return_value=datetime.timedelta(days=91, seconds=74571, microseconds=428571), autospec=True)

  estimate = dh._estimate_next_date(datetime.date(2020, 1, 9), "STWD")

  assert estimate == datetime.datetime(2020, 4, 10, 3, 12, 51, 428571)


class TestUpcoming(unittest.TestCase):
  @freeze_time("2020-01-12 12:00:01")
  def test_limit_upcoming(self):

    dh = DividendHistory([])
    stocks = {
        "STWD": {
            "dividends": [
                {"date": 1577716200, "formatted_date": "2019-12-30", "amount": 0.48}
            ],
            "next_dividend": {
                "date": "2020-01-16 23:47:08.571429",
                "formatted_date": "2020-01-16"
            },
            "volatililty": 0.13605430659514575,
            "dividend_yield": 0.0773,
            "average_volume": 2000
        }
    }

    with patch.object(DividendHistory, 'loadStocks', return_value=stocks):
      res = dh.upcoming()

      self.assertEqual(len(res), 1)
      self.assertEqual(res[0].symbol, "STWD")

  @freeze_time("2020-01-16 12:00:01")
  def test_limit_upcoming_unmet(self):

    dh = DividendHistory([])
    stocks = {
        "STWD": {
            "dividends": [
                {"date": 1577716200, "formatted_date": "2019-12-30", "amount": 0.48}
            ],
            "next_dividend": {
                "date": "2020-01-16 23:47:08.571429",
                "formatted_date": "2020-01-16"
            },
            "volatililty": 0.13605430659514575,
            "dividend_yield": 0.0773,
            "average_volume": 20000
        }
    }

    with patch.object(DividendHistory, 'loadStocks', return_value=stocks):
      res = dh.upcoming()

      self.assertEqual(len(res), 0)

  @freeze_time("2020-01-12 12:00:01")
  def test_limit_upcoming_custom_day_limit(self):

    dh = DividendHistory([])
    stocks = {
        "STWD": {
            "dividends": [
                {"date": 1577716200, "formatted_date": "2019-12-30", "amount": 0.48}
            ],
            "next_dividend": {
                "date": "2020-01-17 23:47:08.571429",
                "formatted_date": "2020-01-17"
            },
            "volatililty": 0.13605430659514575,
            "dividend_yield": 0.0773,
            "average_volume": 20000
        },
        "PP": {
            "dividends": [
                {"date": 1577716200, "formatted_date": "2019-12-30", "amount": 0.48}
            ],
            "next_dividend": {
                "date": "2020-01-15 23:47:08.571429",
                "formatted_date": "2020-01-15"
            },
            "volatililty": 0.13605430659514575,
            "dividend_yield": 0.0773,
            "average_volume": 20000
        }
    }

    with patch.object(DividendHistory, 'loadStocks', return_value=stocks):
      res = dh.upcoming(limit_days=6)

      self.assertEqual(len(res), 1)
      self.assertEqual(res[0].symbol, "STWD")
