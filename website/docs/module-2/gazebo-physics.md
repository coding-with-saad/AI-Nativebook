---
sidebar_position: 1
---

# Gazebo Physics: Setting up your Digital Twin

This chapter covers the basics of Gazebo Physics for Digital Twin environments. We'll explore how to configure physics properties and integrate robot models to create a realistic simulation.

## Physics Configuration

Gazebo allows for detailed configuration of physics parameters. We've defined some basic parameters in `code/module-2/gazebo/config/physics.yaml`:

```yaml
# code/module-2/gazebo/config/physics.yaml
gravity: [0.0, 0.0, -9.81]
max_step_size: 0.001
real_time_factor: 1.0
real_time_update_rate: 1000
```

These parameters control aspects like gravity, the simulation timestep, and the real-time factor, which determines how fast the simulation runs relative to real-world time.

## Creating a Physics World

The `humanoid_physics.sdf` file defines a basic Gazebo world with a ground plane and integrates our `DigitalRobot` model.

```xml
<!-- code/module-2/gazebo/worlds/humanoid_physics.sdf -->
<sdf version="1.6">
  <world name="humanoid_physics_world">
    <gravity>0 0 -9.81</gravity>
    <physics type="ode">
      <ode>
        <solver>
          <type>quick</type>
          <iters>50</iters>
          <min_step_size>0.0001</min_step_size>
        </solver>
        <constraints>
          <contact_max_correcting_vel>100</contact_max_correcting_vel>
          <contact_surface_layer>0.001</contact_surface_layer>
        </constraints>
      </ode>
    </physics>

    <include>
      <uri>model://sun</uri>
    </include>
    <model name="ground_plane_friction">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>0.8</mu> <!-- Coefficient of friction -->
                <mu2>0.8</mu2>
              </ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <script>
              <uri>file://media/materials/scripts/gazebo.material</uri>
              <name>Gazebo/Grey</name>
            </script>
          </material>
        </visual>
      </link>
    </model>

    <!-- Include the DigitalRobot URDF -->
    <include>
      <uri>model://robot.urdf</uri>
      <name>digital_robot_instance</name>
      <pose>0 0 1.0 0 0 0</pose> <!-- Initial pose of the robot -->
    </include>
  </world>
</sdf>
```

This SDF file sets up a world with a sun, a ground plane with friction, and includes our simple `robot.urdf` for simulation.

## Your Digital Robot Model

The `robot.urdf` file in `code/module-2/gazebo/models/` defines a basic robot structure:

```xml
<!-- code/module-2/gazebo/models/robot.urdf -->
<?xml version="1.0"?>
<robot name="digital_robot">
  <link name="base_link">
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 0.5"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0"/>
      <geometry>
        <box size="0.2 0.2 1.0"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.5"/>
      <geometry>
        <box size="0.2 0.2 1.0"/>
      </geometry>
    </collision>
  </link>
</robot>
```

This simple robot model demonstrates how to define links, inertias, visuals, and collisions. You can expand on this to create more complex robot designs.