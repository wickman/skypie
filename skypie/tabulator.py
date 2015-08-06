from color import white


DEFAULT_M_RANGE = [m + 12 for m in range(0, 120, 12)]
DEFUALT_H_RANGE = [h + 100 for h in range(0, 2000, 100)]


def table(plane, acquisition, model, m_range=None, h_range=None, colorant=None):
  m_range = m_range or DEFAULT_M_RANGE
  h_range = h_range or DEFAULT_H_RANGE

  print('%5s ' % '', end='')
  for months in m_range:
    print('%10d ' % months, end='')
  print('')

  for hours in h_range:
    print('%5d ' % hours, end='')

    for months in m_range:
      rate = model(plane, acquisition, hours, months)

      srate = '%-.2f' % rate
      srate = '%10s ' % srate
      
      color = colorant(rate) if colorant is not None else white
      
      print(color(srate), end='')

    print('')
