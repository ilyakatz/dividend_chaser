from celery import Celery
from celery.schedules import crontab
import sys
import os

from dividend_chaser.workers.all_dividends_worker import AllDividendsWorker
from dividend_chaser.workers.dividend_history import DividendHistory
import dividend_chaser.settings

REDIS_URL = os.getenv("REDIS_URL") or "localhost:6379"

app = Celery('hello', broker=f"redis://{REDIS_URL}//")
app.conf.timezone = 'America/Los_Angeles'


@app.task
def dividend_history_worker():
  """ https://en.wikipedia.org/wiki/List_of_public_REITs_in_the_United_States """
  for stock in ["STWD", "AIV", "PLYM", "OUT"]:
    print(f"Running worker for {stock}")
    DividendHistory(stock).dump()
  return True


@app.task
def reload_batch_worker(stocks):
  print(f"Running worker for {stocks}")
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
