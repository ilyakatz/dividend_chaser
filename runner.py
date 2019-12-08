#!/usr/bin/env python
from chaser import Chaser
from brokers.robinhood import Broker
import os

if __name__ == '__main__':
    broker = Broker(os.environ["USER_NAME"], os.environ["PASSWORD"])
    chaser = Chaser(broker)
    chaser.run()

"""
from chaser import Chaser
from brokers.robinhood import Broker
from models.reit import REIT 
import os

broker = Broker(os.environ["USER_NAME"], os.environ["PASSWORD"])

r = REIT("STWD", broker)
r.is_allowed_to_sell()     
"""