# Data Model: Module 2

## Entities

### Robot Model (Digital Twin)
**Name**: `DigitalRobot` (URDF/SDF/Prefab)
- **Kinematics**: Joint limits, hierarchy.
- **Dynamics**: Mass, Inertia tensors, Friction coefficients.
- **Visuals**: 3D meshes (.obj, .dae, .fbx).
- **Collision**: Simplified primitive shapes (Box, Cylinder, Sphere).

### Physics Engine Config
**Name**: `PhysicsConfig`
- **Gravity**: `Vector3` (Default: 0, 0, -9.81).
- **Solver**: `String` (e.g., "quick", "world").
- **Timestep**: `Float` (e.g., 0.001s).
- **Friction**: `Map<Material, Coefficient>`.

### Environment Scene
**Name**: `SimWorld`
- **Static Assets**: Buildings, Terrain, Furniture.
- **Lighting**: Global illumination, Point lights, Shadows.
- **Skybox**: HDR environmental map.

### Virtual Sensor
**Name**: `VirtualSensor`
- **Type**: `Enum` (LIDAR, DEPTH_CAMERA, IMU).
- **Frame ID**: `String` (Link to robot transform).
- **Update Rate**: `Int` (Hz).
- **Noise Model**: `GaussianNoise(mean, stddev)`.

### Simulation Run
**Name**: `SimSession`
- **Real Time Factor (RTF)**: `Float` (Target: 1.0).
- **Log Path**: `String` (Output for sensor/pose data).
- **State**: `Enum` (PAUSED, RUNNING, STEPPING).
