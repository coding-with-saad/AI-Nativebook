# Chapter 2: Python Agents

An "agent" in ROS 2 is simply a Node that makes decisions. It takes inputs (sensors) and produces outputs (actuation or status) based on internal logic.

## The Smart Agent

Our `SmartAgent` monitors a temperature topic and decides if the system is overheating.

```python title="smart_agent.py"
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
```

## Running the Agent

1. Start the agent: `ros2 run ros2_basics_py smart_agent`
2. Publish simulated data manually:
   ```bash
   ros2 topic pub --once /temperature std_msgs/msg/Float32 "{data: 35.0}"
   ```
3. Observe the logs. It should warn about overheating.
