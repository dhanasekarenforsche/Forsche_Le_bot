# Hand Observation Protocol

This document defines the boundary between the Windows vision application and
the Ubuntu ROS 2 system. The initial transport will be UDP JSON over a trusted
local network.

## Version 1 observation

Required fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `version` | integer | Protocol version; initially `1` |
| `sequence` | integer | Monotonically increasing observation number |
| `timestamp_ms` | integer | Vision capture timestamp for diagnostics |
| `tracking` | boolean | Whether a valid hand is currently tracked |
| `confidence` | number | Detection confidence from `0.0` to `1.0` |
| `handedness` | string | `left`, `right`, or `unknown` |
| `palm_x` | number | Normalized horizontal image coordinate from `0.0` to `1.0` |
| `palm_y` | number | Normalized vertical image coordinate from `0.0` to `1.0` |
| `palm_size` | number | Palm width normalized by image width |
| `pinch_ratio` | number | Thumb-index distance divided by palm width |
| `palm_roll` | number | Optional estimated in-plane rotation in radians |
| `fps` | number | Current vision processing rate |

The AI application must continue sending `tracking: false` observations when no
hand is detected. The ROS receiver owns timeouts, neutral calibration, robot
coordinates, velocity scaling, workspace limits, arming, and emergency stops.

