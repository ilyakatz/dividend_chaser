from tasks import reload_batch_worker
# from dividend_chaser.workers.dividend_history import DividendHistory
from dividend_chaser.workers.stock_universe_worker import StockUniverseWorker


class ReloadStockDatabaseWorker:
  # pylint: disable=R0903
  @classmethod
  def run(cls):
    stocks = StockUniverseWorker.loadStocks()
    # stocks = list(DividendHistory.loadStocks().keys())
    chunk_size = 5
    for i in range(0, len(stocks), chunk_size):
      chunk = stocks[i:i + chunk_size]
      reload_batch_worker.delay(chunk)

    return True
