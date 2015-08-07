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


class LinearDepreciation(Depreciation):
  def __init__(self, months):
    self.months = months

  def iterate_values(self):
    for k in range(self.months, 0, -1):
      yield 1.0 * k / self.months
    while True:
      yield 0

  def __str__(self):
    return 'Fixed %d month useful life.' % self.months


class DepreciationCombinator(Depreciation):
  def __init__(self, depreciation_models):
    self.dms = [model for model in depreciation_models]

  def iterate_values(self):
    dm_iters = [model.iterate_values() for model in self.dms]

    while True:
      yield reduce(float.__mul__, [next(dm_iter) for dm_iter in dm_iters])

  def __str__(self):
    return 'Blended depreciation: %s' % (' + '.join(map(str, (dm for dm in self.dms))))
