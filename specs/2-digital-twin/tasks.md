# Tasks: Module 2: Digital Twin Environments

**Branch**: `2-digital-twin` | **Spec**: [specs/2-digital-twin/spec.md](./spec.md)
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md

**Organization**: Tasks are grouped by user story (P1, P2) to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize simulation project structures and Docusaurus placeholders.

- [X] T001 Initialize Unity project with HDRP and Robotics Hub in `code/module-2/unity_project`
- [X] T002 Create Gazebo resource structure in `code/module-2/gazebo/{worlds,models,plugins}`
- [X] T003 [P] Configure Docusaurus category definition in `website/docs/module-2/_category_.json`
- [X] T004 Create placeholder content pages in `website/docs/module-2/{gazebo-physics.md,unity-environments.md,sensor-simulation.md}`

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ensure baseline simulation tools and robot models are available.

- [X] T005 [P] Export Humanoid robot meshes for Unity and Gazebo in `code/module-2/assets/`
- [X] T006 Configure initial Gazebo environment `code/module-2/gazebo/worlds/base_world.sdf`
- [X] T007 Verify Gazebo installation and GUI rendering with the base world

**Checkpoint**: Infrastructure ready. User stories can proceed.

---

## Phase 3: User Story 1 - Gazebo Physics Simulation (Priority: P1)

**Goal**: Establish realistic physics for robot validation.
**Independent Test**: Robot model demonstrates gravity and friction response in Gazebo.

### Implementation for User Story 1

- [X] T008 [US1] Create `PhysicsConfig` parameters in `code/module-2/gazebo/config/physics.yaml`
- [X] T009 [US1] Implement `humanoid_physics.sdf` world with ground plane and friction properties
- [X] T010 [US1] Integrate `DigitalRobot` (URDF) into the Gazebo physics world
- [ ] T011 [US1] Write Chapter: "Gazebo Physics" in `website/docs/module-2/gazebo-physics.md` referencing code/configs

**Checkpoint**: US1 verification (FR-001, FR-002, SC-001).

---

## Phase 4: User Story 2 - Unity Visual Environments (Priority: P1)

**Goal**: High-fidelity 3D visualization.
**Independent Test**: Robot renders with realistic lighting and materials in a Unity scene.

### Implementation for User Story 2

- [X] T012 [P] [US2] Import humanoid model and configure PBR materials in Unity project
- [X] T013 [US2] Create `SimWorld` kitchen/workspace scene in Unity with HDRP lighting
- [X] T014 [US2] Configure camera viewpoints and workspace scale validation
- [ ] T015 [US2] Write Chapter: "Unity Environments" in `website/docs/module-2/unity-environments.md`

**Checkpoint**: US2 verification (FR-003, FR-004, SC-006).

---

## Phase 5: User Story 3 - Sensor Simulation & Data Visualization (Priority: P1)

**Goal**: Generate and visualize LiDAR, Depth, and IMU data.
**Independent Test**: Point cloud data accurately represents environment geometry in RViz2.

### Implementation for User Story 3

- [X] T016 [US3] Add `VirtualSensor` (LiDAR/Depth) plugins to robot in `code/module-2/gazebo/models/robot.sdf`
- [X] T017 [US3] Implement IMU Gaussian noise model in simulation config
- [X] T018 [P] [US3] Create RViz2 display configuration `code/module-2/config/sensors.rviz`
- [ ] T019 [US3] Write Chapter: "Sensor Simulation" in `website/docs/module-2/sensor-simulation.md`

**Checkpoint**: US3 verification (FR-005, FR-006, SC-002).

---

## Phase 6: User Story 4 & 5 - Validation and ROS Integration (Priority: P2)

**Goal**: Sim-to-real gap analysis and control integration.
**Independent Test**: Compare simulated data against real-world logs; command robot via ROS.

### Implementation for User Stories 4 & 5

- [X] T020 [US4] Develop `compare_sensors.py` analysis script in `code/module-2/scripts/`
- [X] T021 [US5] Configure `ros_gz_bridge` for motor and sensor topics
- [X] T022 [US5] Implement a simple move-to-goal test node in Python
- [X] T023 [US4] [US5] Update Docusaurus with "Sim-to-Real Validation" sections

**Checkpoint**: US4/5 verification (SC-003, FR-007).

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation cleanup.

- [X] T024 Verify all internal links and code imports in Docusaurus site
- [X] T025 Run `npm run build` in `website/` to ensure production readiness
- [X] T026 Update `quickstart.md` with final installation commands for Unity/Gazebo

## Dependencies & Execution Order

1. **Setup (Phase 1)**: T001 and T002 are prerequisites for all story phases.
2. **Foundational (Phase 2)**: T005 and T006 must complete before US1.
3. **User Stories (Phase 3-5)**: 
   - US1, US2, and US3 are high priority and can run largely in parallel once Phase 2 is done.
4. **Validation (Phase 6)**: Depends on completion of US1 and US3.

## Parallel Execution Example

```bash
# Parallel Phase: Unity visuals and Gazebo physics
Task: T012 Import humanoid model to Unity
Task: T008 Create PhysicsConfig for Gazebo
Task: T003 Configure Docusaurus category
```

## Implementation Strategy
- **MVP**: Complete US1 (Gazebo Physics) first to enable the "Robotic Nervous System" validation.
- **Incremental**: Add Unity visuals (US2) and Sensors (US3) in parallel to enhance the "Digital Twin" fidelity.
