# Chapter 3: Humanoid Structure

A robot needs a body. In ROS 2, we define this body using the **Unified Robot Description Format (URDF)**.

## The URDF Model

Our simple humanoid has a boxy torso, a spherical head, and two cylindrical arms.

```xml title="simple_humanoid.urdf"
<robot name="simple_humanoid">
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.2 0.4 0.6"/>
      </geometry>
      <!-- ... -->
    </visual>
  </link>
  <!-- ... full XML structure ... -->
</robot>
```

## Setup and Validation

1. Install the URDF check tool (standard in desktop install, or via `liburdfdom-tools`):
   ```bash
   sudo apt install liburdfdom-tools
   ```

2. Validate the model:
   ```bash
   check_urdf code/module-1/urdf/simple_humanoid.urdf
   ```
   **Expected Output**:
   ```text
   robot name is: simple_humanoid
   ---------- Successfully Parsed XML ---------------
   root Link: base_link has 1 child(ren)
       child(1):  torso
           child(1):  head
           child(2):  left_arm
           child(3):  right_arm
   ```

3. Visualize (Requires GUI):
   ```bash
   urdf_to_graphviz code/module-1/urdf/simple_humanoid.urdf
   # Opens a PDF showing the link tree
   ```
