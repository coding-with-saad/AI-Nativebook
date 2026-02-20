# Data Model: Module 3: The AI-Robot Brain (NVIDIA Isaac)

## Entities

### Humanoid Robot Model
-   **Description**: Represents the robot's kinematic, dynamic, and visual properties within Isaac Sim.
-   **Attributes**:
    -   `kinematics` (joint limits, hierarchy)
    -   `dynamics` (mass, inertia tensors, friction coefficients)
    -   `visuals` (3D meshes, textures, materials)
    -   `sensors` (virtual sensors like cameras, IMUs, LiDAR)
    -   `actuators` (joints, motors)

### Isaac Sim Environment
-   **Description**: 3D simulation world with configurable physics, lighting, and assets for synthetic data generation.
-   **Attributes**:
    -   `assets` (static objects, dynamic objects, props)
    -   `lighting` (HDRI maps, light sources, exposure)
    -   `physics_properties` (gravity, collision settings)
    -   `render_settings` (resolution, anti-aliasing, post-processing effects)

### Synthetic Data
-   **Description**: Generated sensor readings with corresponding ground truth labels from Isaac Sim.
-   **Attributes**:
    -   `modality` (RGB, Depth, Semantic Segmentation, Instance Segmentation, Bounding Boxes 2D/3D)
    -   `annotations` (labels, instance IDs, class IDs)
    -   `metadata` (camera intrinsics/extrinsics, timestamp, simulation parameters)
    -   `format` (e.g., image files, JSON, CSV)

### VSLAM System
-   **Description**: Software module within Isaac ROS that processes visual input to estimate robot pose and build a map.
-   **Attributes**:
    -   `input_sensors` (stereo cameras, IMU)
    -   `output_data` (6-DOF pose, odometry, sparse/dense map)
    -   `performance_metrics` (update rate, localization accuracy, map consistency)

### Nav2 Stack
-   **Description**: ROS 2 navigation framework responsible for path planning, control, and obstacle avoidance.
-   **Attributes**:
    -   `map` (occupancy grid for navigation)
    -   `global_planner` (algorithm for long-range path planning, e.g., A\*)
    -   `local_planner` (algorithm for short-range obstacle avoidance, e.g., TEB, DWB)
    -   `controller` (interface to robot actuators)
    -   `costmaps` (layers for static obstacles, dynamic obstacles, inflation)
    -   `robot_footprint` (geometric definition of robot base for collision)

### AI Perception Model (Conceptual)
-   **Description**: An AI model trained using synthetic data for tasks like object detection or pose estimation, integrated into the robot's perception pipeline.
-   **Attributes**:
    -   `input_data` (sensor data, e.g., RGB images)
    -   `output_data` (detection bounding boxes, object classes, pose estimates)
    -   `inference_engine` (e.g., TensorRT for acceleration)
    -   `performance` (inference time, accuracy)
