# Chapter 1: ROS 2 Basics

The nervous system of an intelligent robot relies on robust communication. In ROS 2, this is achieved through the **Graph**, a network of Nodes communicating via Topics and Services.

## Nodes: The Neurons

A Node is the fundamental unit of computation.

```python title="simple_publisher.py"
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SimplePublisher(Node):

    def __init__(self):
        super().__init__('simple_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
```

## Topics: The Axons (Pub/Sub)

Topics facilitate asynchronous streaming of data.

```python title="simple_subscriber.py"
class SimpleSubscriber(Node):

    def __init__(self):
        super().__init__('simple_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
```

## Services: Synaptic Request/Response

Services allow for synchronous remote procedure calls, useful for actions like "Compute this path" or "Turn on the gripper".

### Server

```python title="service_server.py"
    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))

        return response
```

### Client

```python title="service_client.py"
    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
```

## Hands On

1. Build the module: `colcon build --symlink-install`
2. Source: `source install/setup.bash`
3. Run: `ros2 run ros2_basics_py simple_publisher`
