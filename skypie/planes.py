from .common import (
    Airplane,
    Engine,
    Performance,
)
from .depreciation import ExponentialDepreciation


# G1000 Chart subscription price
G1000_SUBSCRIPTION = 1122


Diamond_DA40 = Airplane(
    name='DA40',
    price=239000,
    performance=Performance(ktas=135, gph=10),
    insurance=1500,
    annual=3500,
    upgrades=[],
    engine=Engine(overhaul=18000, tbo=2000),
    depreciation=ExponentialDepreciation(0.10, 12),
    yearly_costs=G1000_SUBSCRIPTION,
)

Cessna_T210 = Airplane(
    name='T210',
    price=79000,
    performance=Performance(ktas=170, gph=18),
    insurance=5000,
    annual=9000,
    upgrades=[],
    engine=Engine(overhaul=30000, tbo=1400),
    depreciation=ExponentialDepreciation(0.03, 12),
)

Cessna_152 = Airplane(
    name='152',
    price=35000,
    performance=Performance(ktas=107, gph=5.5),
    insurance=800,
    annual=1500,
    upgrades=[],
    engine=Engine(overhaul=13900, tbo=2400),
    depreciation=ExponentialDepreciation(0.03, 12),
)

PLANES = dict({
    'DA40': Diamond_DA40,
    'T210': Cessna_T210,
    '152': Cessna_152,
})
