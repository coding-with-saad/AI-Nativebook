---
sidebar_position: 3
---

# Nav2 Path Planning for Humanoids: Autonomous Movement

This chapter delves into Nav2 for advanced path planning and navigation for humanoid robots, enabling them to move autonomously in complex environments.

## Nav2 for Complex Kinematics

Nav2, the ROS 2 navigation stack, is highly configurable and can be adapted for non-differential drive robots like humanoids. This involves selecting appropriate local controllers and global planners that can handle the unique kinematic and dynamic constraints of a humanoid.

### Nav2 Parameter Configuration

The `nav2_params.yaml` file (`code/module-3/nav2_humanoid_config/nav2_params.yaml`) contains the key parameters for configuring Nav2 for a humanoid robot.

```yaml
# code/module-3/nav2_humanoid_config/nav2_params.yaml
# Nav2 Parameters for Humanoid Robots

# Global parameters
nav2_controller:
  ros__parameters:
    use_sim_time: True
    min_turning_radius: 0.2
    max_linear_vel: 0.2
    max_angular_vel: 0.5
    transform_tolerance: 0.1

# Controller Server (e.g., TEB Local Planner)
  controller_server:
    ros__parameters:
      controller_plugin_ids: ["FollowPath"]
      controller_plugin_types: ["teb_local_planner/TebLocalPlannerROS"]
      # TEB-specific parameters (example)
      TebLocalPlannerROS:
        max_vel_x: 0.2
        max_vel_theta: 0.5
        acc_lim_x: 0.5
        acc_lim_theta: 0.8
        min_obstacle_dist: 0.3

# Planner Server (e.g., Smac Hybrid-A* Planner)
nav2_planner:
  ros__parameters:
    use_sim_time: True
    planner_plugin_ids: ["GridBased"]
    planner_plugin_types: ["nav2_smac_planner/SmacPlannerHybrid"]
    # SmacPlannerHybrid-specific parameters (example)
    SmacPlannerHybrid:
      allow_unknown: true
      max_iterations: 1000
      max_on_approach_iterations: 100
```

Key considerations include setting appropriate velocity limits (`max_linear_vel`, `max_angular_vel`), defining the robot's footprint, and choosing a planner suitable for complex kinematics, such as the `SmacPlannerHybrid`.

### Launching the Nav2 Stack

The `nav2_bringup.launch.py` file (`code/module-3/nav2_humanoid_config/nav2_bringup.launch.py`) is used to start the entire Nav2 stack with our custom parameters.

```python
# code/module-3/nav2_humanoid_config/nav2_bringup.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    
    nav2_params_path = os.path.join(
        get_package_share_directory('nav2_humanoid_config'),
        'nav2_params.yaml'
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'map': LaunchConfiguration('map', default=os.path.join(nav2_bringup_dir, 'maps', 'turtlebot3_world.yaml')),
            'use_sim_time': LaunchConfiguration('use_sim_time', default='true'),
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
            default_value=LaunchConfiguration('map', default=os.path.join(nav2_bringup_dir, 'maps', 'turtlebot3_world.yaml')),
            description='Full path to map file to load'),
        
        nav2_launch
    ])
```

To use this, you would typically build your ROS 2 workspace, source it, and then use `ros2 launch nav2_humanoid_config nav2_bringup.launch.py`. With Nav2 properly configured, your humanoid robot can autonomously plan paths and avoid obstacles in its simulated environment.
