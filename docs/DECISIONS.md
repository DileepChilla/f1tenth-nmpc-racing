# Design decisions

One entry per decision: what, why, what else was considered. These are the answers to
"why did you do it that way?".

## D1. Controller core is a plain Python package, ROS 2 is a thin wrapper
- **Decision:** `src/nmpc_racing/` has no ROS imports. `ros2/` only subscribes, calls the
  core, and publishes.
- **Why:** The controller can be unit-tested and run against the gym without ROS timing
  effects, so model errors and timing errors can be told apart.
- **Alternative:** Everything inside one ROS node (the v1 layout).

## D2. Cornering stiffness in N/rad is computed from the gym's normalised coefficients
- **Decision:** `C_alpha = mu * C_S * Fz` (front 94.3, rear 100.9 N/rad).
- **Why:** The gym's `C_Sf`, `C_Sr` are normalised [1/rad]; its lateral force is
  `mu * C_S * Fz * alpha`. Verified in `dynamic_models.py`. Covered by `tests/test_vehicle.py`.
- **Alternative:** Use `C_S` directly as N/rad (v1). That gave a model roughly 20x too soft.

## D3. Simulator pinned to a specific commit
- **Decision:** `GYM_REF` in `docker/Dockerfile` is the commit from the original project.
- **Why:** The upstream gym changed structure after 2023; unpinned builds are not reproducible.

## D4. Only measured quantities are fed to the controller
- **Note:** The gym reports `linear_vels_y = 0` and `linear_vels_x` = total speed `v`.
  The controller's initial state must be built accordingly (handled in Week 3 validation).
