from tasks import reload_batch_worker
from dividend_chaser.workers.dividend_history import DividendHistory


class ReloadStockDatabaseWorker:
  # pylint: disable=R0903
  @classmethod
  def run(cls):

    stocks = list(DividendHistory.loadStocks().keys())
    chunk_size = 5
    for i in range(0, len(stocks), chunk_size):
      chunk = stocks[i:i + chunk_size]
      reload_batch_worker.delay(chunk)

    return True
