# F1TENTH NMPC Racing

Nonlinear Model Predictive Control for racing-line tracking on a 1:10 scale F1TENTH car,
using a dynamic bicycle model, CasADi/IPOPT, ROS 2 Humble and the F1TENTH Gym.

Course project: *Automated Driving and Driver Assistance Systems*, Westsächsische
Hochschule Zwickau (Prof. Dr.-Ing. Rick Voßwinkel).

> **Status:** work in progress, updated weekly. See [docs/ROADMAP.md](docs/ROADMAP.md).

## Goals

- Track a pre-computed racing line with an NMPC based on a dynamic bicycle model.
- Respect steering, speed and friction-circle constraints.
- Run in real time (control period 50 ms) and in ROS 2.
- Report tracking error, solve time and constraint handling at several speeds.

## Repository layout

```
config/      vehicle and (later) MPC parameters
docker/      Dockerfile and compose file (ROS 2 Humble + gym + CasADi)
docs/        roadmap, design decisions, theory, formulation, report
ros2/        ROS 2 wrapper package (added Week 12)
results/     curated plots, tables and videos
scripts/     offline simulation and evaluation scripts
src/         nmpc_racing Python package (no ROS dependency)
tests/       unit tests
tracks/      track and racing-line data
```

## Quick start

```bash
git clone https://github.com/DileepChilla/f1tenth-nmpc-racing.git
cd f1tenth-nmpc-racing
make build     # build the Docker image
make shell     # open a shell in the container
make test      # inside the container: run unit tests
```

## Results

Added in Weeks 14–16.

## Design decisions

See [docs/DECISIONS.md](docs/DECISIONS.md).

## License

MIT
