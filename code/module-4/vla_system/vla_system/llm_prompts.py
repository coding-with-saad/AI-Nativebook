# llm_prompts.py

# Prompt for task decomposition
TASK_DECOMPOSITION_PROMPT = """
You are a robotic task planner. Decompose the following high-level command into a sequence of simple, executable sub-tasks for a robot.
Each sub-task should be a single, distinct action.
Example:
High-level command: "Fetch the red ball from the table."
Sub-tasks:
- Navigate to the table.
- Identify the red ball.
- Grasp the red ball.
- Navigate to the drop-off zone.
- Release the red ball.

High-level command: "{command}"
Sub-tasks:
"""

# Prompt for generating function calls based on decomposed tasks
FUNCTION_CALL_PROMPT = """
Given the following sub-task, generate the appropriate robot function call.
Available functions:
- `move_to(location: str)`: Navigates the robot to a specified location.
- `grasp_object(object_name: str)`: Instructs the robot to grasp a named object.
- `release_object()`: Instructs the robot to release the currently held object.
- `identify_object(object_name: str)`: Identifies a specific object in the robot's perception.

Example:
Sub-task: "Navigate to the table."
Function call: `move_to("table")`

Sub-task: "Grasp the red ball."
Function call: `grasp_object("red ball")`

Sub-task: "{sub_task}"
Function call:
"""

# You can add more prompts here as needed for different LLM functionalities
# For example, prompts for error handling, confirmation, etc.
