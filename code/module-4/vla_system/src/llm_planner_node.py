#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from vla_system.llm_interface import llm_inference
from vla_system.llm_prompts import TASK_DECOMPOSITION_PROMPT, FUNCTION_CALL_PROMPT

class LLMPlannerNode(Node):
    def __init__(self):
        super().__init__('llm_planner_node')
        self.declare_parameter('llm_model', 'gpt-4')
        self.llm_model = self.get_parameter('llm_model').get_parameter_value().string_value

        self.subscription = self.create_subscription(
            String,
            'high_level_command', # Topic for high-level commands
            self.command_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        self.action_publisher = self.create_publisher(String, 'robot_actions', 10) # Topic for publishing LLM-generated actions
        self.get_logger().info(f'LLM Planner Node started with model: {self.llm_model}.')

    def command_callback(self, msg):
        high_level_command = msg.data
        self.get_logger().info(f'Received high-level command: "{high_level_command}"')

        # 1. Task Decomposition using LLM
        decomposition_prompt = TASK_DECOMPOSITION_PROMPT.format(command=high_level_command)
        decomposed_tasks_str = llm_inference(decomposition_prompt, self.llm_model)
        self.get_logger().info(f'Decomposed tasks: {decomposed_tasks_str}')

        decomposed_tasks = [task.strip() for task in decomposed_tasks_str.split('- ') if task.strip()]

        # 2. Convert decomposed tasks to function calls
        for sub_task in decomposed_tasks:
            function_call_prompt = FUNCTION_CALL_PROMPT.format(sub_task=sub_task)
            function_call = llm_inference(function_call_prompt, self.llm_model)
            self.get_logger().info(f'Generated function call for "{sub_task}": {function_call}')
            
            # Publish the function call as an action
            action_msg = String()
            action_msg.data = function_call
            self.action_publisher.publish(action_msg)
            self.get_logger().info(f'Published action: {function_call}')
            # TODO: In a full implementation, this would involve a ROS 2 Action Client
            # to send goals to an Action Server for execution.


def main(args=None):
    rclpy.init(args=args)
    llm_planner_node = LLMPlannerNode()
    rclpy.spin(llm_planner_node)
    llm_planner_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
