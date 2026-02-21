# Voice-to-Action (Whisper + ROS 2)

This chapter details the implementation of the Voice-to-Action pipeline, enabling the robot to understand and react to spoken commands. This pipeline integrates the Whisper speech-to-text model with ROS 2 for seamless communication.

## Components

The Voice-to-Action pipeline consists of three primary ROS 2 nodes:

1.  **`whisper_node.py`**: This node is responsible for capturing audio (placeholder for now), processing it through the Whisper speech-to-text model, and publishing the transcribed text as a `std_msgs/String` message on the `/transcribed_text` topic.

    -   **Location**: `code/module-4/audio_interface/src/whisper_node.py`
    -   **Functionality**:
        -   Subscribes to an audio input (future implementation).
        -   Transcribes spoken language into text using Whisper.
        -   Publishes the transcribed text.

2.  **`action_mapper_node.py`**: This node subscribes to the `/transcribed_text` topic, processes the incoming text, and maps specific keywords or phrases to corresponding robot movement commands. For demonstration, it publishes `geometry_msgs/Twist` messages to the `/cmd_vel` topic.

    -   **Location**: `code/module-4/vla_system/src/action_mapper_node.py`
    -   **Functionality**:
        -   Subscribes to `/transcribed_text`.
        -   Parses transcribed text to identify commands (e.g., "move forward", "turn left").
        -   Publishes `geometry_msgs/Twist` messages to `/cmd_vel` for robot control.

3.  **`robot_action_server.py`**: This node acts as a simple action server, subscribing to `geometry_msgs/Twist` messages on the `/cmd_vel` topic. In a real robot setup, these commands would be translated into motor controls. In this simulation, it logs the received commands and simulates basic robot movement.

    -   **Location**: `code/module-4/vla_system/src/robot_action_server.py`
    -   **Functionality**:
        -   Subscribes to `/cmd_vel`.
        -   Receives and processes robot movement commands.
        -   (Future) Interfaces with robot hardware or simulation for execution.

## Launching the Pipeline

The entire Voice-to-Action pipeline can be launched using the `voice_to_action.launch.py` file:

```bash
ros2 launch vla_system voice_to_action.launch.py
```

This launch file starts all three nodes (`whisper_node`, `action_mapper_node`, `robot_action_server`) and sets up the necessary topic connections.

## Future Enhancements

-   **Actual Audio Input**: Implement real-time audio capture and integration with the Whisper model.
-   **Advanced Action Mapping**: Develop more sophisticated natural language processing (NLP) to interpret complex commands and a broader range of actions.
-   **Integration with Robot Hardware**: Connect the `robot_action_server` to actual robot motor controllers or a more advanced simulation environment.
