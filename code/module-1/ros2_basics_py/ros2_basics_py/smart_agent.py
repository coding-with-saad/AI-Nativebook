import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String


class SmartAgent(Node):

    def __init__(self):
        super().__init__('smart_agent')
        self.subscription = self.create_subscription(
            Float32,
            'temperature',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(String, 'status', 10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Received temperature: "%f"' % msg.data)

        status_msg = String()
        if msg.data > 30.0:
            status_msg.data = 'WARNING: Overheating!'
            self.get_logger().warn(status_msg.data)
        else:
            status_msg.data = 'NOMINAL'
            self.get_logger().info(status_msg.data)

        self.publisher_.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)

    smart_agent = SmartAgent()

    rclpy.spin(smart_agent)

    smart_agent.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
