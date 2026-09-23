#!/usr/bin/env python3
"""
Move the SO-ARM-100 robot arm using FollowJointTrajectory action client.
This version waits for controllers and performs a simple "hi" motion.
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from control_msgs.msg import JointTolerance
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time

# ── CONFIGURATION ────────────────────────────────────────────────────────────
ARM_JOINTS    = ["joint1", "joint2", "joint3", "joint4", "joint5"]
GRIPPER_JOINTS = ["joint6"]

# "Hi" motion positions (radians)
HI_POSITIONS_SEQ = [
    [0.0, -0.5, 0.5, 0.0, 0.0],  # initial
    [0.2, -0.4, 0.6, 0.0, 0.0],  # wave
    [0.0, -0.5, 0.5, 0.0, 0.0]   # back to initial
]

GRIPPER_POS = [0.5]  # keep gripper half-closed

TRAVEL_TIME_SEC = 2
# ─────────────────────────────────────────────────────────────────────────────

def make_tolerances(joint_names, position_tol=0.2, velocity_tol=0.5, accel_tol=0.5):
    tolerances = []
    for name in joint_names:
        t = JointTolerance()
        t.name = name
        t.position = position_tol
        t.velocity = velocity_tol
        t.acceleration = accel_tol
        tolerances.append(t)
    return tolerances


class ArmMover(Node):
    def __init__(self):
        super().__init__("arm_debug_mover")
        self._arm_client = ActionClient(self, FollowJointTrajectory,
                                        "/arm_controller/follow_joint_trajectory")
        self._gripper_client = ActionClient(self, FollowJointTrajectory,
                                           "/gripper_controller/follow_joint_trajectory")

    def wait_for_controllers(self, timeout_sec=10):
        self.get_logger().info("Checking controller availability...")
        start_time = time.time()
        while (time.time() - start_time) < timeout_sec:
            arm_ready = self._arm_client.wait_for_server(timeout_sec=1.0)
            grip_ready = self._gripper_client.wait_for_server(timeout_sec=1.0)
            if arm_ready and grip_ready:
                self.get_logger().info("✅ Controllers are available!")
                return True
            self.get_logger().warn("Waiting for controllers to start...")
        self.get_logger().error("❌ Controllers NOT available! Start hardware first.")
        return False

    def _send_goal(self, client, joint_names, positions, travel_sec):
        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names = joint_names

        point = JointTrajectoryPoint()
        point.positions = list(positions)
        point.time_from_start = Duration(sec=travel_sec)
        goal.trajectory.points = [point]

        goal.goal_tolerance = make_tolerances(joint_names, position_tol=0.3)
        goal.path_tolerance = []
        goal.goal_time_tolerance = Duration(sec=15)

        def dummy_feedback_cb(feedback_msg):
            pass

        self.get_logger().info(f"Moving: {dict(zip(joint_names, positions))}")
        future = client.send_goal_async(goal, feedback_callback=dummy_feedback_cb)
        rclpy.spin_until_future_complete(self, future)
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error("Goal REJECTED by controller!")
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result = result_future.result()
        if result.status == 4:
            self.get_logger().info("Motion SUCCEEDED!")
            return True
        else:
            self.get_logger().warn(f"Motion finished with status: {result.status}")
            return False

    def wave_hi(self):
        for pos in HI_POSITIONS_SEQ:
            success = self._send_goal(self._arm_client, ARM_JOINTS, pos, TRAVEL_TIME_SEC)
            if not success:
                self.get_logger().warn("Stopping hi-motion due to failure.")
                break
            time.sleep(0.5)  # pause between positions

    def move_gripper(self):
        return self._send_goal(self._gripper_client, GRIPPER_JOINTS,
                               GRIPPER_POS, 2)


def main(args=None):
    rclpy.init(args=args)
    node = ArmMover()

    if not node.wait_for_controllers():
        node.destroy_node()
        rclpy.shutdown()
        return

    node.wave_hi()
    node.move_gripper()
    node.get_logger().info("Done waving hi!")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()