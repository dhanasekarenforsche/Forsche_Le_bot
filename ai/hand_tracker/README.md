# Hand Tracker

Windows-compatible Python application owned by Dhanasekaren.

Initial scope:

- Capture frames from the laptop webcam.
- Detect and track one hand.
- Calculate normalized palm position, palm size, confidence, handedness, and
  pinch ratio.
- Display a diagnostic preview.
- Produce observations that conform to `shared/protocol.md`.

This component must not calculate robot joint angles or bypass the ROS-side
safety supervisor.

