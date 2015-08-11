from .common import (
    Airplane,
    Engine,
    Performance,
    Prop,
)
from .depreciation import ExponentialDepreciation
from .upgrades import G500_GTN750

# TODO:
#   Add TTAF/TTSMOH/TTSPOH
#   Pull depreciation model off plane.
#


# G1000 Chart subscription price
G1000_SUBSCRIPTION = 1122


Diamond_DA40 = Airplane(
    name='DA40',
    price=239000,
    performance=Performance(ktas=135, gph=9),
    insurance=5580,
    annual=1600,
    upgrades=[],
    engine=Engine(overhaul=24000, tbo=2000, fuel='gas_100ll'),
    prop=Prop(overhaul=3000, tbo=2000),
    depreciation=ExponentialDepreciation(0.10, 12),
    yearly_costs=G1000_SUBSCRIPTION,
)

Cessna_T210 = Airplane(
    name='T210',
    price=79000,
    performance=Performance(ktas=170, gph=18),
    insurance=8000,
    annual=9000,
    upgrades=[G500_GTN750],
    engine=Engine(overhaul=30000, tbo=1400, fuel='gas_100ll'),
    prop=Prop(overhaul=4000, tbo=2000),
    depreciation=ExponentialDepreciation(0.03, 12),
)


"""
Cirrus_SR20 = Airplane(
    name='SR20',
    price=369000,
    performance=Performance(ktas=145, gph=10),
    insurance=2500,
    annual=3500,
    upgrades=[],
    engine=Engine(overhaul=25000, tbo=2200, fuel='gas_100ll'),
    depreciation=ExponentialDepreciation(0.10, 12),
    yearly_costs=G1000_SUBSCRIPTION,
)

Diamond_DA42 = Airplane(
    name='DA42',
    price=821000,
    performance=Performance(ktas=191, gph=16),
    insurance=8000,
    annual=7000,
    upgrades=[],
    # No support for twins yet, just put overhaul at 2x price
    # engine=Engine(overhaul=22000, tbo=1400, fuel='gas_jet_a'),
    engine=Engine(overhaul=44000, tbo=1400, fuel='gas_jet_a'),
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
    engine=Engine(overhaul=30000, tbo=1400, fuel='gas_100ll'),
    depreciation=ExponentialDepreciation(0.03, 12),
)

Cessna_152 = Airplane(
    name='152',
    price=35000,
    performance=Performance(ktas=107, gph=5.5),
    insurance=800,
    annual=1500,
    upgrades=[],
    engine=Engine(overhaul=13900, tbo=2400, fuel='gas_100ll'),
    depreciation=ExponentialDepreciation(0.03, 12),
)

Cessna_177RG = Airplane(
    name='177RG',
    price=74900,
    performance=Performance(ktas=170, gph=10),
    insurance=1500,
    annual=1500,
    upgrades=[G500_GTN750],
    engine=Engine(overhaul=20000, tbo=2000, fuel='gas_100ll'),
    depreciation=ExponentialDepreciation(0.03, 12),
)

PLANES = dict({
    'DA40': Diamond_DA40,
    'DA42': Diamond_DA42,
    'T210': Cessna_T210,
    'SR20': Cirrus_SR20,
    '152': Cessna_152,
    '177RG': Cessna_177RG,
})
"""

Cessna_177RG = Airplane(
    name='177RG',
    price=74900,
    performance=Performance(ktas=170, gph=10),
    insurance=1500,
    annual=1500,
    upgrades=[G500_GTN750],
    engine=Engine(overhaul=20000, tbo=2000, fuel='gas_100ll'),
    prop=Prop(overhaul=3000, tbo=2000),
    depreciation=ExponentialDepreciation(0.03, 12),
)

Pipistrel_Virus = Airplane(
    name='Virus',
    price=125000,
    performance=Performance(ktas=145, gph=4),
    insurance=3000,
    annual=1500,
    upgrades=[],
    engine=Engine(overhaul=12000, tbo=2000, fuel='gas_mogas'),
    prop=Prop(overhaul=3000, tbo=2000),
    depreciation=ExponentialDepreciation(0.10, 12),
)

PLANES = dict({
    'DA40': Diamond_DA40,
    'T210': Cessna_T210,
    '177RG': Cessna_177RG,
    'Virus': Pipistrel_Virus,
})
