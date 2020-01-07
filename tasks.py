from celery import Celery
from celery.signals import celeryd_init

from dividend_chaser.workers.dividend_history import DividendHistory

app = Celery('hello', broker='redis://localhost:6379//')


@app.task
def dividend_history_worker():
  """ https://en.wikipedia.org/wiki/List_of_public_REITs_in_the_United_States """
  for stock in ["STWD", "AIV", "PLYM", "OUT"]:
    print(f"Running worker for {stock}")
    DividendHistory(stock).dump()
  return True


"""Run dividend refresh worker on celery startup
"""
@celeryd_init.connect
def dividend_history(conf=None, **kwargs):
  """ https://en.wikipedia.org/wiki/List_of_public_REITs_in_the_United_States """
  for stock in ["STWD", "AIV", "PLYM", "OUT", "VER", "AGNC", "WPC", "VICI", "MPW", "RWT", "IRM", "LAMR", "AVB", "CPT", "EQR", "ESS", "MAA", "UDR", "COR", "CONE", "DLR", "EQIX", "QTS", "ALX", "CUZ", "EPR", "AB", "WMC", "UHT"]:
    print(f"Running worker for {stock}")
    DividendHistory(stock).dump()
  return True
