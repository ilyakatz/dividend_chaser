import logging

"""
TODO: change symbol/quantity to variable args
"""


def do_if_enabled(dry_run, symbol, quantity, func): 
  if(not dry_run):
    result = func(symbol, quantity)
  else:
    logging.info("Not Executing in Dry Run Mode")
    result = None
  return result
