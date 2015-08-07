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
Insurance = namedtuple('Insurance', ('vfr', 'ifr'))


class Upgrade(object):
  def __init__(
      self,
      name,
      price,
      depreciation):
    self.name, self.price, self.depreciation = name, price, depreciation


class Airplane(object):
  """
  All attributes affecting cost (attribute of plane)
    - KTAS
    - GPH
    - Price
    - Insurance rate
    - Cost of annual
    - Necessary upgrades
    - Engine (overhaul cost, TBO)
    - Depreciation model
  """

  REQUIRED_ATTRS = frozenset([
    'name',
    'price',
    'performance',
    'insurance',
    'annual',
    'upgrades',
    'engine',
    'depreciation',
  ])

  """
  def __init__(
      self,
      name,
      price,          # int
      performance,    # (ktas, gph) tuple
      insurance,      # (vfr, ifr) tuple
      annual,         # price
      upgrades,       # [ (price, depreciation model), ... ]
      engine,         # (overhaul cost, tbo)
      depreciation):  # depreciation model
  """

  def __init__(self, **kw):
    self.__dict__.update(kw)
    """
    self.name = name
    self.price = price
    self.performance = performance
    self.insurance = insurance
    self.annual = annual
    self.upgrades = upgrades
    self.engine = engine
    self.depreciation = depreciation
    """
    self.__check()

  def __check(self):
    if not all(attr in self.__dict__ for attr in self.REQUIRED_ATTRS):
      raise ValueError('Missing one of %s' % ' '.join(REQUIRED_ATTRS))

  def __call__(self, **kwargs):
    kw = self.__dict__.copy()
    kw.update(**kwargs)
    return Airplane(**kw)
