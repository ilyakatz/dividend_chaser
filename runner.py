#!/usr/bin/env python
import logging
import os
import sys
import click

from dividend_chaser.brokers.robinhood import Broker
from dividend_chaser.chaser import Chaser


@click.command()
@click.option('--execute/--no-execute', required=True, help='Dry run mode - buy and sell orders are not executed')
def run(execute=False):
  dry_run = not execute
  broker = Broker(os.environ["USER_NAME"], os.environ["PASSWORD"], dry_run=dry_run)
  chaser = Chaser(broker)
  chaser.run()


if __name__ == '__main__':

  root = logging.getLogger()
  root.setLevel(logging.INFO)

  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.INFO)

  formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
  handler.setFormatter(formatter)

  root.addHandler(handler)
  run()


"""
from dividend_chaser.chaser import Chaser
from dividend_chaser.brokers.robinhood import Broker
from dividend_chaser.models.position import Position
import os
import logging
import sys

broker = Broker(os.environ["USER_NAME"], os.environ["PASSWORD"])
#broker = Broker(os.environ["USER_NAME"], os.environ["PASSWORD"],dry_run=False)

position = Position("STWD", broker)
position.is_allowed_to_sell()     

    
"""
