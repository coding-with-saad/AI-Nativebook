/**
 * Any CSS included here will be global. The classic template
 * bundles Infima by default. Infima is a CSS framework designed to
 * work well for content-centric websites.
 */

/* You can override the default Infima variables here. */
:root {
  --ifm-color-primary: #2e8555;
  --ifm-color-primary-dark: #29784c;
  --ifm-color-primary-darker: #277148;
  --ifm-color-primary-darkest: #205d3b;
  --ifm-color-primary-light: #33925d;
  --ifm-color-primary-lighter: #359962;
  --ifm-color-primary-lightest: #3cad6e;
  --ifm-code-font-size: 95%;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.1);

  /* New UI Upgrade Variables - Light Mode */
  --ifm-color-primary: #3366ff; /* Modern blue */
  --ifm-color-primary-dark: #2a52cc;
  --ifm-color-primary-darker: #254aa3;
  --ifm-color-primary-darkest: #1e3a8a;
  --ifm-color-primary-light: #4c7dff;
  --ifm-color-primary-lighter: #6699ff;
  --ifm-color-primary-lightest: #99bbff;

  --ifm-color-secondary: #00b894; /* Complementary green */
  --ifm-color-tertiary: #fdcb6e; /* Accent yellow */

  --ifm-font-family-base: 'Inter', sans-serif; /* Modern sans-serif font */
  --ifm-font-family-code: 'Fira Code', monospace; /* Modern monospace font */

  --ifm-h1-font-size: 3rem;
  --ifm-h2-font-size: 2.5rem;
  --ifm-h3-font-size: 2rem;
  --ifm-h4-font-size: 1.5rem;
  --ifm-h5-font-size: 1.25rem;
  --ifm-h6-font-size: 1rem;

  --ifm-spacing-unit: 1rem; /* Base spacing unit */
  --ifm-spacing-xxs: calc(0.25 * var(--ifm-spacing-unit));
  --ifm-spacing-xs: calc(0.5 * var(--ifm-spacing-unit));
  --ifm-spacing-sm: calc(0.75 * var(--ifm-spacing-unit));
  --ifm-spacing-md: var(--ifm-spacing-unit);
  --ifm-spacing-lg: calc(1.5 * var(--ifm-spacing-unit));
  --ifm-spacing-xl: calc(2 * var(--ifm-spacing-unit));
  --ifm-spacing-xxl: calc(3 * var(--ifm-spacing-unit));

  --ifm-border-radius: 0.5rem; /* Rounded corners */
  --ifm-container-width: 1200px; /* Max content width */
}

/* For readability concerns, you should choose a lighter palette in dark mode. */
[data-theme='dark'] {
  --ifm-color-primary: #6699ff; /* Modern blue for dark mode */
  --ifm-color-primary-dark: #4c7dff;
  --ifm-color-primary-darker: #3366ff;
  --ifm-color-primary-darkest: #2a52cc;
  --ifm-color-primary-light: #99bbff;
  --ifm-color-primary-lighter: #b3ccff;
  --ifm-color-primary-lightest: #cce6ff;

  --ifm-color-secondary: #00e6b8; /* Complementary green for dark mode */
  --ifm-color-tertiary: #ffdd88; /* Accent yellow for dark mode */
}

/* General styling using new CSS variables */
body {
  font-family: var(--ifm-font-family-base);
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--ifm-font-family-base);
}

h1 { font-size: var(--ifm-h1-font-size); }
h2 { font-size: var(--ifm-h2-font-size); }
h3 { font-size: var(--ifm-h3-font-size); }
h4 { font-size: var(--ifm-h4-font-size); }
h5 { font-size: var(--ifm-h5-font-size); }
h6 { font-size: 0.9rem; } /* Adjusted for T013 */

/* Buttons */
.button {
  border-radius: var(--ifm-border-radius);
  background-color: var(--ifm-color-primary);
  color: white;
  padding: var(--ifm-spacing-sm) var(--ifm-spacing-md);
  transition: background-color 0.2s ease-in-out;
}

.button:hover {
  background-color: var(--ifm-color-primary-dark);
  text-decoration: none;
}

/* Links */
a {
  color: var(--ifm-color-primary);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

/* Cards (example for Docusaurus admonitions/blocks) */
.card {
  border-radius: var(--ifm-border-radius);
  border: 1px solid var(--ifm-color-primary-lightest);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: var(--ifm-spacing-lg);
  margin-bottom: var(--ifm-spacing-lg);
}

/* Specific Docusaurus elements might need targeting */
.navbar__link {
  font-weight: bold;
}

/* Sidebar Styling */
.sidebar {
  background-color: var(--ifm-background-color);
  border-right: 1px solid var(--ifm-color-emphasis-200);
}

.sidebar .menu__list-item--collapsed > .menu__link {
  font-weight: normal;
}

.sidebar .menu__link {
  border-radius: var(--ifm-border-radius);
  margin-bottom: var(--ifm-spacing-xxs);
}

.sidebar .menu__link:hover {
  background-color: var(--ifm-hover-background-color);
  color: var(--ifm-link-color);
}

.sidebar .menu__link--active {
  background-color: var(--ifm-color-primary-lightest);
  color: var(--ifm-color-primary);
  font-weight: bold;
}

/* Responsive adjustments for smaller screens */
@media screen and (max-width: 996px) {
  .main-wrapper {
    padding: var(--ifm-spacing-md);
  }

  h1 { font-size: 2.5rem; }
  h2 { font-size: 2rem; }
  h3 { font-size: 1.75rem; }
  h4 { font-size: 1.25rem; }
  h5 { font-size: 1.1rem; }
  h6 { font-size: 1rem; }

  /* Adjust spacing for mobile */
  .container {
    padding: 0 var(--ifm-spacing-md);
  }

  .row {
    margin-left: calc(-1 * var(--ifm-spacing-md));
    margin-right: calc(-1 * var(--ifm-spacing-md));
  }

  .col {
    padding-left: var(--ifm-spacing-md);
    padding-right: var(--ifm-spacing-md);
  }
}

/* Adjustments for even smaller screens (e.g., mobile portrait) */
@media screen and (max-width: 768px) {
  h1 { font-size: 2rem; }
  h2 { font-size: 1.75rem; }
  h3 { font-size: 1.5rem; }
  h4 { font-size: 1.1rem; }
  h5 { font-size: 1rem; }
  h6 { font-size: 0.9rem; }

  /* More compact spacing for mobile */
  --ifm-spacing-unit: 0.8rem;
}
/*
 * Task T018: Applied typographic scale and spacing using CSS variables.
 * Verification: Ensure the entire theme consistently uses these variables for text and spacing elements.
 */

/* Consistent Spacing Rules */
p {
  margin-bottom: var(--ifm-spacing-md);
}

ul, ol {
  margin-bottom: var(--ifm-spacing-md);
  padding-left: var(--ifm-spacing-lg);
}

li {
  margin-bottom: var(--ifm-spacing-xs);
}

img {
  margin-top: var(--ifm-spacing-lg);
  margin-bottom: var(--ifm-spacing-lg);
  max-width: 100%;
  height: auto;
}

/* Headings spacing */
h1, h2, h3, h4, h5, h6 {
  margin-top: var(--ifm-spacing-xl);
  margin-bottom: var(--ifm-spacing-md);
}

h1:first-child, h2:first-child, h3:first-child {
  margin-top: var(--ifm-spacing-md); /* Less top margin if it's the first element */
}

/* Unique Logo Styling */
.navbar__logo {
  height: 2rem; /* Smaller height to fit inside header */
  margin-right: 0.5rem;
  transition: transform 0.3s ease-in-out, filter 0.3s ease-in-out;
  filter: drop-shadow(0 0 2px rgba(51, 102, 255, 0.3));
}

.navbar__logo:hover {
  transform: scale(1.05); /* Slightly smaller scale on hover */
  filter: drop-shadow(0 0 6px rgba(51, 102, 255, 0.6));
}

.navbar__brand {
  display: flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  border-radius: var(--ifm-border-radius);
  transition: background-color 0.2s ease;
}

.navbar__brand:hover {
  background-color: var(--ifm-color-emphasis-100);
  text-decoration: none;
}




Build RAG agent with retrieval capability

Target:
Create an AI agent using OpenAI Agents SDK that integrates Qdrant retrieval to answer questions based on stored book embeddings.

Success criteria:
- Agent receives user query and triggers retrieval pipeline
- Query embedded using same embedding model as ingestion
- Top_k relevant chunks retrieved from Qdrant
- Retrieved context injected into agent prompt
- Agent generates answer grounded only in retrieved content
- Logs show retrieved sources and response time
- System prevents hallucination outside provided context


Constraints:
- No frontend integration yet
- No deployment scaling
- No authentication system
- No analytics or monitoring layer

Not building:
- UI interface
- Backend-frontend connection
- Advanced memory system
- Multi-agent orchestration