import pytest
from rfsys.core.errors import InvalidArgumentError
from components.base_component import Tolerance


def test_tolerance_invalid_arg():
    pytest.raises(InvalidArgumentError, Tolerance, 'invalid_arg', [9, 11])
    pytest.raises(InvalidArgumentError, Tolerance, 'dB', [9, 11],
                  dist='invalid_dist')


def test_tolerance_value_uniform():
    t = Tolerance('dB', [8, 12])
    assert 8 <= t.get_value() <= 12


def test_tolerance_value_normal():
    t = Tolerance('dB', [8, 12], dist='normal')
    assert 8 <= t.get_value(10) <= 12


