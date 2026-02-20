# Quickstart: Module 3: The AI-Robot Brain (NVIDIA Isaac)

## Prerequisites

-   **OS**: Ubuntu 20.04/22.04 (recommended for Isaac Sim/ROS).
-   **NVIDIA GPU**: Required for Isaac Sim and Isaac ROS.
-   **NVIDIA Drivers**: Latest proprietary drivers.
-   **Docker & NVIDIA Container Toolkit**: Essential for running Isaac ROS.
-   **ROS 2**: Humble Hawksbill or Iron Irwini.
-   **Nav2**: Compatible with your ROS 2 distribution.

## Setup

1.  **Install NVIDIA Isaac Sim**:
    Follow the official NVIDIA Isaac Sim installation guide. This typically involves downloading Omniverse Launcher, then installing Isaac Sim through it.
    *   [Official Isaac Sim Documentation](https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/overview.html)
    *   Ensure proper setup for the Isaac Sim ROS 2 bridge.

2.  **Install NVIDIA Isaac ROS**:
    Follow the official NVIDIA Isaac ROS documentation for installation. This often involves using Docker containers.
    *   [Official Isaac ROS Documentation](https://nvidia-isaac-ros.github.io/index.html)
    *   Verify your VSLAM pipeline setup (e.g., `isaac_ros_visual_slam`).

3.  **Install Nav2**:
    Install Nav2 compatible with your ROS 2 distribution.
    ```bash
    sudo apt install ros-<ros2-distro>-navigation
    ```
    (Replace `<ros2-distro>` with `humble` or `iron`.)

4.  **Clone the repository**:
    ```bash
    git clone <repo-url>
    cd <repo-dir>
    ```

5.  **Build Isaac ROS 2 Workspace**:
    Navigate to the `isaac_ros_ws` and build your ROS 2 packages, including `my_vslam_node`.
    ```bash
    cd code/module-3/isaac_ros_ws
    colcon build --symlink-install
    source install/setup.bash
    ```
    (Ensure to source this workspace in every new terminal you use for ROS 2 commands.)

## Running Examples

### 1. Isaac Sim & Synthetic Data Generation (User Story 1)

**Launch Isaac Sim**:
-   Start NVIDIA Isaac Sim application.
-   Load your robot and environment USD files from `code/module-3/isaac_sim_assets/` (e.g., `humanoid_robot.usd`, `simple_env.usd`).

**Run Synthetic Data Generation Script**:
-   Within Isaac Sim's Script Editor or a custom extension, execute or call the `generate_synthetic_data.py` script.
    ```python
    # Example command (execute from Isaac Sim's Python environment)
    # python_path = "/path/to/your/isaac_sim_assets/generate_synthetic_data.py"
    # exec(open(python_path).read())
    ```
    (This script, when fully implemented, will generate synthetic sensor data and ground truth annotations.)

### 2. Isaac ROS VSLAM Pipeline (User Story 2)

**Launch Isaac Sim (if using simulated camera)**:
-   Start Isaac Sim and ensure your robot model is publishing camera topics (e.g., `/stereo_camera/left/image_raw`, `/stereo_camera/right/image_raw`).

**Launch Isaac ROS VSLAM node**:
-   **Open a new terminal and source your ROS 2 workspace (`code/module-3/isaac_ros_ws/install/setup.bash`)**.
    ```bash
    ros2 launch my_vslam_node vslam.launch.py
    ```
    (This will launch your placeholder VSLAM node. For actual Isaac ROS VSLAM, you would launch `isaac_ros_visual_slam`.)

### 3. Humanoid Navigation with Nav2 (User Story 3)

**Launch Isaac Sim with robot and environment**:
-   Ensure a localization source (e.g., your VSLAM pipeline) is active and publishing `odom` and `tf` data.

**Launch Nav2 stack**:
-   **Open a new terminal and source your ROS 2 workspace (`code/module-3/isaac_ros_ws/install/setup.bash`)**.
    ```bash
    # Assuming 'nav2_humanoid_config' is recognized as a ROS 2 package
    ros2 launch nav2_humanoid_config nav2_bringup.launch.py \
        params_file:=code/module-3/nav2_humanoid_config/nav2_params.yaml \
        use_sim_time:=true
    ```
    (Use RViz2 to set navigation goals and observe humanoid robot path planning and execution.)

---
*(Note: Specific commands for Isaac Sim and Isaac ROS might require additional environment setup or Docker commands not fully detailed here. Refer to official NVIDIA documentation.)*
