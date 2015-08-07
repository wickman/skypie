from .common import (
    Airplane,
    Performance,
    Engine,
)
from .depreciation import ExponentialDepreciation


DA40 = Airplane(
    name='DA40',
    price=239000,
    performance=Performance(ktas=135, gph=10),
    # insurance=Insurance(vfr=2200, ifr=1300),
    insurance=1300,
    annual=3500,
    upgrades=[],
    engine=Engine(overhaul=18000, tbo=2000),
    depreciation=ExponentialDepreciation(0.10, 12),
)

T210 = Airplane(
    name='T210',
    price=79000,
    performance=Performance(ktas=170, gph=18),
    # insurance=Insurance(vfr=8000, ifr=5000),
    insurance=5000,
    annual=9000,
    upgrades=[],
    engine=Engine(overhaul=30000, tbo=1400),
    depreciation=ExponentialDepreciation(0.03, 12),
)


PLANES = dict(
    DA40=DA40,
    T210=T210,
)
