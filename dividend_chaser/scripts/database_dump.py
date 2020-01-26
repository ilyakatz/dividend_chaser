from dividend_chaser.workers.dividend_history import DividendHistory


def import_from_json_to_db():
  dividends_data = DividendHistory.load_from_file()

  for symbol in dividends_data.keys():
    # pylint: disable=W0212
    DividendHistory([])._persist_dividend_data(symbol, dividends_data)
