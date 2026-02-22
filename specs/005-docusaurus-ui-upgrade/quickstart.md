# Quickstart Guide: UI Upgrade for Docusaurus Website

**Feature**: [UI Upgrade for Docusaurus Website](specs/005-docusaurus-ui-upgrade/spec.md)
**Date**: 2026-02-22

This guide provides instructions to quickly set up the Docusaurus development environment and view the UI changes related to the feature "UI Upgrade for Docusaurus Website".

## Prerequisites

- Node.js (LTS version) installed
- npm or Yarn package manager installed

## Setup and Run the Docusaurus Website

1.  **Navigate to the `website` directory**:
    ```bash
    cd F:\ai native book\website
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    # or if you use Yarn
    # yarn install
    ```

3.  **Start the development server**:
    ```bash
    npm run start
    # or if you use Yarn
    # yarn start
    ```
    This command builds the website and serves it locally. A browser window should automatically open, typically at `http://localhost:3000`.

## Viewing UI Changes

Once the development server is running, you can:

-   **Browse the website**: Navigate through various pages (docs, blog, custom pages) to observe the updated visual theme, navigation components (navbar, footer, sidebar), typography, and spacing.
-   **Test responsiveness**: Resize your browser window or use browser developer tools (device emulation mode) to check how the UI adapts to different screen sizes (desktop, tablet, mobile).
-   **Inspect elements**: Use your browser's developer tools to inspect CSS properties and confirm that the styling aligns with the modernized design.

## Stopping the Development Server

To stop the Docusaurus development server, press `Ctrl+C` in the terminal where the `npm run start` (or `yarn start`) command is running.
