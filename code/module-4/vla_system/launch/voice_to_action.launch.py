from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='audio_interface',
            executable='whisper_node.py',
            name='whisper_node',
            output='screen',
            emulate_tty=True
        ),
        Node(
            package='vla_system',
            executable='action_mapper_node.py',
            name='action_mapper_node',
            output='screen',
            emulate_tty=True
        ),
        Node(
            package='vla_system',
            executable='robot_action_server.py',
            name='robot_action_server',
            output='screen',
            emulate_tty=True
        ),
    ])
