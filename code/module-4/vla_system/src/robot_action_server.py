#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time # For simulating action duration

class RobotActionServer(Node):
    def __init__(self):
        super().__init__('robot_action_server')
        self.cmd_vel_subscriber = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )
        self.cmd_vel_subscriber # prevent unused variable warning
        self.get_logger().info('Robot Action Server has been started.')

    def cmd_vel_callback(self, msg: Twist):
        self.get_logger().info(f'Received Twist command: Linear.x={msg.linear.x}, Angular.z={msg.angular.z}')
        # In a real robot, this would control motors.
        # For simulation, we just print and simulate a delay.
        if msg.linear.x > 0:
            self.get_logger().info("Robot moving forward...")
            # Simulate movement
            time.sleep(1)
        elif msg.angular.z > 0:
            self.get_logger().info("Robot turning left...")
            # Simulate movement
            time.sleep(1)
        else:
            self.get_logger().info("Robot stopped.")


def main(args=None):
    rclpy.init(args=args)
    robot_action_server = RobotActionServer()
    rclpy.spin(robot_action_server)
    robot_action_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
