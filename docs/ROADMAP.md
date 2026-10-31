# Roadmap

Course: Automated Driving and Driver Assistance Systems, WHZ (Prof. Voßwinkel).
Assignment: MPC for racing-line tracking with a dynamic bicycle model in F1TENTH Gym.
Final deliverable: 20-minute live code demo + 10 minutes questions.


## Assignment tasks → where they live

| Task | Requirement | Repo location |
|------|-------------|---------------|
| 1 | Theory: MPC, dynamic bicycle model, F1TENTH Gym | `docs/theory.md`, `docs/gym_notes.md` |
| 2 | Formulation: cost, dynamics, actuator limits, friction circle | `docs/formulation.md`, `src/nmpc_racing/mpc.py` |
| 3 | Implementation in ROS 2 with CasADi, real-time considerations | `src/nmpc_racing/`, `ros2/` |
| 4 | Closed loop with F1TENTH Gym | `scripts/run_offline.py`, `ros2/` |
| 5 | Tuning (horizon, weights) and validation at several speeds | `config/mpc.yaml`, `results/` |
| 6 | Documentation and comparative evaluation | `docs/report.md`, `results/` |

## Weekly push schedule (Sundays)

| Week | Push date | Content | Task |
|------|-----------|---------|------|
| 0 | Sat 31 Oct | Repository skeleton, vehicle parameters with unit-tested cornering stiffness | 1 |
| 1 | 8 Nov | Docker image builds; gym smoke test (car drives, scan and odom visible) | 1, 4 |
| 2 | 15 Nov | `docs/theory.md`: MPC basics, single-track derivation from the lecture notes | 1 |
| 3 | 22 Nov | Model validation: lecture bicycle model vs gym model, step and sine steer plots | 1, 2 |
| 4 | 29 Nov | Track data: centreline and widths for the chosen map | 2 |
| 5 | 6 Dec | Racing line from the minimum-curvature optimiser, plot | 2 |
| 6 | 13 Dec | Speed profile and reference sampling, Frenet errors, unit tests | 2 |
| 7 | 20 Dec | `docs/formulation.md` and the CasADi NLP; one solve checked against hand calculation | 2, 3 |
| 8 | 27 Dec | Offline closed loop at low speed: first full lap | 3, 4 |
| 9 | 3 Jan | Friction circle and steering-rate constraints; acceleration command applied | 3 |
| 10 | 10 Jan | Weight tuning with rationale; solve-time profiling | 5 |
| 11 | 17 Jan | Horizon study and validation at several speeds | 5 |
| 12 | 24 Jan | ROS 2 node, launch file, YAML parameters | 3 |
| 13 | 31 Jan | ROS 2 closed loop in the gym, RViz visualisation, timing in ROS | 3, 4 |
| 14 | 7 Feb | Pure Pursuit baseline and evaluation scripts | 6 |
| 15 | 14 Feb | Results: lap time, RMS and max lateral error, p50/p95 solve time, GIF | 6 |
| 16 | 21 Feb | `docs/report.md` and final README | 6 |
| 17 | 28 Feb | Tag `v1.0`, demo rehearsal, LinkedIn post | 6 |

