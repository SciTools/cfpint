import pint
import pytest

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
        assert str(m) == "meter"

    def test_cflike_product(self):
        m = Unit("m.s-1")
        assert str(m) == "meter/second"

    def test_cflike_exponent(self):
        m = Unit("kg.s-2")
        assert str(m) == "kilogram/second**2"

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
        assert str(ms) == "meter/second**2"

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
