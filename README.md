# AI Native: Building Intelligent Robotic Systems

Welcome to the "AI Native" book project! This repository contains the companion code, documentation, and development history for a comprehensive guide to building modern, AI-powered robotic systems from the ground up.

## Project Overview

This project is structured as a series of modules, each building upon the last to create a sophisticated, autonomous humanoid robot. We follow a spec-driven development (SDD) approach, with detailed specifications, plans, and tasks for each module.

The core of this project is a Docusaurus-based website that serves as the book, providing step-by-step tutorials, explanations, and code examples. Recently, we've enhanced the interactive experience by integrating a Retrieval-Augmented Generation (RAG) chatbot, allowing users to ask questions directly from the book's content.

## Project Status

-   **Module 1: ROS 2 Basics:** Planned and initial setup complete.
-   **Module 2: Digital Twin:** Implemented, providing a simulated environment for the robot.
-   **Module 3: NVIDIA Isaac Brain:** Implemented, integrating advanced perception and navigation.
-   **Module 4: Vision-Language-Action (VLA) Module:** Implemented, enabling natural language interaction.
-   **Website:** The Docusaurus website is live and has been recently upgraded for a better user experience.
-   **RAG Chatbot Integration:** Implemented, providing an interactive Q&A experience based on the book content.

## New Feature: RAG Chatbot

An interactive RAG chatbot has been integrated into the Docusaurus frontend. This feature allows users to:
-   Ask questions directly related to the book's content.
-   Receive answers grounded in the provided documentation.
-   See source citations (from the book sections) for the generated answers.

The chatbot UI is accessible via a persistent floating button on the Docusaurus website.

## Modules

### Module 1: ROS 2 Basics

This module introduces the fundamental concepts of the Robot Operating System (ROS 2), the backbone of our robotic system. Key topics include:

-   ROS 2 nodes, topics, services, and actions.
-   Creating and managing ROS 2 packages.
-   Basic robot modeling with URDF.

### Module 2: Digital Twin

In this module, we create a digital twin of our robot in a simulated environment using Gazebo. This allows for safe and efficient development and testing of our robot's behaviors. Key topics include:

-   Setting up a Gazebo simulation environment.
-   Integrating sensors and actuators in the simulation.
-   Validating the simulated robot against its real-world counterpart.

### Module 3: NVIDIA Isaac Brain

This module leverages the power of NVIDIA Isaac to give our robot advanced perception and navigation capabilities. Key topics include:

-   Integrating Isaac ROS for perception, including VSLAM for localization.
-   Using Nav2 for autonomous path planning and navigation.
-   Generating synthetic data with Isaac Sim for training AI models.

### Module 4: Vision-Language-Action (VLA) Module

The capstone of our project, this module implements a Vision-Language-Action (VLA) pipeline that allows our humanoid robot to understand and react to natural language commands. Key topics include:

-   Integrating voice recognition with Whisper.
-   Using Large Language Models (LLMs) for cognitive planning and task decomposition.
-   Mapping LLM-generated plans to executable robot actions.
-   Implementing reactive planning and error recovery mechanisms.

## Technologies Used

-   **Robotics**: ROS 2 (Humble/Iron), Gazebo
-   **AI/ML**: NVIDIA Isaac, OpenAI Whisper, Large Language Models (LLMs), OpenAI Agents SDK, Qdrant (for retrieval)
-   **Backend**: Python, FastAPI
-   **Frontend**: Docusaurus, React
-   **Documentation**: Docusaurus
-   **Development**: Python, C++, Git, Spec-Driven Development (SDD)

## Getting Started

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/coding-with-saad/AI-Nativebook.git
    cd AI-Nativebook
    ```

2.  **Set up Environment Variables**:
    Create a `.env` file in the project root and add your API keys. For the RAG chatbot, you'll need an API key for the LLM. Example:
    ```
    Openrouter_api_key="sk-your-openrouter-api-key"
    ```

3.  **Backend Setup (RAG API)**:
    Navigate to the project root (`F:\ai native book`) in your terminal.
    ```bash
    # Install Python dependencies
    pip install -r requirements.txt # Or individually: pip install fastapi uvicorn python-dotenv openai-agents
    
    # Run the backend server
    python -m uvicorn api:app --reload --port 8000
    ```
    Keep this terminal window open and running.

4.  **Frontend Setup (Docusaurus Website)**:
    Open a **new terminal window** and navigate to the `website` directory (`F:\ai native book\website`).
    ```bash
    # Install Node.js dependencies
    npm install
    
    # Run the frontend development server
    npm start
    ```
    Keep this terminal window open and running.

5.  **Explore the website**:
    Once both the backend and frontend are running, open your web browser and navigate to `http://localhost:3000`. You should see the Docusaurus website with the interactive RAG chatbot available via a floating button.

## Project Structure

-   `api.py`: The FastAPI application for the RAG backend.
-   `src/`: Contains core Python modules, including `agent.py` and `retrieval_pipeline.py`.
-   `code/`: Contains the source code for each robotic module, organized by module number.
-   `website/`: The Docusaurus project for the book's frontend.
-   `specs/`: Detailed specifications, plans, and tasks for each module and feature.
-   `history/`: Prompt History Records (PHRs) and Architectural Decision Records (ADRs) that document the development process.
-   `.env`: Environment variables for API keys and configurations.

We hope you find this project informative and inspiring. Happy building!
