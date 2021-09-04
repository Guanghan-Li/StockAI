from momentum import Momentum


class Entry:
  def __init__(self, stock, atr, percent_atr, current_momentum, prev_momentum, acceleration):
    self.stock = stock
    self.atr = atr
    self.percent_atr = percent_atr
    self.current_momentum = current_momentum
    self.prev_momentum = prev_momentum
    self.acceleration = acceleration

  def __str__(self):
    return "Stock: {} - ATR: {} - Percent ATR: {} - 1Y Momentum: {}".format(self.stock, self.atr, self.percent_atr, self.current_momentum, self.prev_momentum, self.acceleration)