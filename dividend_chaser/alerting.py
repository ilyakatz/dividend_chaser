import logging
import os
import sentry_sdk

# pylint: disable=W0611
import dividend_chaser.settings


def setup_alerting():
  SENTRY_URL = os.getenv("SENTRY_URL")
  if(SENTRY_URL):
    logging.info("Setting up Sentry")
    sentry_sdk.init(SENTRY_URL)
  else: 
    logging.info("Sentry is not enabled")
