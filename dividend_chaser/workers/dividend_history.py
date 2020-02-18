import json
import datetime
import logging
from json import JSONDecodeError
from yahoofinancials import YahooFinancials

from dividend_chaser.models.dividendable import Dividendable
from dividend_chaser.services.yahoo_data_service import YahooDataService
from dividend_chaser.orm import orm

"""Class responsible for maintaining dividend history

DividendHistory retrieves and stores dividend history for
desires instruments. History is stored in json file for
easy retrieval
"""


class DividendHistory:
  filename = 'dividends.json'

  def __init__(self, symbols):
    self.symbols = symbols
    self.filename = 'dividends.json'
    self.dividends_data = self.load()

  @classmethod
  def loadStocks(cls):
    with open(DividendHistory.filename) as file:
      obj = json.load(file)
      return obj

  """ Finds the candidates for positions that have upcoming dividends

  Parameters
  ----------
  limit_days: int
     Limit to number of days in the future of when the next dividend is expected

  Returns
  -------
  Array[Dividendable]
  """
  @classmethod
  def upcoming(cls, limit_days=14):

    arr = orm.Dividendable.where("average_volume", ">", "100000").where("next_dividend_actual", "=", True).get()

    simplified = list(map(lambda x: Dividendable(
        x.symbol,
        x.next_dividend_formatted_date,
        x.dividend_yield,
        x.volatililty,
        x.average_volume,
        x.next_dividend_actual), arr))

    simplified = list(filter(lambda d: d.dividend_date.date() < (
        datetime.date.today() + datetime.timedelta(days=limit_days)), simplified))

    simplified.sort(key=lambda x: x.dividend_date, reverse=False)

    filtered = list(
        filter(lambda dividendable: dividendable.is_clearable(), simplified))

    return filtered

  @classmethod
  def load_from_file(cls):
    try:
      with open(DividendHistory.filename) as file:
        obj = json.load(file)
    except JSONDecodeError:
      obj = {
      }
    return obj

  def load(self):
    obj = DividendHistory.load_from_file()

    for symbol in self.symbols:
      if(symbol not in obj):
        obj[symbol] = {}

    return obj

  def dump(self):
    # pylint: disable=W0702
    divs = self._get_dividends(self.symbols)
    for symbol in self.symbols:
      self.dividends_data[symbol]["dividends"] = divs[symbol]

    self._enrich(self.symbols, self.dividends_data)
    logging.info(f"Dumping data for {self.symbols}")

    for symbol in self.symbols:
      self._persist_dividend_data(symbol, self.dividends_data)

    with open(self.filename, 'w') as fp:
      pretty = json.dumps(self.dividends_data, indent=2)
      fp.write(pretty)

  def _persist_dividend_data(self, symbol, dividends_data):
    params = dividends_data[symbol].copy()
    params["symbol"] = symbol
    params["next_dividend_actual"] = params["next_dividend"]["actual"]
    params["next_dividend_date"] = params["next_dividend"]["date"]
    params["next_dividend_formatted_date"] = params["next_dividend"]["formatted_date"]

    d = orm.Dividendable.first_or_create(symbol=symbol)
    d.update(params)

    for dividend_dict in params['dividends']:
      orm.Dividend.first_or_create(
          date=str(dividend_dict["date"]),
          formatted_date=dividend_dict["formatted_date"],
          amount=dividend_dict["amount"],
          dividendable_id=d.id
      )

  def _enrich(self, symbols, dividends_data):
    logging.debug("Starting _enrich")
    self._enrich_with_volatililty(symbols, dividends_data)
    # This is too slow
    self._enrich_with_volume(symbols, dividends_data)
    self._enrich_with_next_dividend(symbols, dividends_data)
    self._enrich_with_dividend_yield(symbols, dividends_data)
    logging.debug("Finished _enrich")

  """
  Returns
  _______
  dateime.date
  """

  @classmethod
  def next_dividend(cls, symbol):
    dividendable = orm.Dividendable.where("symbol", "=", symbol).first()
    new_upcoming_date = dividendable.next_dividend_date

    """ Accomodate the case where dividend has just passed
    In some cases, our database gets updated on the date of the dividend,
    So the system thinks that the next dividend is 30 days away, while
    in real life, it's today
    """
    two_days_ago = datetime.date.today() - datetime.timedelta(days=2)
    seconds = int(two_days_ago.strftime("%s"))

    dividend = orm.Dividend.where("date", ">=", seconds).first()
    if(dividend):
      return datetime.date.fromtimestamp(dividend.date)

    return datetime.date.fromtimestamp(new_upcoming_date)

  """
  Returns
  -------
  Hash[String: datetime.date]
  """

  def _enrich_with_next_dividend(self, symbols, dividends_data):
    # service = IExcloudService(symbols, dividends_data)
    service = YahooDataService(symbols, dividends_data)
    service.calculate_next_dividend()

    for symbol in symbols:
      self.dividends_data[symbol]["next_dividend"] = service.next_dividend(symbol)

  def _enrich_with_dividend_yield(self, symbols, dividends_data):
    service = YahooDataService(symbols, dividends_data)
    service.calculate_dividend_yield()

    for symbol in symbols:
      self.dividends_data[symbol]["dividend_yield"] = service.dividend_yield(symbol)

  def _enrich_with_volume(self, symbols, dividends_data):
    service = YahooDataService(symbols, dividends_data)
    service.calculate_average_volume()

    for symbol in symbols:
      self.dividends_data[symbol]["average_volume"] = service.average_volume(symbol)

  def _enrich_with_volatililty(self, symbols, dividends_data):
    service = YahooDataService(symbols, dividends_data)
    service.calculate_historical_volatility()

    for symbol in symbols:
      self.dividends_data[symbol]["volatililty"] = service.volatililty(symbol)

  def _get_dividends(self, symbols):
    start_date = '2018-01-15'
    d = datetime.datetime.today()
    end_date = d.strftime("%Y-%m-%d")
    yahoo_financials = YahooFinancials(symbols)
    divs = yahoo_financials.get_daily_dividend_data(start_date, end_date)

    return divs
