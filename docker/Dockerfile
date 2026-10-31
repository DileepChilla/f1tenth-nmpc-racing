# ROS 2 Humble + f1tenth_gym + CasADi.
# STATUS: builds and runs (Task 1). Image tag: f1tenth-nmpc:humble
FROM ros:humble-ros-base-jammy

SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        git python3-pip python3-colcon-common-extensions \
        libgl1 libglu1-mesa \
        ros-humble-ackermann-msgs ros-humble-rviz2 ros-humble-xacro \
        ros-humble-robot-state-publisher ros-humble-nav2-map-server \
        ros-humble-nav2-lifecycle-manager \
    && rm -rf /var/lib/apt/lists/*

# f1tenth_gym pins numpy<=1.22 and gym==0.19.0, so the numerics stack is pinned to match.
RUN pip3 install --no-cache-dir \
        "numpy==1.22.0" "numba==0.56.4" "scipy==1.8.1" "gym==0.19.0" \
        "pyglet<1.5" pyopengl transforms3d pyyaml \
        "casadi>=3.6,<3.8" "matplotlib==3.5.3" "pandas==1.5.3" pytest

# Simulator pinned to the commit used in the original project (v1).
ARG GYM_REF=4fdb9c7e6fb7c701290f4dc18377d07c1681724f
RUN git clone https://github.com/f1tenth/f1tenth_gym /opt/f1tenth_gym \
    && cd /opt/f1tenth_gym && git checkout ${GYM_REF} \
    && pip3 install --no-cache-dir -e .

# ROS 2 gym bridge (upstream main; matches the pinned f110_gym simulator)
ARG BRIDGE_REF=883394df0964c555ee05bea69c3002daf6f2d405
RUN apt-get update \
    && mkdir -p /sim_ws/src \
    && git clone https://github.com/f1tenth/f1tenth_gym_ros /sim_ws/src/f1tenth_gym_ros \
    && git -C /sim_ws/src/f1tenth_gym_ros checkout ${BRIDGE_REF} \
    && source /opt/ros/humble/setup.bash \
    && cd /sim_ws \
    && rosdep install -i --from-path src --rosdistro humble -y --skip-keys "python-transforms3d-pip" \
    && colcon build \
    && rm -rf /var/lib/apt/lists/*
RUN echo 'source /sim_ws/install/setup.bash' >> /root/.bashrc

WORKDIR /workspace/f1tenth-nmpc-racing
RUN echo 'source /opt/ros/humble/setup.bash' >> /root/.bashrc
CMD ["/bin/bash"]