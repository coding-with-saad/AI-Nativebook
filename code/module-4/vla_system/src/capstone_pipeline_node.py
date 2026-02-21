#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String # Placeholder for perception data

class CapstonePipelineNode(Node):
    def __init__(self):
        super().__init__('capstone_pipeline_node')
        self.perception_subscription = self.create_subscription(
            String,
            'perception_output', # Topic for perception data from Module 3
            self.perception_callback,
            10
        )
        self.perception_subscription # prevent unused variable warning

        self.llm_command_publisher = self.create_publisher(String, 'high_level_command', 10)
        self.get_logger().info('Capstone Pipeline Node has been started.')
        self.get_logger().info('Ready to integrate perception outputs from Module 3.')

    def perception_callback(self, msg: String):
        self.get_logger().info(f'Received perception output: "{msg.data}"')

        # Reactive Planning and Error Recovery Logic
        if "obstacle detected" in msg.data.lower():
            self.get_logger().warn("Obstacle detected! Initiating reactive planning...")
            replan_command = String()
            replan_command.data = f"Re-plan path to goal, avoiding {msg.data}. Current goal is [CURRENT_GOAL_PLACEHOLDER]"
            self.llm_command_publisher.publish(replan_command)
            self.get_logger().info(f"Published re-plan command: '{replan_command.data}'")
        elif "task failed" in msg.data.lower():
            self.get_logger().error("Task reported failed. Initiating error recovery...")
            # For demonstration, a simple recovery action. In a real system, this could be
            # a more complex sequence or another LLM call for recovery strategies.
            recovery_command = String()
            recovery_command.data = "Execute predefined recovery sequence: back up 1 meter and try again."
            self.llm_command_publisher.publish(recovery_command) # Sending a recovery command to LLM planner
            self.get_logger().info(f"Published recovery command: '{recovery_command.data}'")
        else:
            self.get_logger().info("No immediate reactive planning or error recovery needed based on perception.")
            # In a real scenario, this data would be processed and fed into the LLM planning
            # or directly used for proactive adjustments.


def main(args=None):
    rclpy.init(args=args)
    capstone_pipeline_node = CapstonePipelineNode()
    rclpy.spin(capstone_pipeline_node)
    capstone_pipeline_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
