from dividend_chaser.workers.dividend_history import DividendHistory


class ReloadStockDatabaseWorker:
  # pylint: disable=R0903
  @classmethod
  def run(cls):
    stocks = list(DividendHistory.loadStocks().keys())
    index = stocks.index("GME")
    stocks = stocks[901:-1]
    for stock in stocks:
      print(f"Running worker for {stock}")
      DividendHistory(stock).dump()
    return True
