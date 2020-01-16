![Dividend Chaser](./assets/chaser_logo.png)

```
pip3 install virtualenv
virtualenv dividends_env
source dividends_env/bin/activate
pip install -r requirements.txt
```

## Running

```
export USER_NAME="some user"
export PASSWORD="somepassword"
```

### Run the main process

```
python ./runner.py
```

#### Example

```
% python3 ./runner.py                                                                                                                                                                                  ✹ ✭
INFO - Logging in to Robinhood 🏹
INFO - ---START STWD---
INFO - Getting details
INFO - Bought STWD for $24.26
INFO - Current price $24.81
INFO - Time to next dividend 18 days, 23:52:18.491797
INFO - Upcoming dividends [<Dividedable symbol=MAIN dividend_date=2019-12-16 >, <Dividedable symbol=VICI dividend_date=2019-12-26 >, <Dividedable symbol=STWD dividend_date=2019-12-27 >, <Dividedable symbol=PLYM dividend_date=2019-12-27 >, <Dividedable symbol=VER dividend_date=2019-12-27 >, <Dividedable symbol=AGNC dividend_date=2019-12-27 >, <Dividedable symbol=WPC dividend_date=2019-12-27 >, <Dividedable symbol=AIV dividend_date=2020-02-13 >]
INFO - Proposal: Sell STWD, Buy MAIN
INFO - ---END STWD---

INFO - ---START MPW---
INFO - Getting details
INFO - Bought MPW for $20.68
INFO - Current price $21.27
INFO - Time to next dividend 2 days, 15:52:13.699454
INFO - Not ready to sell
 ['Next dividend is only 2 days away (less than 5) ']
INFO - ---END MPW---
```

### Worker jobs

```
celery -A tasks worker --loglevel=debug --concurrency=1
flower -A tasks --port=5555
```

#### Commands

```
celery -A tasks purge -f
```

#### Update stock universe data

```
from dividend_chaser.workers.stock_universe_worker import StockUniverseWorker
StockUniverseWorker.dump()
```

### Scheduling a job

```
from tasks import dividend_history_worker
dividend_history_worker.delay()
```

### Notebook

```
ipython kernel install --user --name=dividends_env
jupyter notebook
```

## Linting

```
autopep8 --in-place --recursive --exclude=dividends_env .

```

## Robinhood

Want to do your own automated trading? Use my referal link to sign up for [Robinhood](https://join.robinhood.com/ilyak36)
