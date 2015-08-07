from colors import blue, green, red


def breakeven(watermark):
  def colorant(amount):
    if amount <= 0:
      return green
    elif 0 < amount < watermark:
      return blue
    else:
      return red

  return colorant
