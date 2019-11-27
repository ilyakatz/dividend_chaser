```
pip3 install virtualenv
source dividends_chaser/bin/activate
pip install -r requirements.txt
```

## Running

```
export USER_NAME="some user"
export PASSWORD="somepassword"
```

## Worker jobs

```
celery -A tasks worker --loglevel=info
flower -A tasks --port=5555
```

### Scheduling a job

```
from tasks import dividend_history_worker
dividend_history_worker.delay()
```
