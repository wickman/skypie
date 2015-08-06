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

    self.name = name
    self.price = price
    self.performance = performance
    self.insurance = insurance
    self.annual = annual
    self.upgrades = upgrades
    self.engine = engine
    self.depreciation = depreciation
