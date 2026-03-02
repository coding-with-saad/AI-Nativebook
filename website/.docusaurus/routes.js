import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/blog',
    component: ComponentCreator('/blog', 'b2f'),
    exact: true
  },
  {
    path: '/blog/archive',
    component: ComponentCreator('/blog/archive', '182'),
    exact: true
  },
  {
    path: '/blog/authors',
    component: ComponentCreator('/blog/authors', '0b7'),
    exact: true
  },
  {
    path: '/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/blog/authors/all-sebastien-lorber-articles', '4a1'),
    exact: true
  },
  {
    path: '/blog/authors/yangshun',
    component: ComponentCreator('/blog/authors/yangshun', 'a68'),
    exact: true
  },
  {
    path: '/blog/first-blog-post',
    component: ComponentCreator('/blog/first-blog-post', '89a'),
    exact: true
  },
  {
    path: '/blog/long-blog-post',
    component: ComponentCreator('/blog/long-blog-post', '9ad'),
    exact: true
  },
  {
    path: '/blog/mdx-blog-post',
    component: ComponentCreator('/blog/mdx-blog-post', 'e9f'),
    exact: true
  },
  {
    path: '/blog/tags',
    component: ComponentCreator('/blog/tags', '287'),
    exact: true
  },
  {
    path: '/blog/tags/docusaurus',
    component: ComponentCreator('/blog/tags/docusaurus', '704'),
    exact: true
  },
  {
    path: '/blog/tags/facebook',
    component: ComponentCreator('/blog/tags/facebook', '858'),
    exact: true
  },
  {
    path: '/blog/tags/hello',
    component: ComponentCreator('/blog/tags/hello', '299'),
    exact: true
  },
  {
    path: '/blog/tags/hola',
    component: ComponentCreator('/blog/tags/hola', '00d'),
    exact: true
  },
  {
    path: '/blog/welcome',
    component: ComponentCreator('/blog/welcome', 'd2b'),
    exact: true
  },
  {
    path: '/markdown-page',
    component: ComponentCreator('/markdown-page', '3d7'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '0c2'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'b53'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '360'),
            routes: [
              {
                path: '/docs/category/module-1',
                component: ComponentCreator('/docs/category/module-1', '239'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/category/module-2',
                component: ComponentCreator('/docs/category/module-2', 'd37'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/category/module-3',
                component: ComponentCreator('/docs/category/module-3', 'b1d'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/category/module-4',
                component: ComponentCreator('/docs/category/module-4', '995'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '853'),
                exact: true
              },
              {
                path: '/docs/module-1/chapter-1-basics',
                component: ComponentCreator('/docs/module-1/chapter-1-basics', '961'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-1/chapter-2-agents',
                component: ComponentCreator('/docs/module-1/chapter-2-agents', 'd95'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-1/chapter-3-urdf',
                component: ComponentCreator('/docs/module-1/chapter-3-urdf', 'f94'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-2/gazebo-physics',
                component: ComponentCreator('/docs/module-2/gazebo-physics', 'f8f'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-2/sensor-simulation',
                component: ComponentCreator('/docs/module-2/sensor-simulation', '6a5'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-2/sim-to-real-validation',
                component: ComponentCreator('/docs/module-2/sim-to-real-validation', 'e09'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-2/unity-environments',
                component: ComponentCreator('/docs/module-2/unity-environments', 'a35'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-3/isaac-ros-vslam-acceleration',
                component: ComponentCreator('/docs/module-3/isaac-ros-vslam-acceleration', 'c2b'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-3/isaac-sim-synthetic-data',
                component: ComponentCreator('/docs/module-3/isaac-sim-synthetic-data', '282'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-3/nav2-humanoid-planning',
                component: ComponentCreator('/docs/module-3/nav2-humanoid-planning', '89b'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-4/capstone-vla-pipeline',
                component: ComponentCreator('/docs/module-4/capstone-vla-pipeline', 'fc7'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-4/llm-cognitive-planning',
                component: ComponentCreator('/docs/module-4/llm-cognitive-planning', '2a5'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/module-4/voice-to-action',
                component: ComponentCreator('/docs/module-4/voice-to-action', 'e3f'),
                exact: true,
                sidebar: "moduleSidebar"
              },
              {
                path: '/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/docs/tutorial-basics/congratulations', '70e'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/docs/tutorial-basics/create-a-blog-post', '315'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/docs/tutorial-basics/create-a-document', 'f86'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/docs/tutorial-basics/create-a-page', '9f6'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/docs/tutorial-basics/deploy-your-site', 'b91'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/docs/tutorial-basics/markdown-features', '272'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/docs/tutorial-extras/manage-docs-versions', 'a34'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/docs/tutorial-extras/translate-your-site', '739'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2e1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
