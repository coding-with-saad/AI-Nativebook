#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist # Example for robot movement commands

class ActionMapperNode(Node):
    def __init__(self):
        super().__init__('action_mapper_node')
        self.subscription = self.create_subscription(
            String,
            'transcribed_text',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10) # Example publisher for robot movement
        self.get_logger().info('Action Mapper Node has been started.')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received transcribed text: "{msg.data}"')
        # Here, implement logic to map transcribed text to robot commands
        # For now, we'll just publish a dummy Twist message
        twist_msg = Twist()
        if "move forward" in msg.data.lower():
            twist_msg.linear.x = 0.5
            self.get_logger().info('Mapped to: Move Forward')
        elif "turn left" in msg.data.lower():
            twist_msg.angular.z = 0.5
            self.get_logger().info('Mapped to: Turn Left')
        else:
            self.get_logger().info('No specific action mapped.')
            
        self.publisher_.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    action_mapper_node = ActionMapperNode()
    rclpy.spin(action_mapper_node)
    action_mapper_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
