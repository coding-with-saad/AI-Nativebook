---
sidebar_position: 4
---

# Sim-to-Real Validation and ROS Integration

This chapter focuses on the crucial steps of validating your digital twin against real-world data and integrating it with ROS 2 for control and perception.

## Validating with Real-World Data

The "sim-to-real gap" refers to the discrepancies between simulated and real-world robot behavior. Closing this gap is vital for effective digital twins.

We've developed a basic Python script (`code/module-2/scripts/compare_sensors.py`) to help you compare simulated sensor data with real-world logs. This script provides a starting point for quantitative analysis of simulation fidelity.

### Usage:

```bash
python3 code/module-2/scripts/compare_sensors.py --sim <path_to_sim_log.csv> --real <path_to_real_log.csv>
```

This script will read and perform a basic comparison of the two CSV files. For a more in-depth analysis, you would typically:
-   Synchronize timestamps between datasets.
-   Calculate metrics like Root Mean Squared Error (RMSE) or correlation coefficients.
-   Visualize data overlays to identify discrepancies.

## ROS 2 Integration

ROS 2 provides a powerful framework for robotic control and communication. Integrating your Gazebo digital twin with ROS 2 allows you to use the same control algorithms in both simulation and on physical robots.

The `ros_gz_bridge` package facilitates this integration by bridging topics between ROS 2 and Gazebo. We've set up a basic configuration in `code/module-2/config/ros_gz_bridge.yaml`:

```yaml
# code/module-2/config/ros_gz_bridge.yaml
# ... (full content of ros_gz_bridge.yaml) ...
```

This configuration bridges common topics such as motor commands (`/cmd_vel`) from ROS 2 to Gazebo, and sensor data (LiDAR `/scan`, Depth Camera `/depth/image_raw`, IMU `/imu`) from Gazebo to ROS 2.

### Simple ROS 2 Control Node

We've implemented a simple Python ROS 2 node (`code/module-2/ros2_nodes/simple_mover.py`) that publishes `Twist` messages to move the robot.

```python
# code/module-2/ros2_nodes/simple_mover.py
# ... (full content of simple_mover.py) ...
```

To use this node, you would typically launch it alongside Gazebo and the `ros_gz_bridge`. This allows you to command your simulated robot using ROS 2, enabling the development and testing of robotic control algorithms within your digital twin environment.
