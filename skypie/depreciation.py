import math

from .common import Depreciation


class FixedDepreciation(Depreciation):
  def __init__(self, percent):
    self.percent = percent
  
  def iterate_values(self):
    while True:
      yield self.percent
  
  def __str__(self):
    return 'Fixed depreciation of %.2f%%' % (self.percent * 100)


class YearlyConstantDepreciation(Depreciation):
  def __init__(self, depreciation_rate):
    self.rate = depreciation_rate
  
  def iterate_values(self):
    x = 1.0
    exponent = math.exp(math.log(1 + self.rate) / 12)
    while True:
      x /= exponent
      yield x

  def __str__(self):
    return 'Yearly depreciation of %.2f%% per annum' % (self.rate * 100)


class ExponentialDepreciation(Depreciation):
  def __init__(self, amount, rate):
    # amount = percentage, e.g. 0.07 for 7%
    # rate = over how many months
    # e.g. (0.07, 12) => 7% per year
    #      (0.03, 1) => 3% per month
    self.amount = amount
    self.rate = rate
  
  def iterate_values(self):
    x = 1.0
    exponent = math.exp(math.log(1 + self.amount) / self.rate)
    while True:
      x /= exponent
      yield x

  def __str__(self):
    return '%.2f%% per %d months' % (self.amount * 100, self.rate)
