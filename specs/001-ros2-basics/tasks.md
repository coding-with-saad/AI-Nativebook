# Tasks: Module 1: The Robotic Nervous System (ROS 2)

**Branch**: `001-ros2-basics` | **Spec**: [specs/001-ros2-basics/spec.md](./spec.md)
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md

**Organization**: Tasks are grouped by user story (P1, P2, P3) to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize Docusaurus site and ROS 2 package structure.

- [ ] T001 Initialize Docusaurus site in `website/` using `classic` template
- [ ] T002 [P] Configure Docusaurus sidebars and navigation in `website/docusaurus.config.js` and `website/sidebars.js`
- [ ] T003 Create ROS 2 package structure `code/module-1/ros2_basics_py` with `setup.py` and `package.xml`
- [ ] T004 [P] Create `code/module-1/urdf` directory structure for URDF files
- [ ] T005 Update `code/module-1/ros2_basics_py/setup.py` to support entry points for future nodes

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ensure build and test infrastructure works before adding logic.

- [ ] T006 Configure `ament_python` build in `code/module-1/ros2_basics_py/setup.py`
- [ ] T007 Add standard linting tests (flake8, pep257) in `code/module-1/ros2_basics_py/test/`
- [ ] T008 [P] Create placeholder content pages `website/docs/module-1/{chapter-1-basics.md,chapter-2-agents.md,chapter-3-urdf.md}`
- [ ] T009 Verify `colcon build` and `colcon test` pass on the empty package

**Checkpoint**: Infrastructure ready. User stories can proceed.

---

## Phase 3: User Story 1 - ROS 2 Communication Fundamentals (Priority: P1)

**Goal**: Enable Pub/Sub and Service communication.
**Independent Test**: Run publisher/subscriber and client/server pairs successfully.

### Implementation for User Story 1

- [ ] T010 [US1] Implement `SimplePublisher` node in `code/module-1/ros2_basics_py/ros2_basics_py/simple_publisher.py`
- [ ] T011 [US1] Implement `SimpleSubscriber` node in `code/module-1/ros2_basics_py/ros2_basics_py/simple_subscriber.py`
- [ ] T012 [P] [US1] Create `ServiceServer` node in `code/module-1/ros2_basics_py/ros2_basics_py/service_server.py`
- [ ] T013 [P] [US1] Create `ServiceClient` node in `code/module-1/ros2_basics_py/ros2_basics_py/service_client.py`
- [ ] T014 [US1] Register utility entry points in `setup.py` for all 4 nodes
- [ ] T015 [US1] Write Chapter 1 content "ROS 2 Basics" in `website/docs/module-1/chapter-1-basics.md` referencing code

**Checkpoint**: US1 verification (FR-001, FR-002, SC-001).

---

## Phase 4: User Story 2 - Python Agent Integration (Priority: P2)

**Goal**: Logic-based agents using `rclpy`.
**Independent Test**: Agent node reacts to mock sensor data.

### Implementation for User Story 2

- [ ] T016 [US2] Implement `SmartAgent` class in `code/module-1/ros2_basics_py/ros2_basics_py/smart_agent.py` logic
- [ ] T017 [US2] Register `smart_agent` entry point in `setup.py`
- [ ] T018 [US2] Write Chapter 2 content "Python Agents" in `website/docs/module-1/chapter-2-agents.md` referencing code

**Checkpoint**: US2 verification (FR-006).

---

## Phase 5: User Story 3 - Visualizing Humanoid Structure (Priority: P3)

**Goal**: URDF modeling and visualization.
**Independent Test**: Valid URDF file that renders in Rviz/Graphviz.

### Implementation for User Story 3

- [ ] T019 [US3] Create `simple_humanoid.urdf` in `code/module-1/urdf/simple_humanoid.urdf` with torso, head, arms
- [ ] T020 [US3] Add validation script or instruction in `website/docs/module-1/chapter-3-urdf.md`
- [ ] T021 [US3] Write Chapter 3 content "Humanoid Structure" in `website/docs/module-1/chapter-3-urdf.md`

**Checkpoint**: US3 verification (FR-004, SC-003).

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation cleanup.

- [ ] T022 Run full `colcon test` suite (sc-002)
- [ ] T023 Verify Docusaurus build locally `npm run build`
- [ ] T024 Ensure Quickstart guide `quickstart.md` commands match implemented paths

## Dependencies & Execution Order

1. **Setup (Phase 1)**: Parallelizable T001, T002, T003/T004.
2. **Foundational (Phase 2)**: Depends on Phase 1. T009 blocks all US.
3. **User Stories (Phase 3+)**:
   - US1 (T010-T015) can start after T009.
   - US2 (T016-T018) depends on T009 (technically independent of US1 code, but conceptually builds on it).
   - US3 (T019-T021) is independent of code logic, can run parallel to US1/US2.
4. **Polish**: Runs after all stories.

## Parallel Execution Example

```bash
# Parallel: UI setup + Code structure + Documentation scaffolding
Task: T002 Configure Docusaurus sidebars
Task: T003 Create ROS 2 package structure
Task: T008 Create placeholder content pages
```
