#!/usr/bin/env python
from chaser import Chaser
from brokers.robinhood import Broker
import os

if __name__ == '__main__':
    broker = Broker(os.environ["USER_NAME"], os.environ["PASSWORD"])
    chaser = Chaser(broker)
    chaser.positions()