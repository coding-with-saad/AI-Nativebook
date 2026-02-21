from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='vla_system',
            executable='llm_planner_node.py',
            name='llm_planner_node',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'llm_model': 'gpt-4'} # Example parameter
            ]
        ),
    ])
