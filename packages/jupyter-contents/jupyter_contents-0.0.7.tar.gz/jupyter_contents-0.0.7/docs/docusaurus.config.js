/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
  title: '🪐 💼 Jupyter Contents documentation',
  tagline: 'Jupyter Contents documentation',
  url: 'https://datalayer.io',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'datalayer', // Usually your GitHub org/user name.
  projectName: 'datalayer', // Usually your repo name.
  themeConfig: {
    colorMode: {
      defaultMode: 'light',
      disableSwitch: true,
    },
    navbar: {
      title: 'Jupyter Contents Docs',
      logo: {
        alt: 'Datalayer Logo',
        src: 'img/datalayer/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'index',
          position: 'left',
          label: 'Jupyter Contents',
        },
        {
          href: 'https://bsky.app/profile/datalayer.io',
          position: 'right',
          className: 'header-bluesky-link',
          'aria-label': 'Bluesky',
        },
        {
          href: 'https://www.linkedin.com/company/datalayer',
          position: 'right',
          className: 'header-linkedin-link',
          'aria-label': 'LinkedIn',
        },
        {
          href: 'https://github.com/datalayer/jupyter-contents',
          position: 'right',
          className: 'header-github-link',
          'aria-label': 'GitHub',
        },
        {
          href: 'https://datalayer.io',
          position: 'right',
          className: 'header-datalayer-io-link',
          'aria-label': 'Datalayer',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Jupyter Contents',
              to: '/docs',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Bluesky',
              href: 'https://assets.datalayer.tech/logos-social-grey/youtube.svg',
            },
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/company/datalayer',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/datalayer',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Datalayer IO',
              href: 'https://datalayer.io',
            },
            {
              label: 'Datalayer IO',
              href: 'https://datalayer.io',
            },
            {
              label: 'Datalayer Run',
              href: 'https://datalayer.run',
            },
            {
              label: 'Datalayer Tech',
              href: 'https://datalayer.tech',
            },
            {
              label: 'Clouder',
              href: 'https://clouder.sh',
            },
            {
              label: 'Datalayer Blog',
              href: 'https://datalayer.blog',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Datalayer, Inc.`,
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl:
            'https://github.com/datalayer/jupyter-contents/edit/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
