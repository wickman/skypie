from colors import red, green, blue


def breakeven(watermark):
  def colorant(amount):
    if amount <= 0:
      return green
    elif 0 < amount < watermark:
      return blue
    else: 
      return red

  return colorant
