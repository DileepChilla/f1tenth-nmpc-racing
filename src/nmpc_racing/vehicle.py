"""Vehicle parameters and derived quantities for the F1TENTH car.

The numbers come from the simulator (see ``config/vehicle.yaml``), so the
controller's prediction model and the simulated plant share one source of truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

G = 9.81  # gravitational acceleration [m/s^2]

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "vehicle.yaml"


@dataclass(frozen=True)
class VehicleParams:
    mu: float
    C_Sf: float
    C_Sr: float
    lf: float
    lr: float
    h: float
    m: float
    I: float
    s_min: float
    s_max: float
    sv_min: float
    sv_max: float
    v_switch: float
    a_max: float
    v_min: float
    v_max: float
    width: float
    length: float

    @classmethod
    def from_yaml(cls, path: str | Path = DEFAULT_CONFIG) -> "VehicleParams":
        with open(path) as f:
            return cls(**yaml.safe_load(f))

    @property
    def wheelbase(self) -> float:
        return self.lf + self.lr

    @property
    def Fz_front(self) -> float:
        """Static normal load on the front axle [N]."""
        return self.m * G * self.lr / self.wheelbase

    @property
    def Fz_rear(self) -> float:
        """Static normal load on the rear axle [N]."""
        return self.m * G * self.lf / self.wheelbase

    @property
    def C_alpha_front(self) -> float:
        """Front axle cornering stiffness [N/rad] = mu * C_Sf * Fz_front."""
        return self.mu * self.C_Sf * self.Fz_front

    @property
    def C_alpha_rear(self) -> float:
        """Rear axle cornering stiffness [N/rad] = mu * C_Sr * Fz_rear."""
        return self.mu * self.C_Sr * self.Fz_rear

    @property
    def understeer_gradient(self) -> float:
        """K = m/L * (lr/C_af - lf/C_ar) [rad/(m/s^2)]. K > 0: understeer."""
        return (self.m / self.wheelbase) * (
            self.lr / self.C_alpha_front - self.lf / self.C_alpha_rear
        )
