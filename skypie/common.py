from collections import namedtuple


class Meterable(object):
  def iterate_values(self):
    pass


class Acquisition(object):
  # produces a Meterable whose iterate_values yields (P, i) tuples
  def get(self, price):
    pass


class Depreciation(Meterable):
  # yields %ages that represent percent of original price
  pass


Engine = namedtuple('Engine', ('overhaul', 'tbo'))
Performance = namedtuple('Performance', ('ktas', 'gph'))


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
    'upgrades',       # array of Upgrade objects
    'engine',         # engine (overhaul price, tbo) tuple
    'depreciation',   # depreciation model
  ])

  DEFAULT_ATTRS = dict(
    yearly_costs=0    # additional yearly costs, e.g. g1000 subscription for equipped planes
  )

  def __init__(self, **kw):
    self.__dict__.update(self.DEFAULT_ATTRS)
    self.__dict__.update(kw)
    self.__check()

  def __check(self):
    if not all(attr in self.__dict__ for attr in self.REQUIRED_ATTRS):
      raise ValueError('Missing one of %s' % ' '.join(self.REQUIRED_ATTRS))

  def __call__(self, **kwargs):
    kw = self.__dict__.copy()
    kw.update(**kwargs)
    return Airplane(**kw)
