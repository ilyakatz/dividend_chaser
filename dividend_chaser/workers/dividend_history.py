import json
import datetime
import logging
from json import JSONDecodeError
from yahoofinancials import YahooFinancials

from dividend_chaser.models.dividendable import Dividendable
from dividend_chaser.services.yahoo_data_service import YahooDataService
# from dividend_chaser.services.iexcloud_service import IExcloudService

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
    stocks = DividendHistory.loadStocks()
    arr = list(stocks.items())
    simplified = list(map(lambda x: Dividendable(
        x[0],
        x[1]['next_dividend']['formatted_date'],
        x[1]['dividend_yield'],
        x[1]['volatililty'],
        x[1].get('average_volume'),
        x[1]['next_dividend'].get('actual')), arr))

    simplified = list(filter(lambda d: d.dividend_date.date() < (
        datetime.date.today() + datetime.timedelta(days=limit_days)), simplified))

    simplified.sort(key=lambda x: x.dividend_date, reverse=False)
    simplified = list(filter(lambda d: d.actual == True, simplified))

    filtered = list(
        filter(lambda dividendable: dividendable.is_clearable(), simplified))

    return filtered

  @classmethod
  def load_from_db(cls):
    try:
      with open(DividendHistory.filename) as file:
        obj = json.load(file)
    except JSONDecodeError:
      obj = {
      }
    return obj

  def load(self):
    obj = DividendHistory.load_from_db()

    for symbol in self.symbols:
      if(symbol not in obj):
        obj[symbol] = {}

    return obj

  def dump(self):
    # pylint: disable=W0702
    divs = self._get_dividends(self.symbols)
    for symbol in self.symbols:
      self.dividends_data[symbol]["dividends"] = divs[symbol]

    # try:
    self._enrich(self.symbols, self.dividends_data)
    logging.info(f"Dumping data for {self.symbols}")
    with open(self.filename, 'w') as fp:
      # json.dump(self.dividends_data, fp)
      pretty = json.dumps(self.dividends_data, indent=2)
      fp.write(pretty)
    # except:
    #   print("Exception:")
    #   print('-' * 60)
    #   traceback.print_exc(file=sys.stdout)
    #   print('-' * 60)

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
    " TODO maybe can use get_exdividend_date "
    data = DividendHistory.load_from_db()
    new_date = data[symbol]['next_dividend']['formatted_date']
    return datetime.date.fromisoformat(new_date)

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
