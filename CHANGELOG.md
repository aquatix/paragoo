## v0.3.0 (unreleased)

2016-05-??

- Fixed AppNotFoundException in androidapp plugin
- Tags are now recursively expanded (so a tile inside a news item gets rendered)
- Markdown support for tiles
- Minor bugfixes


## v0.2.0

2016-04-24

- More robust template loading
- Less verbose on generating things (less output)
- Navigation-type is configurable:
  - default switches from mobile view to desktop view
  - option to always show a mobile-like list (depending on theme of course)
  - in material theme, this shows a nested navigation bar to the left instead
    of a topbar navigation
- Copy site-specific css files to destination
- Support for page titles to be used in the navigation (`navtitle`), to be able
  to show short titles in navigation and have the original longer ones in the pages
- Better Android app info from the tag plugin
- Table-of-contents support for Markdown (`[TOC]`)
- ReST (reStructuredText) support
- (Initial) Support for generating a sitemap
- Cache busting for styling and script assets (append timestamp to filename), automatically renaming files where needed
- Support comments in news listings, skipping the item


## v0.1.0

2016-03-26

- Initial release
- Support for HTML files, Markdown files
- Custom themes
- Automatic generation of navigation
- Copying of static assets
- Plugins to render tags to content:
  - Android applications (crawl info from PlayStore)
  - Icons
  - News items
  - Tiles (blocks of html/md)
  - Initial support for galleries
