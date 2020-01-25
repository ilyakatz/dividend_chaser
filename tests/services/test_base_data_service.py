import unittest
from unittest.mock import patch
from freezegun import freeze_time
import datetime

from dividend_chaser.services.base_data_service import BaseDataService


class MockDataService(BaseDataService):
  def __init__(self, symbols):
    super().__init__(symbols, [])

  def _calculate_next_dividend(self, symbols):
    print("Not impplemented")


class TestNextDiv(unittest.TestCase):
  @freeze_time("2020-01-12 12:00:01")
  def test_valid_date(self):
    """ Handle valid dividend date scenario
    """

    service = MockDataService([])

    return_date_str = "2020-12-12"
    return_date = datetime.datetime.fromisoformat(return_date_str)
    with patch.object(service, '_estimate_next_date', return_value=return_date):

      data = {'STWD': return_date_str}
      res = service._next_div(data, "STWD")

      self.assertEqual(res['value'], return_date)
      self.assertEqual(res['actual'], True)

  def test_invalid_date(self):
    """ Handle invalid dividend date scenario
    """

    service = MockDataService([])

    return_date_str = "2012-12-12"
    return_date = datetime.date.fromisoformat(return_date_str)
    with patch.object(service, '_estimate_next_date', return_value=return_date):

      data = {'STWD': "-"}
      res = service._next_div(data, "STWD")

      self.assertEqual(res['value'], return_date)
      self.assertEqual(res['actual'], False)


class TestEstimateNextDate(unittest.TestCase):
  def test_not_enough_dates(self):
    """ Dividend history is too small
    """
    service = MockDataService([])
    dates = [1554384600]
    with patch.object(service, '_dates', return_value=dates):
      res = service._estimate_next_date(datetime.date(2019, 4, 3), "BOGUS")

      self.assertEqual(res, BaseDataService.EPOCH)
