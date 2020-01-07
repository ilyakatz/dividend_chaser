from dividend_chaser.models.position import Position
from dividend_chaser.models.dividendable import Dividendable
from dividend_chaser.chaser import Chaser

import datetime  
from freezegun import freeze_time
import datetime as dt
import re

with freeze_time('2020-01-06'):
  broker = None
  dividendable = Dividendable("AGNC", "2020-01-07", "0.01", 0.11)
  chaser = Chaser(broker)
  position = Position("APPLE", broker)

  def test_next_dividend_too_far_away(mocker):
    dividendable = Dividendable("AGNC", "2020-01-29", "0.01", 0.11)
    mocker.patch.object(position, 'time_to_next_dividend', return_value=datetime.timedelta(days=8), autospec=True)

    res = chaser._should_exchange(position, dividendable)

    assert res.result == False
    assert re.search('14 days EARLIER', res.reasons)

  def test_next_dividend_closer_than_current(mocker):
    mocker.patch.object(position, 'time_to_next_dividend', return_value=datetime.timedelta(days=8), autospec=True)

    res = chaser._should_exchange(position, dividendable)

    assert res.result == True
    assert re.search('8 days LATER', res.reasons)
