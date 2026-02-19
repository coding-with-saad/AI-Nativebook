# Data Model: Module 1

## Entities

### User Profile (Docusaurus)
*Not applicable - Docusaurus is static.*

### ROS 2 Message (Example)
**Name**: `String` (std_msgs/msg/String)
- **Field**: `data` (string)
- **Usage**: Used in "Hello World" publisher/subscriber example.

### ROS 2 Service (Example)
**Name**: `AddTwoInts` (example_interfaces/srv/AddTwoInts)
- **Request**:
  - `a` (int64)
  - `b` (int64)
- **Response**:
  - `sum` (int64)
- **Usage**: Used in Service Client/Server example.

### Robot Model (URDF)
**Name**: `SimpleHumanoid`
- **Link**: `torso` (Box)
- **Link**: `head` (Sphere)
- **Link**: `left_arm`, `right_arm` (Cylinders)
- **Joint**: `neck` (fixed/continuous)
- **Joint**: `left_shoulder`, `right_shoulder` (revolute)
- **Validation**: Must pass `check_urdf` schema validation.
