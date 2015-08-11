from collections import defaultdict


class Asset(object):
  def __init__(self, value, salvage_value, months_depreciating):
    self.value, self.salvage_value, self.months_depreciating = (
        value, salvage_value, months_depreciating)

  def __str__(self):
    return 'Asset(%r -> %r over %r months)' % (
        self.value, self.salvage_value, self.months_depreciating)


class BalanceSheetItem(object):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return '%s(%s)' % (self.__class__.__name__, self.value)


class CapEx(BalanceSheetItem):
  pass


print(CapEx)
print(CapEx(23))

class OpEx(BalanceSheetItem):
  pass


class Hobby(BalanceSheetItem):
  pass


class Income(BalanceSheetItem):
  pass


class Depreciation(BalanceSheetItem):
  pass


class Balance(object):
  # for basis:
  #   (value, date, depreciation schedule)
  # for [capex, opex, income, hobby]
  #   (value, date)
  # what about capital expenditure that is paid out as down payment + p + i?
  #
  def __init__(self):
    self.month = 0
    self.items = defaultdict(list)

  def tick(self):
    self.month += 1

  def __iadd__(self, val):
    if isinstance(val, (Asset, CapEx, OpEx, Income, Hobby, Depreciation)):
      self.items[self.month].append(val)
    else:
      raise TypeError('Unknown balance shset item %s' % type(val))
    return self

  @classmethod
  def aggregate(cls, item_klazz, elements):
    return item_klazz(
        sum((element.value for element in elements if isinstance(element, item_klazz)), 0))

  def select_month(self, item_klazz, month):
    return self.aggregate(item_klazz, self.items[month])

  def select_year(self, item_klazz, year):
    return self.aggregate(item_klazz,
        sum((self.items[month] for month in range(12*year, 12*year + 12)), []))

  def at_month(self, month):
    cell = [item for item in self.items[month] if isinstance(item, Asset)]
    for item_klazz in CapEx, OpEx, Income, Hobby, Depreciation:
      cell.append(self.select_month(item_klazz, month))
    return cell

  def at_year(self, year):
    cell = []
    for month in range(12 * year, 12 * (year + 1)):
      cell.extend(item for item in self.items[month] if isinstance(item, Asset))
    for item_klazz in CapEx, OpEx, Income, Hobby, Depreciation:
      cell.append(self.select_year(item_klazz, year))
    return cell

  def aggregate_year(self, year, part91_percentage=1.0):
    outflow = sum(self.select_year(item_klazz, year).value for item_klazz in (CapEx, OpEx))
    inflow = sum(self.select_year(item_klazz, year).value for item_klazz in (Income,))
    income = inflow - outflow
    deductions = sum(self.select_year(item_klazz, year).value for item_klazz in (OpEx, Depreciation))
    business_income = income - deductions * part91_percentage
    return (income, business_income)

  #def aggregate(self, part91=False, part91_percentage=0):
  #  pass
