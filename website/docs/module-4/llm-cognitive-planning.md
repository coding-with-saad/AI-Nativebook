# LLM-Based Cognitive Planning

This chapter delves into the implementation of LLM-based cognitive planning, enabling the robot to perform higher-level reasoning and task decomposition. This system leverages Large Language Models (LLMs) to break down complex commands into executable sub-tasks and generate appropriate function calls.

## Components

The LLM-based cognitive planning pipeline primarily involves:

1.  **`llm_interface.py`**: This Python module provides a simulated interface for interacting with an LLM. In a real-world scenario, this would connect to an LLM API (e.g., OpenAI, Hugging Face) or a locally deployed model.

    -   **Location**: `code/module-4/vla_system/vla_system/llm_interface.py`
    -   **Functionality**:
        -   Sends prompts to the LLM.
        -   Receives and processes LLM responses.
        -   Simulates LLM behavior for task decomposition and function call generation.

2.  **`llm_prompts.py`**: This module stores various prompt templates used for guiding the LLM's behavior, particularly for task decomposition and function call generation.

    -   **Location**: `code/module-4/vla_system/vla_system/llm_prompts.py`
    -   **Functionality**:
        -   Defines `TASK_DECOMPOSITION_PROMPT` for breaking down high-level commands.
        -   Defines `FUNCTION_CALL_PROMPT` for converting sub-tasks into robot-executable function calls.

3.  **`llm_planner_node.py`**: This ROS 2 node orchestrates the interaction between high-level commands and the LLM. It subscribes to high-level commands, uses the LLM to decompose them, generates function calls, and publishes these as robot actions.

    -   **Location**: `code/module-4/vla_system/src/llm_planner_node.py`
    -   **Functionality**:
        -   Subscribes to `/high_level_command` (a `std_msgs/String` topic).
        -   Calls `llm_interface.py` for task decomposition and function call generation.
        -   Publishes generated robot actions (e.g., `move_to("table")`, `grasp_object("ball")`) to the `/robot_actions` topic (a `std_msgs/String` topic).
        -   (Future) Will integrate with a ROS 2 Action Client to send goals to an Action Server for execution.

## Launching the Planning Pipeline

The LLM-Based Cognitive Planning pipeline can be launched using the `llm_planning.launch.py` file:

```bash
ros2 launch vla_system llm_planning.launch.py
```

This launch file starts the `llm_planner_node` and can be configured with parameters, such as the LLM model to use.

## Example Workflow

1.  A high-level command (e.g., "Go to the kitchen and get me a cup") is published to `/high_level_command`.
2.  `llm_planner_node` receives the command.
3.  `llm_planner_node` uses `llm_interface.py` with `TASK_DECOMPOSITION_PROMPT` to break down the command into sub-tasks (e.g., "Navigate to kitchen", "Find a cup", "Grasp the cup", "Bring the cup").
4.  For each sub-task, `llm_planner_node` uses `llm_interface.py` with `FUNCTION_CALL_PROMPT` to generate a robot function call (e.g., `move_to("kitchen")`, `identify_object("cup")`, `grasp_object("cup")`).
5.  These function calls are published on `/robot_actions` for an executor to process.

## Future Enhancements

-   **Robust LLM Integration**: Replace the simulated LLM with a live connection to a powerful LLM.
-   **Error Handling and Re-planning**: Implement mechanisms for the LLM to handle execution failures and re-plan tasks.
-   **Dynamic Function Calling**: Allow the LLM to dynamically select and call available robot capabilities based on context.
-   **ROS 2 Action Client/Server**: Full integration with ROS 2 Actions for more robust and feedback-driven task execution.
