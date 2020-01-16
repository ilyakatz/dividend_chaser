import logging
import sys

from dividend_chaser.workers.reload_stock_database_worker import ReloadStockDatabaseWorker 

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
handler.setFormatter(formatter)

root.addHandler(handler)


ReloadStockDatabaseWorker.run() 
