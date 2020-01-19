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

    return_date = "2020-12-12"
    with patch.object(service, '_estimate_next_date', return_value=return_date):

      data = {'STWD': return_date}
      res = service._next_div(data, "STWD")

      self.assertEqual(res['value'], datetime.date.fromisoformat(return_date))
      self.assertEqual(res['actual'], True)

  def test_invalid_date(self):
    """ Handle invalid dividend date scenario
    """

    service = MockDataService([])

    return_date = "2012-12-12"
    with patch.object(service, '_estimate_next_date', return_value=return_date):

      data = {'STWD': "-"}
      res = service._next_div(data, "STWD")

      self.assertEqual(res['value'], return_date)
      self.assertEqual(res['actual'], False)
