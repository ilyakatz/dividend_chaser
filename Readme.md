![Dividend Chaser](./assets/chaser_logo.png)

### Install prerequisites

```
brew install openssl
pip3 install virtualenv
virtualenv dividends_env
source dividends_env/bin/activate
pip install -r prod.txt
```

### Create database

```
createdb dividend_chaser_development
orator migrate -c database.yml
```

## Running

```
export IEX_TOKEN="token"
export USER_NAME="some user"
export PASSWORD="somepassword"
export ENVIRONMENT=development
```

### Run the main process

```
python ./runner.py
```

### Tests

```
orator migrate -c database.test.yml -f
ENVIRONMENT=test pytest
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

### Background Processing

To start workers and monitoring

```
supervisord -c supervisord.conf
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

## Models

Create new model

```
orator make:model User -m
```

Migrate

```
orator migrate -c database.yml
```

## Debugging

```
brew cask install postico
```

## Docker

### Start up docker env

```
eval $(docker-machine env default)
```

### Build the image

```
 docker build . -t dividend_chaser
```

### Run it

```
docker run -p 8080:5555 -it dividend_chaser
```

### Debug it

```
docker run -it dividend_chaser /bin/bash
```
