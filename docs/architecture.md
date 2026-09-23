# Architecture

The Windows application performs camera capture and hand-landmark inference. It
sends normalized, robot-independent observations over the local network.

The Ubuntu ROS 2 system validates packet freshness, applies the safety state
machine, maps hand displacement into robot-frame commands, and passes permitted
commands through MoveIt Servo and `ros2_control` to the existing serial hardware
interface.

Only the ROS 2 side may produce physical robot commands. Hand-tracking loss,
stale network input, invalid robot feedback, a MoveIt fault, or deadman release
must result in a safe hold.

