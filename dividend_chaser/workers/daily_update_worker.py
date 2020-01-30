import datetime
from tasks import reload_batch_worker

from dividend_chaser.orm import orm


class DailyUpdateWorker:
  # pylint: disable=R0903
  @classmethod
  def run(cls):
    time_now = int(datetime.datetime.now().strftime('%s'))
    records = orm.Dividendable.where_raw(f"next_dividend_actual IS false OR next_dividend_date < {time_now}").get()
    stocks = list(map(lambda x: x.symbol, records))
    chunk_size = 5
    for i in range(0, len(stocks), chunk_size):
      chunk = stocks[i:i + chunk_size]
      reload_batch_worker.delay(chunk)

    return True
