import unittest
from unittest.mock import patch
from freezegun import freeze_time

from dividend_chaser.workers.dividend_history import DividendHistory
from dividend_chaser.orm import orm


class TestUpcoming(unittest.TestCase):

  def setUp(self):
    print("Cleaning up database")
    orm.Dividend.where("1", "=", "1").delete()
    orm.Dividendable.where("1", "=", "1").delete()

  @freeze_time("2020-01-12 12:00:01")
  def test_limit_upcoming_with_actual(self):
    """ Return only results that have actual dividends
    """

    dh = DividendHistory([])

    stocks = {
        "TRUE": {
            "dividends": [
                {"date": 1577716200, "formatted_date": "2019-12-30", "amount": 0.48}
            ],
            "next_dividend": {
                "date": "2020-01-16 23:47:08.571429",
                "formatted_date": "2020-01-16",
                "actual": True
            },
            "volatililty": 0.13605430659514575,
            "dividend_yield": 0.0773,
            "average_volume": 2000
        },
        "FALSE": {
            "dividends": [
                {"date": 1577716200, "formatted_date": "2019-12-30", "amount": 0.48}
            ],
            "next_dividend": {
                "date": "2020-01-16 23:47:08.571429",
                "formatted_date": "2020-01-16",
                "actual": False
            },
            "volatililty": 0.13605430659514575,
            "dividend_yield": 0.0773,
            "average_volume": 2000
        }
    }

    for stock in stocks:
      DividendHistory([])._persist_dividend_data(stock, stocks)

    res = dh.upcoming()

    self.assertEqual(len(res), 1)
    self.assertEqual(res[0].symbol, "TRUE")

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
                "formatted_date": "2020-01-16",
                "actual": True
            },
            "volatililty": 0.13605430659514575,
            "dividend_yield": 0.0773,
            "average_volume": 2000
        }
    }

    for stock in stocks:
      DividendHistory([])._persist_dividend_data(stock, stocks)

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
                "formatted_date": "2020-01-16",
                "actual": True
            },
            "volatililty": 0.13605430659514575,
            "dividend_yield": 0.0773,
            "average_volume": 20000
        }
    }

    for stock in stocks:
      DividendHistory([])._persist_dividend_data(stock, stocks)

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
                "formatted_date": "2020-01-17",
                "actual": True
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
                "formatted_date": "2020-01-15",
                "actual": True
            },
            "volatililty": 0.13605430659514575,
            "dividend_yield": 0.0773,
            "average_volume": 20000
        }
    }

    for stock in stocks:
      DividendHistory([])._persist_dividend_data(stock, stocks)

    res = dh.upcoming(limit_days=6)

    self.assertEqual(len(res), 1)
    self.assertEqual(res[0].symbol, "STWD")
