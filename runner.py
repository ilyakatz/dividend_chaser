#!/usr/bin/env python
from chaser import Chaser
from brokers.robinhood import Broker
import os
import logging
import sys

if __name__ == '__main__':

  root = logging.getLogger()
  root.setLevel(logging.INFO)

  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.INFO)

  # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  formatter = logging.Formatter('%(levelname)s - %(message)s')
  handler.setFormatter(formatter)

  root.addHandler(handler)

  broker = Broker(os.environ["USER_NAME"], os.environ["PASSWORD"])
  chaser = Chaser(broker)
  chaser.run()

"""
from chaser import Chaser
from brokers.robinhood import Broker
from models.position import REIT 
import os

broker = Broker(os.environ["USER_NAME"], os.environ["PASSWORD"])

r = REIT("STWD", broker)
r.is_allowed_to_sell()     
"""
