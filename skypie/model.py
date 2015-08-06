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


def simple(
    plane,
    acquisition,
    flight_hours,
    ownership_months,
    sell=True,
    debug=False):

  acquisition_iterator = acquisition.get(plane.price).iterate_values()
  fixed_iterator = FixedCosts(
      plane.insurance.ifr, # insurance
      3500,                # hangar
      1122 + 199,          # g1000 + foreflight subscriptions
      .012 * plane.price,  # property tax
      plane.annual,        # annual inspection
  ).iterate_values()
  hourly_iterator = HourlyCosts(
      plane.performance,
      plane.engine,
      plane.annual,
  ).iterate_values()
  depreciations = DepreciationAggregator([(plane.price, plane.depreciation)] + plane.upgrades)

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

  price_at_sale = depreciations.price()

  if debug:
    print('Plane price: %s' % plane.price)
    print('Balance left on plane: %s' % balance)
    print('Price at sale: %s' % price_at_sale)
    print('Gas, tax, overhauls, interest: %s' % costs)

  # return the total amount spent
  spent = plane.price
  if sell:
    spent -= price_at_sale
  spent += costs

  if debug:
    print('Total spent: %s' % spent)

  return spent


def part91_cost(plane, acquisition, flight_hours, ownership_months, percentage_part91, part91_rate):
  acquisition_iterator = acquisition.get(plane.price).iterate_values()
  fixed_iterator = FixedCosts(
      plane.insurance.ifr, # insurance
      3500,                # hangar
      1122 + 199,          # g1000 + foreflight subscriptions
      .012 * plane.price,  # property tax
      plane.annual,        # annual inspection
  ).iterate_values()
  hourly_iterator = HourlyCosts(
      plane.performance,
      plane.engine,
      plane.annual,
      part91=True,
  ).iterate_values()
  depreciations = DepreciationAggregator([(plane.price, plane.depreciation)] + plane.upgrades)

  costs = plane.price * USE_TAX
  balance = plane.price

  for k in range(ownership_months):
    principal, interest = next(acquisition_iterator)
    costs += interest
    balance -= principal
    fixed_costs = next(fixed_iterator)
    costs += fixed_costs
    depreciations.tick()

  income = percentage_part91 * flight_hours * part91_rate

  for _ in range(flight_hours):
    costs += next(hourly_iterator)

  price_at_sale = depreciations.price()

  # return the total amount spent
  spent = plane.price - price_at_sale
  spent += costs
  spent -= income

  return spent



def debug(plane, acquisition, hours, months, part91=False):
  spent = fly_and_sell(plane, acquisition, hours, months, part91=part91, debug=True)
  print('Total hourly rate: %.2f/hr' % (spent / hours if hours > 0 else 0))
  print('\n')


"""
table(DA40, Mortgage(.15, 120, .0625), breakeven=285)
table(DA40, Mortgage(.25,  60, .0625), breakeven=285)
table(DA40,                   AllCash, breakeven=285)
table(DA40, Mortgage(.15, 120, .0625), breakeven=285, part91=(0.25, 275))
table(DA40, Mortgage(.15, 120, .0625), breakeven=285, part91=(0.5, 275))
table(DA40, Mortgage(.15, 120, .0625), breakeven=285, part91=(0.75, 275))


#table(DA40, AllCash, breakeven=285)
#debug(DA40, Mortgage(.15, 120, .0625), 2000, 144)
#debug(DA40, AllCash, 500, 12)
"""
