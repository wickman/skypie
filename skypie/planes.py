from .common import (
    Airplane,
    Performance,
    Insurance,
    Engine,
)
from .depreciation import ExponentialDepreciation


DA40 = Airplane(
    'DA40',
    price=239000,
    performance=Performance(ktas=135, gph=10),
    insurance=Insurance(vfr=2200, ifr=1300),
    annual=3500,
    upgrades=[],
    engine=Engine(overhaul=18000, tbo=2000),
    depreciation=ExponentialDepreciation(0.10, 12),
)
