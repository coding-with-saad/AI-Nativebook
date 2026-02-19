# Feature Specification: Module 1: The Robotic Nervous System (ROS 2)

**Feature Branch**: `001-ros2-basics`
**Created**: 2026-01-31
**Status**: Draft
**Input**: Module 1: The Robotic Nervous System (ROS 2). Target audience: CS students with Python and basic AI knowledge. Focus: Using ROS 2 as the communication layer between AI agents and humanoid robots. Chapters: 1. ROS 2 Basics (nodes, topics, services), 2. Python Agents with rclpy, 3. Humanoid Structure with URDF.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - ROS 2 Communication Fundamentals (Priority: P1)

A CS student learns to set up a basic ROS 2 environment where Python scripts can communicate via topics and services, establishing the "nervous system" for future AI agents.

**Why this priority**: Core competency required for all subsequent AI-robot interaction. Without mastering nodes and topics, no agent can control a robot.

**Independent Test**: Can be fully tested by running a publisher node and a subscriber node that successfully exchange messages, and a service client/server pair that executes a request.

**Acceptance Scenarios**:

1. **Given** a configured ROS 2 environment, **When** the user runs a publisher node sending "Hello World", **Then** the subscriber node receives and logs the message.
2. **Given** a running service server (e.g., `AddTwoInts`), **When** the user sends a request from a client node, **Then** the server computes the correct result and returns it to the client.

---

### User Story 2 - Python Agent Integration with rclpy (Priority: P2)

The student creates a Python-based "agent" using `rclpy` that can make decisions (simple logic) and act on the ROS 2 network.

**Why this priority**: Bridges the gap between standard Python AI code and the robotics middleware. This is the "AI Native" part of the workflow.

**Independent Test**: Can be tested by a script where an "agent" receives sensor-like data (mocked) and publishes a command based on simple logic.

**Acceptance Scenarios**:

1. **Given** a topic publishing mock sensor data (e.g., `temperature`), **When** the agent node receives a value above a threshold, **Then** it publishes a "Warning" alert to a `status` topic.
2. **Given** a Python script using `rclpy`, **When** the script is executed, **Then** it registers as a node on the ROS graph without errors.

---

### User Story 3 - Visualizing Humanoid Structure (Priority: P3)

The student defines a basic humanoid robot structure using URDF and visualizes it to understand how software maps to physical form.

**Why this priority**: Essential for understanding robot embodiedness. AI agents need to know the physical constraints (links/joints) of the body they control.

**Independent Test**: Can be tested by loading the generated URDF file into a visualization tool (like Rviz or a simple URDF parser) and verifying links/joints exist.

**Acceptance Scenarios**:

1. **Given** a valid URDF file describing a simple robot arm, **When** loaded into a visualization tool (e.g., Rviz2 check), **Then** all defined links and joints are rendered correctly.
2. **Given** two links connected by a joint, **When** the joint state is published, **Then** the visualization updates the relative position of the links.

### Edge Cases

- **Environment Failure**: If ROS 2 is not sourced or available, scripts MUST fail with a clear "ROS 2 not found" style error message rather than a cryptic Python traceback.
- **Network Isolation**: If nodes are run with `ROS_LOCALHOST_ONLY=1`, they MUST still communicate if on the same machine.
- **Invalid URDF**: If the URDF XML is malformed, the validation tool MUST report the specific line number and error.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system (book module code) MUST provide working Python examples of a ROS 2 Publisher and Subscriber using `rclpy`.
- **FR-002**: The system MUST provide working Python examples of a ROS 2 Service Server and Client.
- **FR-003**: The examples MUST be compatible with standard ROS 2 (Humble or Jazzy) distributions.
- **FR-004**: The system MUST provide a comprehensive URDF XML example representing a simplified humanoid structure (e.g., Torso, Head, Arms).
- **FR-005**: The examples MUST run in a headless environment (for CI/validation) but produce textual verification of success.
- **FR-006**: The content MUST explain the mapping between Python classes and ROS 2 Nodes.

### Key Entities *(include if feature involves data)*

- **Node**: A process that performs computation (e.g., a sensor driver, an AI agent).
- **Topic**: A named channel over which nodes exchange messages (Pub/Sub).
- **Service**: A synchronous request/reply interaction between nodes.
- **URDF**: Unified Robot Description Format file representing the physical robot.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A student can run the "Hello World" Pub/Sub example in under 1 minute after environment setup.
- **SC-002**: All provided code examples pass automated linting (flake8/black) and execution tests in the CI pipeline.
- **SC-003**: The URDF model successfully validates against the `check_urdf` tool with 0 errors.
- **SC-004**: The module content enables a user to answer "How do I create a Node in Python?" with a specific code pattern citation.

### Assumptions

- Users have a working ROS 2 installation or ready-to-use Docker container.
- Python 3.10+ is available.
- "CS students" implies familiarity with classes, inheritance, and command line.
