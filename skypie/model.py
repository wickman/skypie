from __future__ import print_function

from collections import defaultdict
import math

from .balance import (
    Asset,
    Balance,
    CapEx,
    Depreciation,
    Hobby,
    Income,
    OpEx,
)
from .common import Meterable
from .constants import CONSTANTS


class UsageModel(object):
  def __init__(
      self,
      personal_rate=1.0,  # percentage use by owner (1.0 = 100% of hours are owner hours)
                          # note, any percentage < 1.0 means that the airplane must be
                          # operated part 91, which means that it must get 100 hour inspections
                          # in addition to annuals
      hobbs_ratio=1.2,    # hobbs hour : tach hour ratio
      salary=0,           # hourly salary as cost of revenue
      revenue=0):         # hourly hobbs revenue

    self.personal_rate = personal_rate
    self.hobbs_ratio = hobbs_ratio
    self.salary = salary
    self.revenue = revenue


def simple(
    plane,
    acquisition,
    flight_hours,
    ownership_years,
    usage=UsageModel(),  # default usage model = 100% personal usage
    constants=CONSTANTS):

  assert ownership_years > 0
  ownership_months = ownership_years * 12

  acquisition_iterator = acquisition.get(plane.price).iterate_values()

  yearly_costs = (
      plane.insurance +
      plane.price * constants['property_tax'] +
      plane.yearly_costs
  )

  hourly_costs = (
      plane.performance.gph * constants[plane.engine.fuel]
      # todo: oil costs
  )

  # initialize a balance sheet
  balance = Balance()

  depreciations = defaultdict(list)

  # we have two models:
  #   - the salvage price (presumably some exponential decay.)
  #   - the depreciation model (presumably straight-line.)
  #
  # Asset(price, salvage value, years)
  balance += Asset(
      plane.price,
      plane.price * plane.depreciation.at(ownership_months),
      ownership_months)

  depreciation_value = plane.price - plane.price * plane.depreciation.at(ownership_months)
  for year in range(ownership_years):
    depreciations[year].append(1.0 * depreciation_value / ownership_years)

  for upgrade in plane.upgrades:
    balance += CapEx(upgrade.price)
    balance += Asset(
        upgrade.price,
        upgrade.depreciation.at(ownership_months),
        ownership_months)
    depreciation_value = upgrade.price - upgrade.price * upgrade.depreciation.at(ownership_months)
    for year in range(ownership_years):
      depreciations[year].append(1.0 * depreciation_value / ownership_years)

  balance += OpEx(plane.price * constants['use_tax'])

  engine_hours = plane.engine.smoh
  prop_hours = plane.prop.spoh
  months_since_annual = 0
  hours_since_inspection = 0

  per_year_hours = 1.0 * flight_hours / ownership_years
  per_month_hours = 1.0 * flight_hours / ownership_months
  per_month_hobby = int(usage.personal_rate * per_month_hours)
  per_month_commercial = int(per_month_hours) - per_month_hobby

  print('Per month hobby: %s' % per_month_hobby)
  print('Per month commercial: %s' % per_month_hobby)

  for month in range(ownership_months):
    principal, interest = next(acquisition_iterator)
    balance += CapEx(principal)
    balance += OpEx(interest)

    if month % 12 == 0:
      balance += OpEx(yearly_costs)
      for depreciation in depreciations[month / 12]:
        balance += Depreciation(depreciation)

    engine_hours += per_month_hobby
    prop_hours += per_month_hobby
    balance += Hobby(hourly_costs * per_month_hobby)

    engine_hours += per_month_commercial
    prop_hours += per_month_commercial
    balance += OpEx(hourly_costs * per_month_commercial)
    balance += Income(usage.revenue * per_month_commercial * usage.hobbs_ratio)
    balance += OpEx(usage.salary * per_month_commercial * usage.hobbs_ratio)

    # Because the useful life of an engine is > 1 year we must
    # categorize the overhaul as a capital expenditure and
    # depreciate accordingly.
    if engine_hours > plane.engine.tbo:
      engine_hours -= plane.engine.tbo
      balance += Asset(
          plane.engine.overhaul,
          0,
          int(math.ceil(plane.engine.tbo / per_month_hours)))
      balance += CapEx(plane.engine.overhaul)
      ownership_years = int(math.ceil(plane.engine.tbo / per_year_hours))
      for year in range(ownership_years):
        depreciations[month / 12 + year].append(1.0 * plane.engine.overhaul / ownership_years)

    # Same for prop
    if prop_hours > plane.prop.tbo:
      prop_hours -= plane.prop.tbo
      balance += Asset(
          plane.prop.overhaul,
          0,
          int(math.ceil(plane.prop.tbo / per_month_hours)))
      balance += CapEx(plane.prop.overhaul)
      ownership_years = int(math.ceil(plane.prop.tbo / per_year_hours))
      for year in range(ownership_years):
        depreciations[month / 12 + year].append(1.0 * plane.prop.overhaul / ownership_years)

    months_since_annual += 1
    hours_since_inspection += per_month_hours
    if months_since_annual >= 12 or hours_since_inspection >= 100:
      months_since_annual = 0
      hours_since_inspection = 0
      balance += OpEx(plane.annual)

    balance.tick()

  return balance
