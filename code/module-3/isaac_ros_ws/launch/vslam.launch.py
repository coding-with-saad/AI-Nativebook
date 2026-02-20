import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Get the launch directory
    vslam_package_share_directory = get_package_share_directory('my_vslam_node')
    
    # Example: Launching the custom VSLAM node
    my_vslam_node = Node(
        package='my_vslam_node',
        executable='vslam_node',
        name='vslam_node',
        output='screen',
        parameters=[{
            # Example parameters (replace with actual Isaac ROS VSLAM parameters)
            'use_sim_time': True,
            'stereo_camera_namespace': '/stereo_camera',
            'imu_topic': '/imu/data',
        }],
    )

    # Example: In a real scenario, you might launch Isaac ROS VSLAM nodes
    # For instance:
    # isaac_ros_vslam_node = Node(
    #     package='isaac_ros_visual_slam',
    #     executable='visual_slam_node',
    #     name='visual_slam_node',
    #     output='screen',
    #     parameters=[os.path.join(
    #         get_package_share_directory('isaac_ros_visual_slam'), 'params', 'vslam_params.yaml'
    #     )],
    # )

    return LaunchDescription([
        my_vslam_node,
        # isaac_ros_vslam_node # Uncomment and configure for actual Isaac ROS VSLAM node
    ])
