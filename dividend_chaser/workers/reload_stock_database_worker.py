from dividend_chaser.workers.dividend_history import DividendHistory


class ReloadStockDatabaseWorker:
  # pylint: disable=R0903
  @classmethod
  def run(cls):
    stocks = list(DividendHistory.loadStocks().keys())
    index = stocks.index("HMC")
    stocks = stocks[index:-1]

    chunk_size = 50
    for i in range(0, len(stocks), chunk_size):
      chunk = stocks[i:i + chunk_size]
      print(f"Running worker for {chunk}")
      DividendHistory(chunk).dump()

    return True
