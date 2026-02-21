# Quickstart: Module 4: Vision-Language-Action (VLA)

## Prerequisites

-   **OS**: Ubuntu 20.04/22.04 (recommended for ROS 2).
-   **ROS 2**: Humble Hawksbill or Iron Irwini.
-   **Python**: 3.8+
-   **Voice Recognition Model**: (e.g., Whisper, installed via `ros-ai/ros2_whisper` or standalone).
-   **Large Language Model (LLM)**: Access to a suitable LLM (local model or API key for cloud service).
-   **Perception/Navigation Stack**: Operational setup from Module 3 (Isaac Sim, Isaac ROS, Nav2).

## Setup

1.  **Install ROS 2**:
    Follow the official ROS 2 installation guide for your distribution (Humble or Iron).
    *   [ROS 2 Documentation](https://docs.ros.org/en/humble/Installation.html)

2.  **Install Voice Recognition (Whisper) ROS 2 Package**:
    Clone and build `ros-ai/ros2_whisper` in your ROS 2 workspace.
    ```bash
    mkdir -p ~/ros2_vla_ws/src
    cd ~/ros2_vla_ws/src
    git clone https://github.com/ros-ai/ros2_whisper.git
    cd ~/ros2_vla_ws
    rosdep install --from-paths src --ignore-src -r -y
    colcon build --packages-up-to ros2_whisper
    source install/setup.bash
    ```

3.  **Setup LLM Access**:
    -   **Local LLM**: Download and configure an open-source LLM (e.g., Llama.cpp or via Hugging Face Transformers) to run locally.
    -   **Cloud LLM**: Obtain an API key for a cloud-based LLM service (e.g., OpenAI, Google Gemini).
    (Specific instructions will depend on the chosen LLM.)

4.  **Clone the repository**:
    ```bash
    git clone <repo-url>
    cd <repo-dir>
    ```

5.  **Build VLA ROS 2 Workspace**:
    ```bash
    cd code/module-4/vla_system
    colcon build --symlink-install
    source install/setup.bash
    ```
    (Ensure this workspace is sourced in every new terminal you use for ROS 2 commands related to VLA.)

## Running Examples

### 1. Voice-to-Action (Whisper + ROS 2) (User Story 1)

**Launch Whisper ROS 2 Node**:
-   Ensure your microphone is configured for audio input.
    ```bash
    ros2 launch whisper_bringup bringup.launch.py
    ```

**Launch Action Mapping Node**:
-   In a separate terminal, launch your custom ROS 2 node that subscribes to Whisper's output and publishes robot commands.
    ```bash
    ros2 run vla_system voice_action_mapper
    ```
    (Speak commands into your microphone and observe the robot's reactions.)

### 2. LLM-Based Cognitive Planning (User Story 2)

**Launch LLM Interface Node**:
-   Start the ROS 2 node that interfaces with your chosen LLM.
    ```bash
    ros2 launch vla_system llm_planner.launch.py
    ```

**Send High-Level Task**:
-   Publish a high-level natural language task to the LLM planner node's input topic.
    ```bash
    ros2 topic pub /vla/command std_msgs/String "data: 'robot, go to the kitchen and get a cup'" --once
    ```
    (Observe the LLM planner breaking down the task into a sequence of ROS 2 actions.)

### 3. Capstone: Autonomous Humanoid Pipeline (User Story 3)

**Ensure Module 3 Components are Running**:
-   Isaac Sim with humanoid robot (simulated or real).
-   Isaac ROS VSLAM for localization (publishing to relevant topics).
-   Nav2 for path planning and navigation.

**Launch Integrated VLA Pipeline**:
-   This launch file integrates all VLA components for the full autonomous pipeline.
    ```bash
    ros2 launch vla_system capstone_vla_pipeline.launch.py
    ```
    Once launched, the system will be ready to receive voice commands. The `capstone_pipeline_node` will orchestrate the LLM planning based on these commands and react to perception inputs.

**Testing Reactive Planning and Error Recovery**:
To test the reactive planning and error recovery mechanisms, you can simulate perception inputs by publishing to the `perception_output` topic.

-   **Simulate Obstacle Detection**:
    ```bash
    ros2 topic pub /perception_output std_msgs/String "data: 'obstacle detected at [X, Y, Z]'" --once
    ```
    Observe the `capstone_pipeline_node` logging a warning and publishing a re-plan command to the `high_level_command` topic.

-   **Simulate Task Failure**:
    ```bash
    ros2 topic pub /perception_output std_msgs/String "data: 'task failed: failed to reach target'" --once
    ```
    Observe the `capstone_pipeline_node` logging an error and publishing a recovery command to the `high_level_command` topic.

(Give a complex voice command and observe the robot autonomously performing the task, utilizing perception, planning, and action, with reactive adjustments as simulated.)

---
*(Note: Specific commands and file paths are placeholders and will be refined during the implementation phase.)*
