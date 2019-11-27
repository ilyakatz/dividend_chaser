from celery import Celery
from workers.dividend_history import DividendHistory

app = Celery('hello', broker='redis://localhost:6379//')

"""

"""
@app.task
def dividend_history_worker():
    DividendHistory("STDW").dump()
    return true