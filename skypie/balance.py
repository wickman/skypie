from collections import defaultdict


class Asset(object):
  def __init__(self, price, depreciation_model, value=None):
    self.price, self.depreciation_model = price, depreciation_model
    self.value = self.price if value is None else value

  def __str__(self):
    return 'Asset(%s [price: %s], %s)' % (self.value, self.price, self.depreciation_model)


class BalanceSheetItem(object):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return '%s(%s)' % (self.__class__.__name__, self.value)


class CapEx(BalanceSheetItem):
  pass


class OpEx(BalanceSheetItem):
  pass


class Hobby(BalanceSheetItem):
  pass


class Income(BalanceSheetItem):
  pass


class Depreciation(BalanceSheetItem):
  pass


class Balance(object):
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
  def aggregate(cls, elements):
    items = [item for item in elements if isinstance(item, Asset)]
    for item_klazz in CapEx, OpEx, Income, Hobby, Depreciation:
      aggregated = item_klazz(value=sum(item.value for item in elements if isinstance(item, item_klazz)))
      if aggregated.value > 0:
        items.append(aggregated)
    return items

  def select(self, month=None, year=None, item_klazz=None):
    selected_items = []

    def keep(month, item, select_month=None, select_year=None, select_item_klazz=None):
      keep_item = True
      if select_month is not None and month != select_month:
        keep_item = False
      if select_year is not None and month / 12 != select_year:
        keep_item = False
      if select_item_klazz is not None:
        if isinstance(select_item_klazz, (list, tuple)):
          if not any(isinstance(item, item_klazz) for item_klazz in select_item_klazz):
            keep_item = False
        else:
          if not isinstance(item, select_item_klazz):
            keep_item = False
      return keep_item

    for mo, items in self.items.items():
      for item in items:
        if keep(mo, item, select_month=month, select_year=year, select_item_klazz=item_klazz):
          selected_items.append(item)

    return self.aggregate(selected_items)

  def sum(self, **kw):
    return sum(item.value for item in self.select(**kw))


def tax_adjusted_profit(balance_sheet, part91_percentage=1.0, tax_rate=0.25, **kw):
  expenses = balance_sheet.sum(item_klazz=(CapEx, OpEx), **kw)
  revenue = balance_sheet.sum(item_klazz=Income, **kw)
  deductions = balance_sheet.sum(item_klazz=(OpEx, Depreciation), **kw) * (1 - part91_percentage)
  # Taxable:
  #   - profit
  #
  # Profit:
  #   - revenue - expenses
  #
  # Taxable:
  #   - profit - deductions
  #
  # After-tax profits:
  #   - profit - max(profit - deductions, 0) * tax_rate
  profit = revenue - expenses
  return profit - max(profit - deductions, 0) * tax_rate
