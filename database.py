from model import *
from peewee import *
from pandas import DataFrame
from alpaca_trade_api.rest import *
from alpaca_trade_api.rest import REST
import datetime

class Database:
  def __init__(self, proxy):
    self.proxy = proxy
    self.proxy.initialize(SqliteDatabase('prices.db'))
    self.proxy.connect()

  def getPricesByMonth(self, stock, date):
    start = 0 # get the first of the month
    end = 1 # get the last day of the month
    table = newPrices(stock)
    result = list(table.select().dicts().where(table.date >= start & table.date <= end))
    return result

  def splitPricesByMonth(self, stock):
    table = newPrices(stock)
    prices = list(table.select().dicts())
    result = {}

    for price in prices:
      date = datetime.datetime.fromisoformat(price['date'])
      year_month = (date.year, date.month)
      candle = {'day': date.day, 'open': price['open'], 'close': price['close'], 'high': price['high'], 'low': price['low']}
      if year_month in result:
        result[year_month].append(candle)
      else:
        result[year_month] = [candle]
      

    return result

  def loadPrices(self, prices, table):
    dates = [str(date) for date in prices['open'].keys()]
    for date in dates:
      table.create(date=date, open=prices['open'][date], close=prices['close'][date], high=prices['high'][date], low=prices['low'][date])

  def setupPrices(self, api, all_assets):
    self.proxy.create_tables([Info])
    Info.create(last_updated=datetime.datetime.now())
    for asset in all_assets:
      whole_data = None

      try:
        whole_data = api.get_bars(asset, TimeFrame.Day, "2019-09-01", "2021-09-01", adjustment='raw').df
      except:
        print("CANNOT GET ASSET:", asset)
        pass

      #print(asset, len(whole_data['open']))

      if isinstance(whole_data, DataFrame) and len(whole_data['open']) > 500:
        print("Loading prices for ", asset)
        table = newPrices(asset)
        self.proxy.create_tables([table])
        print(self.proxy.get_tables())
        self.loadPrices(whole_data, table)

  def updatePrices(self, api):
    assets = self.proxy.get_tables()
    assets.remove('info')

    print(assets  )

  def getPricesFromDB(self, stock):
    table = newPrices(stock)
    return list(table.select().dicts())