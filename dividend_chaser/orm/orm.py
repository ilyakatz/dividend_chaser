import os
from orator.orm import belongs_to
from orator import Model
from orator import DatabaseManager
from orator.orm import has_many

# pylint: disable=W0611
import dividend_chaser.settings

environment = os.environ['ENVIRONMENT']

if(environment == "development"):
  from dividend_chaser.config.database import DATABASES
elif(environment == "test"):
  from dividend_chaser.config.database_test import DATABASES

db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)


class Dividend(Model):
  __fillable__ = ['date', 'formatted_date', 'amount', 'dividendable_id']

  @belongs_to
  def dividendable(self):
    return Dividendable

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return f"""<Dividend \
date={self.date} \
formatted_date={self.formatted_date} \
amount={self.amount} \
dividendable_id={self.dividendable_id} \
/>"""


class Dividendable(Model):
  __fillable__ = ['symbol', 'volatililty', 'dividend_yield',
                  'next_dividend_actual', 'average_volume', 'next_dividend_date', 'next_dividend_formatted_date']

  @has_many
  def dividends(self):
    return Dividend

  def __str__(self):
    # pylint: disable=R0801
    return self.__repr__()

  def __repr__(self):
    # pylint: disable=R0801
    return f"""<Dividedable \
symbol={self.symbol} \
volatililty={self.volatililty} \
dividend_yield={self.dividend_yield} \
next_dividend_actual={self.next_dividend_actual} \
average_volume={self.average_volume} \
next_dividend_date={self.next_dividend_date} \
/>"""
