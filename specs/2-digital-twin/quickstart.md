# Quickstart: Module 2

## Prerequisites

- **OS**: Ubuntu 22.04+ (for Gazebo and ROS 2) or Windows 10+ (for Unity).
- **Gazebo Sim**: Garden or Harmonic version.
- **Unity**: 2022.3 LTS or newer with "Unity Robotics Hub" packages.
- **ROS 2**: Humble/Jazzy (for integration and sensor visualization).

## Setup

1. **Install Gazebo Sim**:
   Follow the official installation guide for Gazebo Garden/Harmonic:
   [https://gazebosim.org/docs/latest/install](https://gazebosim.org/docs/latest/install)
   For ROS 2 integration, install `ros-humble-ros-gz` (for Humble) or `ros-jazzy-ros-gz` (for Jazzy):
   ```bash
   sudo apt-get update
   sudo apt-get install ros-humble-ros-gz # or ros-jazzy-ros-gz
   ```

2. **Unity Setup**:
   - Download and install Unity Hub and Unity Editor (2022.3 LTS or newer):
     [https://unity3d.com/get-unity/download](https://unity3d.com/get-unity/download)
   - Open Unity Hub and add the project located at `code/module-2/unity_project`.
   - Inside Unity Editor, go to `Window > Package Manager` and install "HDRP" (High Definition RP) and "Unity Robotics Hub" packages.
   - Refer to `code/module-2/unity_project/README.md` for detailed Unity project setup instructions.

3. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd <repo-dir>
   ```

4. **Source ROS 2 workspace (if using ROS 2)**:
   ```bash
   source /opt/ros/humble/setup.bash # or jazzy
   ```

## Running Examples

### 1. Gazebo Physics (User Story 1)

Launch the Gazebo physics world with the humanoid robot:
```bash
# Ensure your ROS 2 environment is sourced if using ROS GZ bridge
# From the root of this project:
gz sim -r code/module-2/gazebo/worlds/humanoid_physics.sdf
```
You should see a simple robot fall onto a ground plane.

### 2. Unity Environment (User Story 2)

- Open the Unity project `code/module-2/unity_project` in Unity Editor.
- Navigate to your created `SimWorld` scene (e.g., `Assets/Scenes/SimWorld.unity`).
- Press the **Play** button in the Unity Editor to visualize lighting and high-fidelity rendering of your environment.

### 3. Sensor Visualization (User Story 3)

To visualize LiDAR, Depth Camera, and IMU data in RViz2:

**Terminal 1 (Launch Gazebo Simulation)**:
```bash
# Ensure your ROS 2 environment is sourced
gz sim -r code/module-2/gazebo/worlds/humanoid_physics.sdf
```

**Terminal 2 (Launch ROS-Gazebo Bridge)**:
```bash
# Ensure your ROS 2 environment is sourced
ros2 launch ros_gz_bridge bridge_nodes.launch.py ros_config:=code/module-2/config/ros_gz_bridge.yaml
```

**Terminal 3 (Visualize in RViz2)**:
```bash
# Ensure your ROS 2 environment is sourced
ros2 run rviz2 rviz2 -d code/module-2/config/sensors.rviz
```

You should see the sensor data streams (LiDAR point cloud, depth image, IMU readings) in RViz2.

### 4. Sim-to-Real Validation (User Story 4)

Compare simulation logs with provided dataset (after recording data from simulation and real robot):
```bash
python3 code/module-2/scripts/compare_sensors.py --sim /path/to/sim_log.csv --real /path/to/real_log.csv
```
Replace `/path/to/sim_log.csv` and `/path/to/real_log.csv` with your actual log files.

### 5. ROS 2 Control (User Story 5)

To control the simulated robot via a simple ROS 2 node:

**Terminal 1 (Launch Gazebo Simulation)**:
```bash
# Ensure your ROS 2 environment is sourced
gz sim -r code/module-2/gazebo/worlds/humanoid_physics.sdf
```

**Terminal 2 (Launch ROS-Gazebo Bridge)**:
```bash
# Ensure your ROS 2 environment is sourced
ros2 launch ros_gz_bridge bridge_nodes.launch.py ros_config:=code/module-2/config/ros_gz_bridge.yaml
```

**Terminal 3 (Run Simple Mover Node)**:
```bash
# Ensure your ROS 2 environment is sourced
# You might need to make the script executable: chmod +x code/module-2/ros2_nodes/simple_mover.py
python3 code/module-2/ros2_nodes/simple_mover.py
```
Your simulated robot should start moving according to the commands from `simple_mover.py`.
