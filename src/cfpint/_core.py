"""
Or own version of pint Units, for added CF support.

Notably customised Unit and Registry classes.
"""

from typing import TypeAlias
import pint

from ._cfarray_units_like import make_registry


# Setup our own classes
class Unit(pint.Unit):
    _DATEUNITS_SIGNATURE = " since "

    def __init__(self, *args, **kwargs):
        """Expand unit coverage to include date units."""
        startdate_str: str | None = None
        calendar_str: str | None = None
        if args and isinstance(args[0], str):
            # Catch date units.
            arg = args[0].lower()
            if self._DATEUNITS_SIGNATURE in arg:
                index = arg.index(self._DATEUNITS_SIGNATURE)
                base_unit = arg[:index]
                # NOTE: we are making no attempt to interpret the date string
                #  : cf-units makes only token efforts to check for suitable content,
                #  like expecting digits.
                #  And *no* attempt to normalise the date formatting.
                # TODO: validate this + normalise the formatting.
                startdate_str = arg[index + len(self._DATEUNITS_SIGNATURE) :]
                # NOTE: likewise, we don't really check calendar
                #  N.B. cf_units (1) checks against a list of valid names, and (2)
                #  normalises through a mapping of aliases.
                # TODO: add minimal checking of date+calendar, like cf_units or better
                calendar_str = kwargs.pop("calendar", "default")
                # Replace args[0]
                args = [base_unit] + list(args[1:])
        super().__init__(*args, **kwargs)
        if self.dimensionality.get("[time]" != 1):
            msg = (
                f'Base unit "{base_unit}" of time reference "{arg}" '
                "is not a time-like unit."
            )
            raise ValueError(msg)

        self.startdate_string = startdate_str
        self.calendar_string = calendar_str

    def is_datelike(self) -> bool:
        """Whether this unit is a time reference.

        Note
        ----
        **Don't** copy the 'is_time_reference' name from cf_units, since we don't
        support its other 'is_xxx' methods.
        """
        return self.startdate_string is not None

    def __eq__(self, other):
        """Support comparison between Units and strings.

        Pint Units do not support this, but cf_units did.

        Also support comparison with other unit-like objects
        -- specifically, regular pint.Unit and cf_units.Unit --
        using string conversion.
        """
        if not isinstance(other, pint.Unit):
            # Use the string conversion of whatever it is to create a pint unit.
            other = Unit(str(other))
        # plain string comparison works, because Pint does *not* "store" the original
        #  definition string (unlike udunits / cf_units).
        # Therefore the printed form is "canonical" anyway.
        return str(self) == str(other)

    def __str__(self):
        result = super(pint.Unit, self).__str__()
        if self.startdate_string is not None:
            result += self._DATEUNITS_SIGNATURE + self.startdate_string
            if self.calendar_string not in (None, "default"):
                result += f", calendar='{self.calendar_string!s}'"
        return result

    def __repr__(self):
        result = super(pint.Unit, self).__repr__()
        if self.startdate_string is not None:
            prefix, postfix = "<Unit('", "')>"
            assert result.startswith(prefix)
            assert result.endswith(postfix)
            result = prefix + str(self) + postfix
        return result


# See: https://pint.readthedocs.io/en/stable/advanced/custom-registry-class.html#custom-quantity-and-unit-class
class CfpintRegistry(pint.registry.UnitRegistry):
    Quantity: TypeAlias = pint.Quantity
    Unit: TypeAlias = Unit


# Create our own registry, based on our own UnitRegistry subclass
REGISTRY: CfpintRegistry = make_registry(
    CfpintRegistry
)  # include all 'normal' features

# FOR NOW: failed to make selective installation work.
# TODO: work out why and make "selectable" in future ??
#
# def install_defaults():
#     REGISTRY.formatter.default_format = "CF"
#     pint.set_application_registry(REGISTRY)
#
# FOR NOW: just do it.
pint.set_application_registry(REGISTRY)
pint.application_registry.default_system = "SI"
pint.application_registry.default_format = "cfu"
