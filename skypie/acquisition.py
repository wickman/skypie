from .common import Acquisition, Meterable


__all__ = ('AllCash', 'Mortgage')


class AllCashMeterable(Meterable):
  def __init__(self, price):
    self.price = price

  def iterate_values(self):
    yield (self.price, 0)
    while True:
      yield (0, 0)


class AllCash(Acquisition):
  def get(self, price):
    return AllCashMeterable(price)

  def __str__(self):
    return 'all cash'


class MortgageMeterable(Meterable):
  @classmethod
  def monthly_payment(cls, r, N, P):
    r /= 12
    return P * r * (1 + r) ** N / ((1 + r) ** N - 1)

  @classmethod
  def iterate_payments(cls, rate, term, balance):
    interest = 0
    payment = cls.monthly_payment(rate, term, balance)
    for month in range(term):
      interest_portion = (rate / 12) * balance
      principal_portion = payment - interest_portion
      balance -= principal_portion
      yield (principal_portion, interest_portion)

  def __init__(self, price, down_payment, term, rate):
    self.price, self.down_payment, self.rate, self.term = price, down_payment, rate, term

  def iterate_values(self):
    down_payment = self.down_payment * self.price
    balance = self.price - down_payment
    payment_iterator = self.iterate_payments(self.rate, self.term, balance)
    yield (down_payment, 0)
    for principal, interest in payment_iterator:
      yield (principal, interest)
    while True:
      yield (0, 0)


class Mortgage(Acquisition):
  def __init__(self, down_payment, term, rate):
    self.down_payment, self.rate, self.term = down_payment, rate, term

  def get(self, price):
    return MortgageMeterable(price, self.down_payment, self.term, self.rate)

  def __str__(self):
    return '%d month mortgage, rate: %.2f%%, down payment: %.2f%%' % (
        self.term,
        self.rate * 100,
        self.down_payment * 100)
