---
sidebar_position: 3
---

# Sensor Simulation: Perceiving the Digital World

This chapter delves into sensor simulation techniques for Digital Twin environments, allowing your robot to perceive its virtual surroundings. We'll focus on LiDAR, Depth Cameras, and IMUs.

## Integrating Sensors in Gazebo

We've added various virtual sensors to our `humanoid_robot` model in `code/module-2/gazebo/models/humanoid_robot/model.sdf`. This includes:

### LiDAR Sensor

A LiDAR (Light Detection and Ranging) sensor provides distance measurements by emitting laser pulses and measuring the time it takes for them to return. This creates a "point cloud" representation of the environment.

```xml
<!-- Excerpt from code/module-2/gazebo/models/humanoid_robot/model.sdf -->
    <sensor name="lidar" type="ray">
      <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
        <ros>
          <argument>~/out:=scan</argument>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
        <frame_name>lidar_link</frame_name>
      </plugin>
    </sensor>
```

### Depth Camera

A depth camera provides depth information for each pixel in an image, typically using technologies like structured light or time-of-flight. This is crucial for object recognition and 3D mapping.

```xml
<!-- Excerpt from code/module-2/gazebo/models/humanoid_robot/model.sdf -->
    <sensor name="depth_camera" type="depth_camera">
      <plugin name="depth_camera_controller" filename="libgazebo_ros_depth_camera.so">
        <ros>
          <argument>~/image_raw:=depth/image_raw</argument>
          <argument>~/image_depth:=depth/image_depth</argument>
          <argument>~/points:=depth/points</argument>
        </ros>
        <frame_name>depth_camera_link</frame_name>
      </plugin>
    </sensor>
```

### IMU Sensor

An IMU (Inertial Measurement Unit) measures linear acceleration and angular velocity, providing information about the robot's motion and orientation. Our IMU includes a Gaussian noise model for more realistic simulation.

```xml
<!-- Excerpt from code/module-2/gazebo/models/humanoid_robot/model.sdf -->
    <sensor name="imu_sensor" type="imu">
      <imu>
        <orientation>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
              <bias_mean>0.0000075</bias_mean>
              <bias_stddev>0.0000008</bias_stddev>
            </noise>
          </x>
          <!-- ... other axes and linear acceleration/angular velocity noise ... -->
        </orientation>
      </imu>
      <plugin name="imu_controller" filename="libgazebo_ros_imu_sensor.so">
        <ros>
          <argument>~/out:=imu</argument>
        </ros>
        <frame_name>imu_link</frame_name>
        <topic_name>imu</topic_name>
      </plugin>
    </sensor>
```

## Visualizing Sensor Data with RViz2

To visualize the data coming from these simulated sensors, we use RViz2 (ROS Visualization). A basic configuration is provided in `code/module-2/config/sensors.rviz`:

```yaml
# code/module-2/config/sensors.rviz
# ... (full content of sensors.rviz) ...
```

This configuration includes displays for:
-   **LiDAR Scan**: Shows the point cloud data from the LiDAR sensor.
-   **Depth Image**: Displays the depth information from the depth camera.
-   **IMU**: Visualizes the orientation and acceleration reported by the IMU.

By running Gazebo with your robot model and launching RViz2 with this configuration, you can observe how your digital twin perceives its environment.