from __future__ import print_function, absolute_import

from skypie.acquisition import Mortgage
from skypie.colorant import breakeven
from skypie.planes import DA40
from skypie.tabulator import table
from skypie.model import simple


def main():
    H_RANGE = [hours + 100 for hours in range(0, 1500, 100)]
    M_RANGE = [months + 24 for months in range(0, 120, 24)]

    def hourly_fly(plane, acquisition, hours, months):
      return simple(plane, acquisition, hours, months, sell=False) / hours if hours > 0 else 0

    def hourly_fly_with_sale(plane, acquisition, hours, months):
      return simple(plane, acquisition, hours, months, sell=True) / hours if hours > 0 else 0

    table(
        DA40,
        Mortgage(.15, 60, .0625),
        hourly_fly,
        h_range=H_RANGE,
        m_range=M_RANGE,
        colorant=breakeven(285),
    )

