from __future__ import print_function
import math
from collections import namedtuple

from colors import green, white, red, blue

from .acquisition import AllCash, Mortgage
from .common import Meterable, Airplane
from .depreciation import FixedDepreciation, ExponentialDepreciation, LinearDepreciation


class FixedCosts(Meterable):
  def __init__(self, insurance, hangar, subscriptions, property_tax, annual):
    self.yearly_cost = insurance + hangar + subscriptions + property_tax + annual

  def iterate_values(self):
    while True:
      yield self.yearly_cost / 12.0


# personal_rate = percentage of time used by owner vs school
class UsageModel(object):
  def __init__(
      self,
      personal_rate=1.0,  # percentage use by owner (1.0 = 100% of hours are owner hours)
                          # note, any percentage < 1.0 means that the airplane must be
                          # operated part 91, which means that it must get 100 hour inspections
                          # in addition to annuals
      hobbs_ratio=1.2,    # hobbs hour : tach hour ratio
      revenue=0):         # hourly hobbs revenue

    self.personal_rate = personal_rate
    self.hobbs_ratio = hobbs_ratio
    self.revenue = revenue


class HourlyCosts(Meterable):
  GAS_PRICE_100LL = 5.50

  def __init__(
      self,
      performance,
      engine,
      annual,
      part91=False):

    self.performance, self.engine, self.annual, self.part91 = performance, engine, annual, part91

  def iterate_values(self):
    hourly_tbo_reserve = 1.0 * self.engine.overhaul / self.engine.tbo
    hourly_gas = self.performance.gph * self.GAS_PRICE_100LL

    total = hourly_tbo_reserve + hourly_gas

    if self.part91:
      total += self.annual / 100.0

    # TODO: Support both reserve-style and step-style accounting.
    # TODO: Support oil costs, or just add fixed number like $3/hr
    while True:
      yield total


class DepreciationAggregator(object):
  def __init__(self, price_and_depreciations):
    self.prices = [price for price, _ in price_and_depreciations]
    self.depreciation_iters = [
        depreciation.iterate_values() for _, depreciation in price_and_depreciations]

  def price(self):
    return sum(
      price * next(iterator)
      for price, iterator in zip(self.prices, self.depreciation_iters))

  def tick(self):
    for iterator in self.depreciation_iters:
      next(iterator)


USE_TAX = 0.0825
PROPERTY_TAX = 0.012


def simple(
    plane,
    acquisition,
    flight_hours,
    ownership_months,
    usage=UsageModel(),  # default usage model = 100% personal usage
    sell=True,
    debug=False):

  part91 = usage.personal_rate < 1.0

  acquisition_iterator = acquisition.get(plane.price).iterate_values()

  # TODO(wickman) Add a location profile e.g. KSQL/KHWD
  fixed_iterator = FixedCosts(
      plane.insurance.ifr, # insurance
      3500,                # hangar
      1122 + 199,          # g1000 + foreflight subscriptions
      PROPERTY_TAX * plane.price,  # property tax
      plane.annual,        # annual inspection
  ).iterate_values()

  hourly_iterator = HourlyCosts(
      plane.performance,
      plane.engine,
      plane.annual,
      part91=part91
  ).iterate_values()

  depreciations = [(plane.price, plane.depreciation)]
  depreciations.extend((upgrade.price, upgrade.depreciation) for upgrade in plane.upgrades)
  depreciations = DepreciationAggregator(depreciations)

  costs = plane.price * USE_TAX
  balance = plane.price

  if debug:
    print('Starting costs: %s' % costs)
    print('Starting balance: %s' % balance)

  for k in range(ownership_months):
    principal, interest = next(acquisition_iterator)
    costs += interest
    balance -= principal
    fixed_costs = next(fixed_iterator)
    costs += fixed_costs
    depreciations.tick()

    if debug:
      print('Month %3d:' % k)
      print('  Fixed: %s' % fixed_costs)
      print('  Balance: %s' % balance)
      print('  Costs: %s' % costs)
      print('  P/I: %s / %s' % (principal, interest))

  for _ in range(flight_hours):
    costs += next(hourly_iterator)

  revenue = flight_hours * (1 - usage.personal_rate) * usage.revenue * usage.hobbs_ratio

  if debug:
    print('Revenue generated: %s' % revenue)

  price_at_sale = depreciations.price()

  if debug:
    print('Plane price: %s' % plane.price)
    print('Balance left on plane: %s' % balance)
    print('Price at sale: %s' % price_at_sale)
    print('Gas, tax, overhauls, interest: %s' % costs)

  # return the total amount spent
  spent = plane.price + sum(upgrade.price for upgrade in plane.upgrades)
  if sell:
    spent -= price_at_sale
  spent -= revenue
  spent += costs

  if debug:
    print('Total spent: %s' % spent)

  return spent
