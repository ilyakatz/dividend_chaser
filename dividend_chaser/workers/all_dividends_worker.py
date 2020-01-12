import sys
import json
import numpy as np

from dividend_chaser.workers.dividend_history import DividendHistory


class AllDividendsWorker:
  filename = "data/stocks.json"
  @classmethod
  def dump(cls):
    reits = ["STWD", "AIV", "PLYM", "OUT", "VER", "AGNC", "WPC", "VICI", "MPW", "RWT", "IRM", "LAMR", "AVB", "CPT",
             "EQR", "ESS", "MAA", "UDR", "COR", "CONE", "DLR", "EQIX", "QTS", "ALX", "CUZ", "EPR", "AB", "WMC", "UHT"]
    additional_reits = ["NHI", "VTR", "WELL", "HTA"]
    funds = ["MAIN"]

    with open(AllDividendsWorker.filename) as file:
      all_stocks = json.load(file)

    stocks = all_stocks
    stocks = list(np.unique(stocks))

    """ https://en.wikipedia.org/wiki/List_of_public_REITs_in_the_United_States """
    for stock in stocks:
      print(f"Running worker for {stock}")
      DividendHistory(stock).dump()
    return True
