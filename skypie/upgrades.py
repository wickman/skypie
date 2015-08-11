from .common import Upgrade
from .depreciation import (
    DepreciationCombinator,
    FixedDepreciation,
    LinearDepreciation,
)


G500_GTN750 = Upgrade(
  name='G500/GTN750',
  price=52000,
  depreciation=DepreciationCombinator([FixedDepreciation(.50), LinearDepreciation(120)])
)
