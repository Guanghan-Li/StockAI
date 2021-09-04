from timeit import *
import os, math, subprocess, time
import mplfinance as mpf
from alpaca_trade_api.rest import *
from alpaca_trade_api.rest import REST
from model import *
from peewee import *
from pandas import DataFrame
from calculations import Calculations
from report import Entry
from database import Database
from momentum import Momentum
from order import Order

database = Database(proxy)

start_time = time.time()

api = REST(
  'PK2QSUGIJOV6H5WSFCSH',
  'ta1nZJTKw1Ad8BM3OLUoqN1ApmwWSTXruxDtEsA0',
  'https://paper-api.alpaca.markets'
)

def getMonthlyByYear(year, monthly):
  result = []
  for date in monthly:
    if date[0] == year:
      result.append(monthly[date])
  
  return result

def getAllAssets():
  active_assets = api.list_assets(status='active')
  nasdaq_assets = [a.symbol for a in active_assets if a.exchange == 'NASDAQ']
  nyse_assets = [a.symbol for a in active_assets if a.exchange == 'NYSE']
  return nasdaq_assets+nyse_assets

def generateReport():
  all_stocks = proxy.get_tables()
  report = []

  for stock in all_stocks:
    #print('Getting ATR for ' + stock)
    prices = database.getPricesFromDB(stock)
    atr = round(Calculations.averageTrueRange(prices, 500), 2)
    close_price = prices[-1]['close']
    percent_atr = (atr / close_price) * 100

    monthly = database.splitPricesByMonth(stock)
    current_year = getMonthlyByYear(2021, monthly)
    prev_year = getMonthlyByYear(2020, monthly)

    current_momentum = Momentum.momentumOneYear(current_year)
    prev_momentum = Momentum.momentumOneYear(prev_year)
    acceleration = current_momentum - prev_momentum

    entry = Entry(stock, atr, percent_atr, current_momentum, prev_momentum, acceleration)
    report.append(entry)
  
  return report

def getOrders(report):
  report.sort(key=lambda entry: entry.acceleration, reverse = True)
  stocks = report[:20]
  stocks.sort(key=lambda entry: entry.current_momentum, reverse = True)

  stocks_to_order = []

  for stock in stocks[:5]:
    order = Order(stock.stock, 100, 'buy')

  return stocks_to_order

def buy(order):
  api.submit_order(
        symbol=order.stock,
        qty=order.amount,
        side='buy',
        type='market',
        time_in_force='gtc'
  )
  print("Purchased:", entry.stock)

def sell(order):
  api.submit_order(
      symbol=order.stock,
      qty=order.amount,
      side='sell',
      type='market',
      time_in_force='gtc'
  )
  print("Sold:", entry.stock)

def executeOrders(orders):
  for order in orders:
    if order.position == "buy":
      buy(order)
    elif order.position == 'sell':
      sell(order)

def rebalance(stocks_to_order):
  sell_orders = []
  buy_orders = []

  order_stocks = [order.stock for order in stocks_to_order]
  portfolio = api.list_positions()
  position_stocks = [position.symbol for position in portfolio]

  for position in portfolio:
    if position not in order_stocks:
      order = Order(position.symbol, position.qty, 'sell')
      sell_orders.append(order)

  for position in stocks_to_order:
    if position not in position_stocks:
      order = Order(position.stock, position.amount, 'buy')
      buy_orders.append(order)

  orders = sell_orders + buy_orders
  return orders
  


assets = getAllAssets()
#database.setupPrices(api, assets)

report = generateReport()
stocks_to_order = getOrders(report)
orders = rebalance(stocks_to_order)

for order in orders:
  print(order.stock, order.amount, order.position)

#executeOrders(orders)

print("My program took", time.time() - start_time, "to run")