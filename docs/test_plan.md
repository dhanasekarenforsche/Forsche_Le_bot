# Test Plan

Testing progresses through four gates:

1. Vision-only validation on Windows.
2. ROS package and hardware-interface validation on Ubuntu.
3. Network integration with RViz or mock hardware.
4. Restricted-speed testing on the physical robot.

Physical testing is not permitted until joint directions, calibrated limits,
command clamping, feedback freshness, and stop behavior have been verified.

