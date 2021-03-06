from collections import namedtuple


class Meterable(object):
  def iterate_values(self):
    pass


class Acquisition(object):
  # produces a Meterable whose iterate_values yields (P, i) tuples
  def get(self, price):
    pass


class DepreciationModel(Meterable):
  # yields %ages that represent percent of original price
  def at(self, month):
    _, depreciation = list(zip(range(month), self.iterate_values()))[-1]
    return depreciation


Performance = namedtuple('Performance', ('ktas', 'gph'))


class Engine(object):
  def __init__(self, overhaul, tbo, fuel='gas_100ll', smoh=0):
    self.overhaul, self.tbo = overhaul, tbo
    self.fuel = fuel
    self.smoh = smoh

  def __str__(self):
    return '[%s smoh, %s tbo]' % (self.smoh, self.tbo)


class Prop(object):
  def __init__(self, overhaul, tbo, spoh=0):
    self.overhaul = overhaul
    self.tbo = tbo
    self.spoh = spoh

  def __str__(self):
    return '[%s spoh, %s tbo]' % (self.spoh, self.tbo)

class Upgrade(object):
  def __init__(
      self,
      name,
      price,
      depreciation):
    self.name, self.price, self.depreciation = name, price, depreciation


class Airplane(object):
  REQUIRED_ATTRS = frozenset([
    'name',           # name of the plane
    'price',          # price of the plane
    'performance',    # performance of the plane (ktas, gph) tuple
    'insurance',      # insurance cost of the plane
    'annual',         # cost of annual
    'engine',         # engine (overhaul price, tbo, fuel, smoh) tuple
    'prop',           # prop (overhaul price, tbo, spoh) tuple
    'depreciation',   # depreciation model
  ])

  DEFAULT_ATTRS = dict(
    yearly_costs=0,   # additional yearly costs, e.g. g1000 subscription for equipped planes
    upgrades=[],      # array of Upgrade objects
    ttaf=0,
    value=None,
  )

  def __init__(self, **kw):
    self.__dict__.update(self.DEFAULT_ATTRS)
    self.__dict__.update(kw)
    self.__check()
    if self.value is None:
      self.value = self.price

  def __check(self):
    if not all(attr in self.__dict__ for attr in self.REQUIRED_ATTRS):
      raise ValueError('Missing one of %s' % ' '.join(self.REQUIRED_ATTRS))

  def __call__(self, **kwargs):
    kw = self.__dict__.copy()
    kw.update(**kwargs)
    return Airplane(**kw)

  def __str__(self):
    return '%s price %s value %s insurance %s annual %s engine %s prop %s' % (
        self.name, self.price, self.value, self.insurance, self.annual, self.engine, self.prop)
