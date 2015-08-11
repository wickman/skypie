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
from .depreciation import LinearDepreciation


class UsageModel(object):
  def __init__(
      self,
      hobbs_ratio=1.3,   # ratio of hobbs : tach
      salary=0,          # hourly salary as cost of revenue
      revenue=0):        # hourly hobbs revenue

    self.hobbs_ratio = hobbs_ratio
    self.salary = salary
    self.revenue = revenue


def simple(
    plane,
    acquisition,
    part91_hours_per_month,
    part135_hours_per_month,
    ownership_years,
    usage=UsageModel(),  # default usage model = 100% part91/personal usage
    constants=CONSTANTS,
    sell=False):

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

  plane_asset = Asset(
      plane.price,
      plane.depreciation,
      value=plane.value)

  balance += plane_asset

  depreciation_value = plane.price - plane.price * plane.depreciation.at(ownership_months)
  for year in range(ownership_years):
    depreciations[year].append(1.0 * depreciation_value / ownership_years)

  for upgrade in plane.upgrades:
    balance += CapEx(upgrade.price)
    balance += Asset(upgrade.price, upgrade.depreciation)
    depreciation_value = upgrade.price - upgrade.price * upgrade.depreciation.at(ownership_months)
    for year in range(ownership_years):
      depreciations[year].append(1.0 * depreciation_value / ownership_years)

  balance += OpEx(plane.price * constants['use_tax'])

  engine_hours = plane.engine.smoh
  prop_hours = plane.prop.spoh
  months_since_annual = 0
  hours_since_inspection = 0

  per_month_hours = 1. * (part91_hours_per_month + part135_hours_per_month)
  per_year_hours = per_month_hours * 12
  per_month_hobby = 1. * part91_hours_per_month
  per_month_commercial = 1. * part135_hours_per_month

  for month in range(ownership_months):
    principal, interest = next(acquisition_iterator)
    balance += CapEx(principal)
    balance += OpEx(interest)

    if month % 12 == 0:
      balance += OpEx(yearly_costs)
      for depreciation in depreciations[month / 12]:
        balance += Depreciation(depreciation)

    engine_hours += 1. * per_month_hobby / usage.hobbs_ratio
    prop_hours += 1. * per_month_hobby / usage.hobbs_ratio
    balance += Hobby(hourly_costs * per_month_hobby)

    engine_hours += 1. * per_month_commercial / usage.hobbs_ratio
    prop_hours += 1. * per_month_commercial / usage.hobbs_ratio
    balance += OpEx(hourly_costs * per_month_commercial)
    balance += Income(usage.revenue * per_month_commercial)
    balance += OpEx(usage.salary * per_month_commercial)

    # Because the useful life of an engine is > 1 year we must
    # categorize the overhaul as a capital expenditure and
    # depreciate accordingly.
    if engine_hours > plane.engine.tbo:
      engine_hours -= plane.engine.tbo
      balance += Asset(
          plane.engine.overhaul,
          LinearDepreciation(int(math.ceil(plane.engine.tbo / per_month_hours))))
      balance += CapEx(plane.engine.overhaul)
      ownership_years = int(math.ceil(plane.engine.tbo / per_year_hours))
      for year in range(ownership_years):
        depreciations[month / 12 + year].append(1.0 * plane.engine.overhaul / ownership_years)

    # Same for prop
    if prop_hours > plane.prop.tbo:
      prop_hours -= plane.prop.tbo
      balance += Asset(
          plane.prop.overhaul,
          LinearDepreciation(int(math.ceil(plane.prop.tbo / per_month_hours))))
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

  if sell:
    current_month = balance.month
    sale_income = 0

    # tally remaining principal
    remaining_principal = 0
    while True:
      principal, interest = next(acquisition_iterator)
      remaining_principal += principal
      if principal == 0:
        break

    for month, items in balance.items.items():
      for item in items:
        if isinstance(item, Asset):
          percentage_value = item.depreciation_model.at(current_month - month)
          if percentage_value > 0:
            sale_income += item.value * percentage_value

    # could be negative
    balance += Income(sale_income - remaining_principal)

  return balance
