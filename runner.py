#!/usr/bin/env python
import logging
import os
import sys

from dividend_chaser.brokers.robinhood import Broker
from dividend_chaser.chaser import Chaser

if __name__ == '__main__':

  root = logging.getLogger()
  root.setLevel(logging.INFO)

  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.INFO)

  formatter = logging.Formatter('%(levelname)s - %(message)s')
  handler.setFormatter(formatter)

  root.addHandler(handler)

  broker = Broker(os.environ["USER_NAME"], os.environ["PASSWORD"])
  chaser = Chaser(broker)
  chaser.run()

"""
from dividend_chaser.chaser import Chaser
from dividend_chaser.brokers.robinhood import Broker
from dividend_chaser.models.position import Position
import os

broker = Broker(os.environ["USER_NAME"], os.environ["PASSWORD"])
#broker = Broker(os.environ["USER_NAME"], os.environ["PASSWORD"],dry_run=False)

position = Position("STWD", broker)
position.is_allowed_to_sell()     
"""
