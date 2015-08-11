from colors import blue, green, red


def breakeven(low_watermark, high_watermark):
  def colorant(amount):
    if amount < low_watermark:
      return red
    elif low_watermark < amount < high_watermark:
      return blue
    else:
      return green

  return colorant
