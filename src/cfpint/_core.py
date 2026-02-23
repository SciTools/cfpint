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
class CfpintRegistry(pint.registry.UnitRegistry):
    Quantity: TypeAlias = pint.Quantity
    Unit: TypeAlias = Unit


# Create our own registry, based on our own UnitRegistry subclass
REGISTRY: CfpintRegistry = make_registry(CfpintRegistry)

# FOR NOW: failed to make selective installation work.
# TODO: work out why and make "selectable" in future ??
#
# def install_defaults():
#     REGISTRY.formatter.default_format = "CF"
#     pint.set_application_registry(REGISTRY)
#
# FOR NOW: just do it.
REGISTRY.formatter.default_format = "CF"
pint.set_application_registry(REGISTRY)
