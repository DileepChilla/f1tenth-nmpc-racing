# F1TENTH Gym: what the simulator actually does

Task 1 notes. Every statement here was checked in the simulator source or measured in
the container. Line numbers refer to the pinned commit `4fdb9c7` of `f1tenth/f1tenth_gym`
(files in `gym/f110_gym/envs/`). The ROS 2 bridge is `f1tenth/f1tenth_gym_ros` `main`
at `883394d`. See [DECISIONS.md](DECISIONS.md) (D3, D5) for why these versions.

## 1. State and inputs

| Item | Value | Source |
|------|-------|--------|
| State vector | `[x, y, steer_angle, v, yaw, yaw_rate, slip_angle]` | comment in `base_classes.py` |
| Commands | steering angle [rad] and speed [m/s] (setpoints, not accelerations) | `env.step(np.array([[steer, speed]]))` |
| Setpoint tracking | an internal controller (`pid`) turns the setpoints into steering velocity and acceleration | `base_classes.py:282`, `dynamic_models.py` |
| Limits | steering ±0.4189 rad, steering rate ±3.2 rad/s, `a_max` 9.51 m/s², `v_max` 20 m/s | `config/vehicle.yaml` (gym defaults) |
| Physics time step | 0.01 s | `f110_env.py:141` |
| Integrator | RK4 | warning printed at `base_classes.py:95` |

## 2. Vehicle model inside the simulator

- Above 0.5 m/s the simulator uses a **dynamic single-track model** with slip angle and
  yaw rate as states. Below 0.5 m/s it switches to a **kinematic** model
  (`dynamic_models.py:152`, `if abs(x[3]) < 0.5`).
- The tire forces in the dynamic model are **linear in slip angle**. The equations contain
  only terms proportional to the yaw rate, the slip angle and the steering angle, with no
  saturation. The simulated tires therefore never reach a friction limit.
- The cornering coefficients `C_Sf`, `C_Sr` are **normalised** [1/rad]. The lateral axle
  force is `mu * C_S * Fz * alpha`, so the stiffness in N/rad is `mu * C_S * Fz`:

| Quantity | Front | Rear |
|----------|-------|------|
| Static axle load Fz [N] | 19.05 | 17.64 |
| Cornering stiffness [N/rad] | 94.3 | 100.9 |

Using `C_S` directly as N/rad gives a model about 20 times too soft. This is covered by
`tests/test_vehicle.py`.

## 3. What the simulator reports

| Observation | Meaning | Source |
|-------------|---------|--------|
| `poses_x`, `poses_y` | position | `base_classes.py:605-606` |
| `poses_theta` | yaw angle `state[4]` | `base_classes.py:607` |
| `linear_vels_x` | **total speed `v`** (`state[3]`), not the body-frame x velocity | `base_classes.py:608` |
| `linear_vels_y` | **always 0** | `base_classes.py:609` |
| `ang_vels_z` | yaw rate | observation key |
| slip angle `state[6]` | **not published** | not in the observation dictionary |

The ROS 2 bridge copies these into `/ego_racecar/odom`, so `twist.linear.y` is always 0
and the slip angle is not available to a ROS node.

## 4. Collisions

The simulator checks the lidar scan for an imminent collision (`check_ttc_jit`,
`base_classes.py:243`). When it triggers, it executes `self.state[3:] = 0.`
(`base_classes.py:247`): speed, yaw angle, yaw rate and slip angle are all set to zero,
and `env.step` returns `done=True`. The position is kept, so the car stays where it
crashed, with heading 0.

## 5. Measured behaviour (Levine map, start at the origin)

Setup: speed command 2 m/s, 100 Hz steps, `gym.make('f110_gym:f110-v0', ...)`.

| Steering | Result |
|----------|--------|
| 0.0 rad | speed 1.82 m/s at 0.5 s, 1.98 m/s at 1.0 s, 2.00 m/s from 1.5 s; no collision over 3 s |
| 0.2 rad | at 0.5 s: heading 0.353 rad, yaw rate 1.087 rad/s, speed 1.82 m/s. Collision at 0.77 s at (1.02 m, 0.43 m), `done=True`, speed and heading reset to 0 |

**Yaw rate versus the kinematic formula.** With wheelbase L = 0.3302 m, the kinematic
bicycle gives `v * tan(delta) / L = 1.82 * tan(0.2) / 0.3302 = 1.117 rad/s`. The
simulator reports 1.087 rad/s, about 3% lower. At this speed and steering angle the
dynamic model differs only slightly from the kinematic one.

## 6. ROS 2 bridge (`gym_bridge_launch.py`)

- Starts five processes: the bridge, RViz, the map server, its lifecycle manager, and the
  robot state publishers.
- Publishes `/scan` and `/ego_racecar/odom`. Subscribes to `/drive`
  (`ackermann_msgs/AckermannDriveStamped`), `/initialpose` (RViz "2D Pose Estimate"
  resets the car), and `/cmd_vel` (keyboard teleoperation).
- The map is `levine`, loaded from `/sim_ws/src/f1tenth_gym_ros/maps/levine`, with the car
  starting at (0, 0, 0).
- In WSLg, RViz needs `LIBGL_ALWAYS_SOFTWARE=1` (set in `docker/docker-compose.yml`).
  Without it RViz logs a GLSL shader error from the map display.

## 7. Consequences for the controller (Task 2)

1. The prediction model takes its parameters from `config/vehicle.yaml` with the N/rad
   conversion above.
2. The simulator gives `v` and the yaw rate but never `v_y` or the slip angle, so the
   controller's initial state has to be built from what is published.
3. The commands are speed and steering setpoints. An MPC acceleration output cannot be
   applied directly and has to be turned into a speed setpoint.
4. The simulated tires do not saturate, so any friction-circle constraint is a design
   choice of the controller, not something the plant enforces.
5. Every closed-loop run must stop when `done` is `True`.

## 8. Reproduce

Inside the container (`docker compose -f docker/docker-compose.yml run --rm nmpc`):

```bash
cd /opt/f1tenth_gym/gym/f110_gym/envs
grep -n "timestep" f110_env.py | head -5
grep -n "abs(x\[3\])" dynamic_models.py
grep -n "linear_vels_y" base_classes.py
grep -n "state\[3:\] = 0" base_classes.py
```

```bash
python3 - <<'EOF' 2>/dev/null
import gym, numpy as np
env = gym.make('f110_gym:f110-v0',
               map='/opt/f1tenth_gym/gym/f110_gym/envs/maps/levine',
               map_ext='.pgm', num_agents=1)
for steer in (0.0, 0.2):
    obs, *_ = env.reset(np.array([[0.0, 0.0, 0.0]]))
    print(f"--- steer = {steer} rad, speed command 2 m/s ---")
    for i in range(1, 301):
        obs, r, done, info = env.step(np.array([[steer, 2.0]]))
        if i % 50 == 0 or done:
            print(f"t={i*0.01:.2f}s x={obs['poses_x'][0]:.2f} y={obs['poses_y'][0]:.2f} "
                  f"theta={obs['poses_theta'][0]:.3f} vx={obs['linear_vels_x'][0]:.2f} "
                  f"wz={obs['ang_vels_z'][0]:.3f} collision={obs['collisions'][0]} done={done}")
        if done:
            break
EOF
```
