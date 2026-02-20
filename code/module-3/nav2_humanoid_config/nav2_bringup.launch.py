import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Get the launch directory for Nav2
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    
    # Path to our custom Nav2 parameters
    nav2_params_path = os.path.join(
        get_package_share_directory('nav2_humanoid_config'), # Assuming a package for nav2_humanoid_config exists
        'nav2_params.yaml'
    )

    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_yaml_file = LaunchConfiguration('map', default=os.path.join(
        nav2_bringup_dir, 'maps', 'turtlebot3_world.yaml')) # Placeholder map
    
    # Example: Launching Nav2
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'map': map_yaml_file,
            'use_sim_time': use_sim_time,
            'params_file': nav2_params_path,
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument(
            'map',
            default_value=map_yaml_file,
            description='Full path to map file to load'),
        
        nav2_launch
    ])
