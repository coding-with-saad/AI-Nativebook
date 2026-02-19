import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SimpleMover(Node):
    def __init__(self):
        super().__init__('simple_mover')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.5, self.publish_twist)
        self.get_logger().info('Simple Mover Node has been started.')

    def publish_twist(self):
        twist_msg = Twist()
        twist_msg.linear.x = 0.1  # Move forward
        twist_msg.angular.z = 0.0  # No rotation
        self.publisher_.publish(twist_msg)
        self.get_logger().info(f'Publishing Twist: linear.x={twist_msg.linear.x}')

def main(args=None):
    rclpy.init(args=args)
    simple_mover = SimpleMover()
    rclpy.spin(simple_mover)
    simple_mover.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
