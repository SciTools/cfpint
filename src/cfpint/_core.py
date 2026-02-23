"""
Or own version of pint Units, for added CF support.

Notably customised Unit and Registry classes.
"""
from typing import TypeAlias
import pint

from ._cfarray_units_like import make_registry

# Setup our own classes

class Unit(pint.Unit):
    pass


# See: https://pint.readthedocs.io/en/stable/advanced/custom-registry-class.html#custom-quantity-and-unit-class
class CfpintRegistry(pint.registry.GenericUnitRegistry[pint.Quantity, pint.Unit]):
    Quantity: TypeAlias = pint.Quantity
    Unit: TypeAlias = Unit


# Create our own registry, based on our own UnitRegistry subclass
REGISTRY: CfpintRegistry = make_registry(CfpintRegistry)
