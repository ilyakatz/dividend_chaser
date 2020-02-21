from celery import Celery
from celery.schedules import crontab
import logging
import sys
import os

from dividend_chaser.workers.all_dividends_worker import AllDividendsWorker
from dividend_chaser.workers.dividend_history import DividendHistory
from dividend_chaser.alerting import setup_alerting
import dividend_chaser.settings

REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379"

app = Celery('hello', broker=f"{REDIS_URL}/0")
app.conf.timezone = 'America/Los_Angeles'
app.conf.redis_max_connections = 4

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
handler.setFormatter(formatter)

root.addHandler(handler)
setup_alerting()


@app.task
def dividend_history_worker():
  """ https://en.wikipedia.org/wiki/List_of_public_REITs_in_the_United_States """
  for stock in ["STWD", "AIV", "PLYM", "OUT"]:
    print(f"Running worker for {stock}")
    DividendHistory(stock).dump()
  return True


@app.task
def reload_batch_worker(stocks):
  print(f"Running reload_batch_worker for {stocks}")
  DividendHistory(stocks).dump()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  # Calls test('hello') every 10 seconds.
  # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

  # Calls test('world') every 30 seconds
  # sender.add_periodic_task(30.0, test.s('world'), expires=10)

  # Executes every Monday morning at 7:30 a.m.
  sender.add_periodic_task(
      crontab(hour=7, minute=30, day_of_week='mon-fri'),
      daily_update_worker.s(),
  )


@app.task
def daily_update_worker():
  from dividend_chaser.workers.daily_update_worker import DailyUpdateWorker
  print(f"Running daily update worker")
  DailyUpdateWorker.run()
