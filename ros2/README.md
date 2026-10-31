# ros2/

ROS 2 wrapper around the `nmpc_racing` package. Added in Week 12.
The wrapper subscribes to odometry, calls the controller, and publishes
`ackermann_msgs/AckermannDriveStamped` plus RViz paths. No control logic lives here.
