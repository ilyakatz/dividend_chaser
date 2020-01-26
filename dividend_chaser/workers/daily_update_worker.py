from tasks import reload_batch_worker
from dividend_chaser.orm import orm


class DailyUpdateWorker:
  # pylint: disable=R0903
  @classmethod
  def run(cls):
    records = orm.Dividendable.where_raw("next_dividend_actual IS false").get()
    stocks = list(map(lambda x: x.symbol, records))
    chunk_size = 5
    for i in range(0, len(stocks), chunk_size):
      chunk = stocks[i:i + chunk_size]
      reload_batch_worker.delay(chunk)

    return True
