# Implementation Plan: Module 1: The Robotic Nervous System (ROS 2)

**Branch**: `001-ros2-basics` | **Date**: 2026-01-31 | **Spec**: [specs/001-ros2-basics/spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ros2-basics/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement Module 1 of the "AI Native" book, covering ROS 2 communication basics (Pub/Sub, Services), Python agents with `rclpy`, and robot structure visualization with URDF. This involves setting up the Docusaurus site structure to host the content and creating the Python code examples and XML models required by the specification.

## Technical Context

**Language/Version**: Python 3.10+ (for ROS 2 Humble/Jazzy), Node.js 18+ (for Docusaurus)
**Primary Dependencies**:
- ROS 2 (Humble or Jazzy) - `rclpy`
- Docusaurus 3.x
- `ament_python` (build system for ROS 2 Python packages)
- `urdf_tutorial` / `joint_state_publisher` (for checking URDFs)
**Storage**: N/A (Content is static Markdown + Python source files)
**Testing**:
- `ament_lint_auto` / `ament_flake8` for Python linting
- `launch_testing` or simple `unittest` for node integration tests
- `check_urdf` for XML validation
**Target Platform**: Linux (Ubuntu 22.04/24.04 typical for ROS 2), Static Web (GitHub Pages)
**Project Type**: Mixed (Static Site + Python Source Code)
**Performance Goals**: N/A (Education focus)
**Constraints**:
- Must support headless CI execution for verification.
- Content must be written in Markdown.
**Scale/Scope**: 3 Chapters, ~3-5 Python scripts, 1 URDF file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Spec-First Content and Code**: All content derived from `specs/001-ros2-basics/spec.md`.
- [x] **II. Traceable Requirements**: Python examples map to FR-001, FR-002; URDF maps to FR-004.
- [x] **III. Verifiable Technical Accuracy**: Code will include CI-compatible tests (SC-002, SC-005).
- [x] **IV. Developer-Focused Clarity**: Docusaurus structure prioritized for readability.
- [x] **V. Secure, Automated Workflows**: CI ensures code validity; static site deployment.

## Project Structure

### Documentation (this feature)

```text
specs/001-ros2-basics/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
docs/
├── intro.md                   # Docusaurus intro
├── module-1/                  # Module 1 Content
│   ├── chapter-1-basics.md    # ROS 2 Basics
│   ├── chapter-2-agents.md    # Python Agents
│   └── chapter-3-urdf.md      # Humanoid Structure
└── ...

website/                       # Docusaurus Project Root
├── docusaurus.config.js       # Site configuration
├── src/
├── static/
└── sidebars.js

code/                          # Companion Code Repository Structure
├── module-1/                  # Module 1 Code
│   ├── ros2_basics_py/        # ROS 2 Python Package
│   │   ├── setup.py
│   │   ├── package.xml
│   │   ├── ros2_basics_py/
│   │   │   ├── __init__.py
│   │   │   ├── simple_publisher.py
│   │   │   ├── simple_subscriber.py
│   │   │   ├── service_server.py
│   │   │   ├── service_client.py
│   │   │   └── smart_agent.py
│   │   └── test/
│   │       ├── test_pep257.py
│   │       └── test_flake8.py
│   └── urdf/
│       └── simple_humanoid.urdf
└── ...
```

**Structure Decision**: Split content (prose) and code. `website/` holds the Docusaurus instance. `code/` holds the verifiable source code referenced by the book. `docs/` inside the Docusaurus root typically, but here we might map it or keep it standard. We will use standard Docusaurus `docs/` folder for content and a parallel `code/` folder for the raw source files which can be embedded or linked.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Example Code separate from Docs | Automation/CI requires standard ROS 2 package structure for verification | Embedded code blocks in Markdown are harder to test automatically |
