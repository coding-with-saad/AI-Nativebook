# Quickstart: Module 1

## Prerequisites

- **OS**: Ubuntu 22.04 (Jammy) or 24.04 (Noble) recommended.
- **ROS 2**: Humble Hawksbill or Jazzy Jalisco installed.
  - Verify with: `printenv ROS_DISTRO`
- **Build Tools**: `colcon` installed via `sudo apt install python3-colcon-common-extensions`.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd <repo-dir>
   ```

2. **Navigate to Module 1 code**:
   ```bash
   cd code/module-1
   ```

3. **Build the package**:
   ```bash
   colcon build --symlink-install
   ```

4. **Source the workspace**:
   ```bash
   source install/setup.bash
   ```

## Running Examples

### 1. Publisher/Subscriber (User Story 1)

**Terminal 1 (Talker)**:
```bash
ros2 run ros2_basics_py simple_publisher
```

**Terminal 2 (Listener)**:
```bash
ros2 run ros2_basics_py simple_subscriber
```

### 2. Service Server/Client (User Story 1)

**Terminal 1 (Server)**:
```bash
ros2 run ros2_basics_py service_server
```

**Terminal 2 (Client)**:
```bash
ros2 run ros2_basics_py service_client
```

### 3. Smart Agent (User Story 2)

```bash
ros2 run ros2_basics_py smart_agent
```

### 4. Visualize URDF (User Story 3)

**Check validity**:
```bash
check_urdf urdf/simple_humanoid.urdf
```

**Visualize (requires GUI)**:
```bash
urdf_to_graphviz urdf/simple_humanoid.urdf
# or if rviz2 available
ros2 launch urdf_tutorial display.launch.py model:=urdf/simple_humanoid.urdf
```
