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
    'name',
    'price',
    'performance',
    'insurance',
    'annual',
    'upgrades',
    'engine',
    'depreciation',
  ])

  def __init__(self, **kw):
    self.__dict__.update(kw)
    self.__check()

  def __check(self):
    if not all(attr in self.__dict__ for attr in self.REQUIRED_ATTRS):
      raise ValueError('Missing one of %s' % ' '.join(REQUIRED_ATTRS))

  def __call__(self, **kwargs):
    kw = self.__dict__.copy()
    kw.update(**kwargs)
    return Airplane(**kw)
