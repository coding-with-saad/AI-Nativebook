# Tasks: Module 4: Vision-Language-Action (VLA) Module

**Branch**: `004-vla-robot-brain` | **Spec**: [specs/004-vla-robot-brain/spec.md](./spec.md)
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md

**Organization**: Tasks are grouped by user story (P1, P2) to enable independent implementation and testing.

## Phase 1: Setup (Project Initialization)

**Purpose**: Establish core directory structures and Docusaurus integration points for Module 4.

- [X] T001 Create `code/module-4/vla_system/` for the main VLA ROS 2 package
- [X] T002 Create `code/module-4/llm_tools/` for LLM interaction scripts and tools
- [X] T003 Create `code/module-4/audio_interface/` for audio capture and Whisper integration
- [X] T004 Configure Docusaurus category definition in `website/docs/module-4/_category_.json`
- [X] T005 Create placeholder Docusaurus chapter files: `website/docs/module-4/voice-to-action.md`
- [X] T006 Create placeholder Docusaurus chapter files: `website/docs/module-4/llm-cognitive-planning.md`
- [X] T007 Create placeholder Docusaurus chapter files: `website/docs/module-4/capstone-vla-pipeline.md`
- [X] T008 Update `website/sidebars.js` to include Module 4 in the documentation sidebar

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Set up basic ROS 2 packages and dependencies for VLA.

- [X] T009 Set up ROS 2 package `audio_interface` (e.g., `package.xml`, `CMakeLists.txt`) in `code/module-4/audio_interface/`
- [X] T010 Set up ROS 2 package `vla_system` (e.g., `package.xml`, `CMakeLists.txt`) in `code/module-4/vla_system/`
- [X] T011 [P] Create placeholder script for LLM interaction in `code/module-4/llm_tools/llm_interface.py`

## Phase 3: User Story 1 - Voice Command Processing and Action Mapping (Priority: P1)

**Goal**: Enable robot to understand and react to spoken commands.
**Independent Test**: Spoken command successfully translates to robot action.

### Implementation for User Story 1

- [X] T012 [US1] Integrate Whisper model with ROS 2 (e.g., subscribe to audio, publish text) in `code/module-4/audio_interface/src/whisper_node.py`
- [X] T013 [US1] Develop action mapping logic to convert transcribed text to ROS 2 commands in `code/module-4/vla_system/src/action_mapper_node.py`
- [X] T014 [US1] Create a simple ROS 2 action server/publisher for robot base movement commands (e.g., `Twist`) in `code/module-4/vla_system/src/robot_action_server.py`
- [X] T015 [US1] Create launch file for Voice-to-Action pipeline in `code/module-4/vla_system/launch/voice_to_action.launch.py`
- [X] T016 [US1] Write Docusaurus chapter: "Voice-to-Action (Whisper + ROS 2)" in `website/docs/module-4/voice-to-action.md`

## Phase 4: User Story 2 - LLM-Based Cognitive Planning (Priority: P1)

**Goal**: Enable robot to perform higher-level cognitive planning.
**Independent Test**: LLM successfully decomposes complex tasks into sub-actions.

### Implementation for User Story 2

- [X] T017 [US2] Integrate LLM access (API or local) into `code/module-4/llm_tools/llm_interface.py`
- [X] T018 [US2] Develop LLM prompt engineering for task decomposition and function calling in `code/module-4/llm_tools/llm_prompts.py`
- [X] T019 [US2] Implement a ROS 2 node to interface with the LLM for planning in `code/module-4/vla_system/src/llm_planner_node.py`
- [X] T020 [US2] Create ROS 2 action client for executing LLM-generated actions in `code/module-4/vla_system/src/llm_planner_node.py`
- [X] T021 [US2] Create launch file for LLM-Based Cognitive Planning in `code/module-4/vla_system/launch/llm_planning.launch.py`
- [X] T022 [US2] Write Docusaurus chapter: "LLM-Based Cognitive Planning" in `website/docs/module-4/llm-cognitive-planning.md`

## Phase 5: User Story 3 - Capstone: Autonomous Humanoid Pipeline (Priority: P2)

**Goal**: Build a complete VLA pipeline for autonomous humanoid operation.
**Independent Test**: Complex voice command leads to successful task execution in simulation.

### Implementation for User Story 3

- [X] T023 [US3] Integrate perception system outputs (from Module 3) into the VLA pipeline
- [X] T024 [US3] Implement reactive planning and error recovery mechanisms in `code/module-4/vla_system/src/capstone_pipeline_node.py`
- [X] T025 [US3] Create a comprehensive launch file for the Capstone VLA pipeline in `code/module-4/vla_system/launch/capstone_vla_pipeline.launch.py`
- [X] T026 [US3] Write Docusaurus chapter: "Capstone: Autonomous Humanoid Pipeline" in `website/docs/module-4/capstone-vla-pipeline.md`

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation cleanup.

- [X] T027 Verify all internal links and code imports in Docusaurus site
- [X] T028 Run `npm run build` in `website/` to ensure production readiness
- [X] T029 Update `specs/004-vla-robot-brain/quickstart.md` with final installation and running commands
- [X] T030 Final review of Docusaurus navigation flow and sidebar for Module 4

## Dependencies & Execution Order

1.  **Setup (Phase 1)**: T001-T008 are largely independent but should be completed before other phases begin. T008 (sidebar update) depends on T004-T007 (chapter creation).
2.  **Foundational (Phase 2)**: T009-T011 depend on Phase 1 completion.
3.  **User Stories (Phase 3-5)**:
    -   US1 (Phase 3): Depends on Phase 2.
    -   US2 (Phase 4): Depends on Phase 2, and potentially US1 (for shared LLM/action interfaces).
    -   US3 (Phase 5): Strongly depends on US1, US2, and integration with Module 3.
4.  **Polish (Phase 6)**: T027-T030 depend on all previous phases being completed.

## Parallel Execution Example

```bash
# Phase 1: Setup
Task: T001 Create VLA system package directory
Task: T004 Configure Docusaurus category
```

```bash
# Once Foundational (Phase 2) is complete:
# US1 (Phase 3) & US2 (Phase 4) can have parallel implementation of core logic and Docusaurus content
Task: T012 Integrate Whisper model
Task: T017 Integrate LLM access
```

## Implementation Strategy
-   **MVP**: Focus on completing Phase 1 and 2, then US1 (Voice Command Processing and Action Mapping) to establish the basic natural language interface.
-   **Incremental**: Add US2 (LLM-Based Cognitive Planning) building upon the action mapping. US3 (Capstone) integrates all components, including Module 3.
