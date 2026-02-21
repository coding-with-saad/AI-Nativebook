from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    vla_system_share_dir = get_package_share_directory('vla_system')

    # Include the voice_to_action.launch.py
    voice_to_action_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vla_system_share_dir, 'launch', 'voice_to_action.launch.py')
        )
    )

    # Include the llm_planning.launch.py
    llm_planning_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(vla_system_share_dir, 'launch', 'llm_planning.launch.py')
        )
    )

    # Launch the capstone_pipeline_node
    capstone_pipeline_node = Node(
        package='vla_system',
        executable='capstone_pipeline_node.py',
        name='capstone_pipeline_node',
        output='screen',
        emulate_tty=True,
    )

    return LaunchDescription([
        voice_to_action_launch,
        llm_planning_launch,
        capstone_pipeline_node,
    ])
