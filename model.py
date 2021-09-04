from peewee import *

proxy = DatabaseProxy()


def newPrices(name):
  class Prices(Model):
    date = DateTimeField(unique=True)
    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()

    class Meta:
      database = proxy
      table_name = name
  
  return Prices

class Prices(Model):
  date = DateTimeField(unique=True)
  open = FloatField()
  high = FloatField()
  low = FloatField()
  close = FloatField()

  class Meta:
    database = proxy
    table_name = 'table'

class Info(Model):
  last_updated = DateTimeField(unique=True)