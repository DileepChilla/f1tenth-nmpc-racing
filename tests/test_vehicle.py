import pytest

from nmpc_racing.vehicle import VehicleParams


@pytest.fixture(scope="module")
def vp() -> VehicleParams:
    return VehicleParams.from_yaml()


def test_wheelbase(vp):
    assert vp.wheelbase == pytest.approx(0.3302, abs=1e-4)


def test_axle_loads_sum_to_weight(vp):
    assert vp.Fz_front + vp.Fz_rear == pytest.approx(vp.m * 9.81)


def test_cornering_stiffness_in_newtons_per_radian(vp):
    # The gym's C_S values are normalised: C_alpha = mu * C_S * Fz.
    # Using C_S directly as N/rad (as in the v1 code) is ~20x too soft.
    assert vp.C_alpha_front == pytest.approx(94.3, abs=0.2)
    assert vp.C_alpha_rear == pytest.approx(100.9, abs=0.2)


def test_car_understeers(vp):
    assert vp.understeer_gradient > 0.0
