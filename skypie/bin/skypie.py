from __future__ import print_function, absolute_import

from skypie.acquisition import Mortgage
from skypie.colorant import breakeven
from skypie.planes import DA40
from skypie.tabulator import table
from skypie.model import fly_and_sell


table(
    DA40, 
    Mortgage(.15, 120, .0625),
    fly_and_sell,
    breakeven(285),
)

    