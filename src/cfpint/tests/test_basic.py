import pint
import pytest
from cf_units import Unit as CFU_Unit

# from cfpint import install_defaults
from cfpint import Unit

# TODO: want to know why this didn't work
# @pytest.fixture(scope="session")
# def install():
#     install_defaults()


class TestBasicCflike:
    """Basic behaviours copied from cf_xarray.unit."""

    def test_non_cf(self):
        m = Unit("m")
        assert str(m) == "m"

    def test_cflike_product(self):
        m = Unit("m.s-1")
        assert str(m) == "m s-1"

    def test_cflike_exponent(self):
        m = Unit("kg.s-2")
        assert str(m) == "kg s-2"

    @pytest.mark.parametrize(
        "expr",
        [
            "m s-2",
            "m.s-2",
            "m.s**-2",
            "m/s2",
            "m / s**2",
            "m/s**2",
            "m / s2",
            "m/sec/s",
            "m / s / s",
            "meter / seconds**2",
            "meters.s-2",
        ],
    )
    def test_cflike_multistyle(self, expr):
        """Test that a bunch of different styles all mean the same thing."""
        ms = Unit(expr)
        assert str(ms) == "m s-2"

    def test_pintlike_properties(self):
        ms = Unit("m.s-2")
        assert isinstance(ms, pint.Unit)
        assert ms.dimensionless is False
        assert ms.dimensionality == {"[length]": 1, "[time]": -2}


class TestCompares:
    @pytest.fixture(params=["eq", "ne"])
    def equal(self, request):
        return request.param == "eq"

    def test_eq_owntype(self, equal):
        m1 = Unit("m")
        m2 = Unit("metres") if equal else "secs"
        assert m1 is not m2
        if equal:
            assert m1 == m2
        else:
            assert m1 != m2

    def test_eq_string(self, equal):
        m1 = Unit("m")
        string = "meter" if equal else "second"
        if equal:
            assert m1 == string
            assert m1 == "metre"  # alternative spelling, for good measure
        else:
            assert m1 != string

    def test_string_eq(self, equal):
        m1 = Unit("m")
        string = "meter" if equal else "second"
        if equal:
            assert string == m1
            assert "metres" == m1  # alternative spelling, for good measure
        else:
            assert string != m1

    def test_eq_pintbasic(self):
        m1 = Unit("m")
        m2 = pint.Unit("m")
        assert type(m1) is Unit
        assert type(m2) is not Unit
        assert type(m2) is pint.Unit
        assert m1 == m2
        assert m2 == m1

    def test_eq_cfunit(self):
        m1 = Unit("m")
        m2 = CFU_Unit("m")
        assert m1 == m2
        assert m2 == m1


class TestDates:
    @pytest.mark.parametrize("calendar", [None, "default", "365_day"])
    def test_date(self, calendar):
        kwargs = {} if calendar is None else {"calendar": calendar}
        date_unit = Unit("days since 1970-01-01", **kwargs)
        assert (date_unit * 1).units == "days"
        assert date_unit.startdate_string == "1970-01-01"
        expect_calendar = calendar
        assert date_unit.calendar_string == expect_calendar

    @pytest.mark.parametrize("unitstr", ["m", "days", "hours since 1970"])
    def test_is_datelike(self, unitstr):
        unit = Unit(unitstr)
        assert unit.is_datelike() == (" since " in unitstr)

    @pytest.mark.parametrize(
        "other",
        ["days since 1970", "days since 1900"],
    )
    def test_date_difference(self, other):
        m1 = Unit("hours since 1970")
        # TODO: is this what we now need to do for "Unit arithmetic"?
        # i.e. we need to make Quantities
        diff_units = ((1.0 * m1) - (1.0 * Unit(other))).units
        assert isinstance(diff_units, Unit)
        assert diff_units == "hours"
        assert not diff_units.is_datelike()

    @pytest.mark.parametrize("method", ["str", "repr"])
    @pytest.mark.parametrize("calendar", [None, "default", "365_day"])
    def test_str_repr(self, calendar, method):
        kwargs = {} if calendar is None else {"calendar": calendar}
        date_unit = Unit("day since 1970", **kwargs)
        # TODO: fix this (d//days), but for now it is done in Iris ???
        expect = "d since 1970"
        if calendar == "365_day":
            expect += ", calendar='365_day'"
        if method == "str":
            result = str(date_unit)
        else:
            expect = f"<Unit('{expect}')>"
            result = repr(date_unit)
        assert result == expect
