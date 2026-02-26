"""Cfpint

An extension of Pint units to support CF style units.

Intended to replace cf-units and udunits with a pure Python CF units package.
Also adds Pint compatibility.
"""

from ._core import Unit, REGISTRY  #  , install_defaults

__all__ = ["Unit", "REGISTRY"]  # , "install_defaults"]
