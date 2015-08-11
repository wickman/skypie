from __future__ import print_function

from colors import white


DEFAULT_Y_RANGE = [y + 1 for y in range(0, 10)]
DEFAULT_H_RANGE = [h + 100 for h in range(0, 2000, 100)]


def table(
    plane,
    acquisition,
    model,
    y_range=None,
    h_range=None,
    colorant=None,
    yearly=False):

  print('Plane:        %s' % plane.name)
  print('Acquisition:  %s' % acquisition)
  print('Depreciation: %s' % plane.depreciation)
  if plane.upgrades:
    print('Upgrades:')
    for upgrade in plane.upgrades:
      print('  %s: %s, %s' % (upgrade.name, upgrade.price, upgrade.depreciation))

  y_range = y_range or DEFAULT_Y_RANGE
  h_range = h_range or DEFAULT_H_RANGE

  print('%5s ' % '', end='')
  for years in y_range:
    print('%10d ' % years, end='')
  print('')

  for hours in h_range:
    print('%5d ' % hours, end='')

    for years in y_range:
      if yearly:
        num_years = years
        num_hours = int(num_years * hours)
      else:
        num_hours = hours

      rate = model(plane, acquisition, num_hours, months)

      srate = '%-.2f' % rate
      srate = '%10s ' % srate

      color = colorant(rate) if colorant is not None else white

      print(color(srate), end='')

    print('')
