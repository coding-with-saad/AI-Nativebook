# Unity Project for Module 2: Digital Twin Environments

This directory contains the Unity project for "Module 2: Digital Twin Environments".

## Setup Instructions:

1.  **Open in Unity Hub**: Add this `unity_project` folder as a new project in your Unity Hub.
2.  **Unity Version**: Ensure you are using Unity 2022.3 LTS or newer.
3.  **Install Packages**:
    *   Go to `Window > Package Manager`.
    *   Install the "HDRP" (High Definition RP) package for high-fidelity rendering.
    *   Install "Unity Robotics Hub" packages for integration with Gazebo/ROS.
4.  **Import Humanoid Model**: Import your humanoid robot model (e.g., `robot.fbx`, `robot.gltf`) into the `Assets/Models` folder.
5.  **Configure PBR Materials**: Create and assign Physically Based Rendering (PBR) materials to your robot model for realistic visuals.
6.  **Create SimWorld Scene**: Create a new scene (e.g., `Assets/Scenes/SimWorld.unity`) and configure it as your kitchen/workspace environment. Ensure it uses HDRP settings for lighting.
7.  **Configure Cameras & Scale**: Set up various camera viewpoints in your `SimWorld` scene. Validate the scale of your environment and robot to ensure it matches real-world dimensions.


