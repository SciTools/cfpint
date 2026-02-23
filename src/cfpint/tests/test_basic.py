import pint
import pytest

# from cfpint import install_defaults
from cfpint import Unit

# TODO: want to know why this didn't work
# @pytest.fixture(scope="session")
# def install():
#     install_defaults()


class TestBasicCflike:
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
