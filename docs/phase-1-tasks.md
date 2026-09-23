# Phase 1 — Independent Baselines

## Goal

Prove the Windows vision pipeline and Ubuntu ROS baseline independently. Do not
connect the two systems and do not perform robot motion in this phase.

## Schedule and deadline

- Start: Thursday, 24 September 2026
- Capacity: 2 focused hours per person per day
- AI-1 estimate: 6–8 focused hours (3–4 working days)
- ROS-1 estimate: 8–10 focused hours (4–5 working days)
- Midpoint checkpoint: Monday, 28 September 2026
- Final deadline: Wednesday, 30 September 2026, end of day IST

Both tasks run in parallel. At the midpoint checkpoint, report completed work,
test results, remaining work, and blockers. Raise a blocker on the same day it
is found; do not wait until the deadline.

## What to study

### Dhanasekaren

Read only:

- `README.md`
- `docs/architecture.md`
- `shared/protocol.md`

You do not need to study the ROS hardware implementation in Phase 1.

### Santhosh

Read:

- `ros2_ws/src/so_arm_100_hardware/src/so_arm_100_interface.cpp`
- `ros2_ws/src/so_arm_100_hardware/urdf/so101.urdf.xacro`
- Both packages' launch files, `package.xml` files, and controller YAML files
- `ros2_ws/src/lerobot_moveit/config/so101.srdf`
- `ros2_ws/src/lerobot_moveit/config/kinematics.yaml`

## Dhanasekaren — Task AI-1

Branch: `ai/phase-1-hand-tracker`

### Inputs

- Windows laptop
- Laptop webcam
- Python environment
- `shared/protocol.md`

### Work

1. Capture webcam frames with OpenCV.
2. Track exactly one hand with MediaPipe.
3. Draw landmarks and status on the preview.
4. Calculate `tracking`, `confidence`, `handedness`, `palm_x`, `palm_y`,
   `palm_size`, `pinch_ratio`, `palm_roll`, and `fps`.
5. Produce one protocol-compatible observation per processed frame.
6. Produce `tracking: false` observations while the hand is missing.
7. Test normal light, low light, fast movement, occlusion, and hand loss.

### Required outputs

- Python source under `ai/hand_tracker/`
- Dependency file
- Updated AI README with run instructions
- A short sample JSONL file under `shared/sample_messages/`
- Reported average FPS and observed problems

### Done when

- Preview is stable.
- One hand tracks consistently.
- Pinch ratio changes predictably.
- Hand loss does not crash the application.
- Average processing speed is at least 20 FPS.

### Do not do

- No UDP networking
- No ROS installation
- No robot coordinates, velocities, or joint angles

## Santhosh — Task ROS-1

Branch: `ros/phase-1-baseline`

### Inputs

- Ubuntu 24.04 with ROS 2 Jazzy
- SO-101 robot and serial connection
- Existing ROS packages in `ros2_ws/src/`

### Work

1. Record Ubuntu, ROS 2, MoveIt, and `ros2_control` versions.
2. Run a clean dependency check and build.
3. Validate Xacro expansion, URDF, SRDF, joint names, and controller names.
4. Fix the malformed hardware plugin XML.
5. Identify the serial device and servo IDs without commanding movement.
6. Document each joint's ROS name, servo ID, direction, current ticks, and
   known minimum, center, and maximum ticks.
7. Record every build and launch warning.

### Required outputs

- Valid hardware plugin XML
- Successful clean build, or exact unresolved errors
- `docs/ros-baseline-report.md`
- Joint-to-servo and limit table in that report
- List of modified files and reasons

### Done when

- Both ROS packages build.
- Xacro produces a valid robot description.
- Plugin XML is valid.
- Serial port and servo mapping are known.
- No unexpected robot motion occurred.

### Do not do

- No hand-tracking integration
- No MoveIt Servo integration
- No changes to calibration formulas or physical limits
- No automatic or test motion

## What to return to the Team Lead

Each developer returns:

1. Branch name and commit hash.
2. Required output files.
3. Test results.
4. Errors or blockers.
5. Files changed.

Phase 2 starts only after both Phase 1 submissions are reviewed.
