from dividend_chaser.workers.dividend_history import DividendHistory

import datetime  
from freezegun import freeze_time
import datetime as dt
import re


def test_estimate_next_date(mocker):
  dh = DividendHistory(None)
  res = [1523021400, 1531143000, 1539091800, 1547044200, 1554730200, 1562679000, 1570627800, 1578580200]
  mocker.patch.object(dh, '_dates', return_value=res, autospec=True)

  mocker.patch.object(dh, '_average_dividend_interval',
                      return_value=datetime.timedelta(days=91, seconds=74571, microseconds=428571), autospec=True)

  estimate = dh._estimate_next_date(datetime.date(2020, 1, 9))

  assert estimate == datetime.datetime(2020, 4, 10, 3, 12, 51, 428571)
