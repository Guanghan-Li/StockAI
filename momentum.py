class Momentum:

  @staticmethod
  def netReturn(start_price, end_price):
    return (end_price-start_price) / start_price
  
  @staticmethod
  def grossReturn(start_price, end_price):
    return Momentum.netReturn(start_price, end_price) + 1
  
  @staticmethod
  def momentumOneMonth(month_data):
    start = month_data[0]['open']
    end = month_data[-1]['close']
    return Momentum.grossReturn(start, end)
  
  @staticmethod
  def momentumOneYear(year_data):
    gross_returns = []

    for month in year_data:
      one_month_momentum = Momentum.momentumOneMonth(month)
      gross_returns.append(one_month_momentum)
    
    momentum = Momentum.product(gross_returns) + 1

    return momentum


  @staticmethod
  def product(numbers):
    result = 1
    for number in numbers:
      result *= number
    
    return result