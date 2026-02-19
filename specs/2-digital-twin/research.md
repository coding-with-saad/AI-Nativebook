# Research Phase 0: Digital Twin Simulation Architecture

## Simulation Engine Selection

- **Decision**: Use **Gazebo Sim (formerly Ignition)** for physics-heavy validation and **Unity** for high-fidelity visual environments.
- **Rationale**: 
    - **Gazebo Sim** provides industry-standard physics (ODE, Bullet) and deep ROS 2 integration, essential for verifying robot dynamics (User Story 1).
    - **Unity** offers superior rendering, lighting, and a vast asset store, making it ideal for "Human-in-the-loop" or high-fidelity visual scenarios (User Story 2).
- **Alternatives considered**: 
    - *NVIDIA Isaac Sim*: High performance but requires modern NVIDIA GPUs, which might exclude some students.
    - *Webots*: Good middle ground but lacks the visual polish of Unity and the ROS 2 ubiquity of Gazebo.

## Sensor Simulation Strategy

- **Decision**: Utilize Gazebo's built-in sensor plugins (libgazebo_ros_ray_sensor, etc.) and Unity's Perception package.
- **Rationale**: These tools provide realistic noise models and standard data formats (PointClouds, Image streams) required for User Story 3.
- **Alternatives considered**: Writing custom ray-casting logic (too complex, violates "smallest viable change").

## Integration Workflow (Sim-to-Real)

- **Decision**: Use the **ROS 2 Gazebo Bridge** and the **Unity-Robotics-Hub** for communication.
- **Rationale**: These bridges allow the same control logic (from Module 1) to drive robots in different simulation environments, facilitating the "Validation" goals of User Story 4 and 5.
- **Alternatives considered**: Direct socket communication (rejected as it doesn't scale to complex sensor data).
