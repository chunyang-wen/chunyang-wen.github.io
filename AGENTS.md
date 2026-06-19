# Repository Guidelines

## Project Structure & Module Organization
This repository is a Jekyll blog built on the Chirpy theme. Core site settings live in `_config.yml`. Write posts in `_posts/`, usually under year folders, using `YYYY-MM-DD-title.md`. Static pages live in `_tabs/`, shared templates in `_includes/` and `_layouts/`, and structured data in `_data/`. Site assets belong in `assets/` and `images/`. Helper scripts for local workflows live in `scripts/`. Generated output is written to `_site/`; treat it as build output and avoid hand-editing files there.

## Build, Test, and Development Commands
Install dependencies with `bundle install`. Run the site locally with `bundle exec jekyll serve` or `./scripts/build_page.sh serve`. Create a production build with `bundle exec jekyll build` or `bundle exec jekyll b -d _site`. Use `./scripts/build_page.sh init` only for first-time Ruby setup. Content helpers such as `./scripts/daily.sh slug.md` and `./scripts/digest.sh` generate draft post templates.

## Coding Style & Naming Conventions
Use Markdown with concise YAML front matter. Follow existing keys such as `layout`, `title`, `categories`, `tags`, and `image`. Prefer lowercase, hyphen-separated filenames for posts and asset folders, for example `_posts/2025/2025-01-04-construct-the-rectangle.md`. Keep indentation consistent with surrounding files: two spaces in YAML, four spaces only where required by code blocks or existing HTML. Do not edit compiled files like `assets/js/dist/theme.min.js` unless you are intentionally updating vendored output.

## Testing Guidelines
There is no dedicated automated test suite in this repository. The required validation step is a clean local build with `bundle exec jekyll build`. Before opening a PR, also run `bundle exec jekyll serve` and verify changed pages, links, images, and front matter locally. For content-heavy changes, check the generated page under `_site/` before publishing.

## Commit & Pull Request Guidelines
Recent history uses short, imperative commit subjects such as `Update cover` and `Update link`. Keep commits focused and descriptive, for example `Add post on Jekyll image handling`. Pull requests should summarize the user-visible change, list any config or content paths touched, and include screenshots for layout or styling changes. Link related issues when relevant and note the local build command you used for verification.

## Content & Publishing Notes
Posts default to the `post` layout and permalink structure defined in `_config.yml`. Keep category and tag names consistent with existing taxonomy to avoid fragmented archives. Store large media under `images/posts/...` and reference them with root-relative paths such as `/images/posts/2025/example/cover.png`.

## Test

You can use `make serve` to build and serve the page.
