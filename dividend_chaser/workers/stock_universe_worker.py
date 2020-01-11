from datetime import date, timedelta
import json
import os
import dirtyjson
import requests 
import numpy as np

"""
Example
-------

from dividend_chaser.workers.stock_universe_worker import StockUniverseWorker
StockUniverseWorker.dump()

"""


class StockUniverseWorker:
  data_dir = 'data/'
  filename = f"{data_dir}/stocks.json"
  url = 'https://www.thestreet.com/util/divs.jsp'
  """ Worker responsible for analyzing the whole universe of stocks with dividends
  """

  @classmethod
  def dump(cls, start_date="2019-01-01", end_date="2019-12-31"):
    """ 
    Returns
    -------
    List of all stocks written to file
    """
    print(f"Writing to {StockUniverseWorker.filename}")
    stocks = StockUniverseWorker().get_all_dividends(start_date, end_date)
    stocks = list(np.unique(stocks))
    if not os.path.exists(StockUniverseWorker.data_dir):
      os.makedirs(StockUniverseWorker.data_dir)
    with open(StockUniverseWorker.filename, 'w') as fp:
      json.dump(stocks, fp)

    return stocks

  def get_all_dividends(self, start, end):
    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)

    d = start_date
    stocks = []
    while d < end_date:
      stocks = stocks + self._get_dividend_stocks_for_date(d)
      d = d + timedelta(days=1)

    return stocks

  def _get_dividend_stocks_for_date(self, target_date: date):
    date_str = target_date.strftime("%m_%d_%Y")
    url = f"{StockUniverseWorker.url}?date={date_str}"
    r = requests.get(url=url)     
    content = r.content.decode("utf-8") 

    stocks = []
    print(f"Date: {date_str}")
    if(content == ""):
      print("No dividends")
    else:
      parsed = dirtyjson.loads(content)
      results = parsed.get("results")
      for obj in results:
        symbol = obj.get("symbol")
        stocks.append(symbol)

    return stocks
