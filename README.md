# SO-101 Hand Teleoperation

This repository combines laptop-based hand tracking with ROS 2 control of an
SO-101 robot arm.

## Repository layout

- `ai/hand_tracker`: Windows-compatible Python hand-tracking application.
- `ros2_ws`: Ubuntu 24.04 / ROS 2 Jazzy workspace for robot control.
- `shared`: Cross-platform message contracts and test samples.
- `docs`: Architecture, calibration, safety, and integration documentation.

## Ownership

- Dhanasekaren: AI, computer vision, and Windows application.
- Santhosh: ROS 2, MoveIt, hardware interface, and robot testing.

## Current status

The legacy ROS packages have been imported as the project baseline. They must
be stabilized and safety-tested before camera commands are connected to real
hardware.

Do not commit generated ROS build directories, Python environments, recordings,
or machine-specific configuration.

