# pr-assets

Screenshots, walkthroughs and other material linked from pull request descriptions, kept here so they do not
add files to the repositories the pull requests are in.

## Layout

One folder per repository, then one per pull request, named `<PR number>-<short-name>`:

```
<repository>/<PR number>-<short-name>/...
```

- A PR description embeds an image with its raw URL:
  `https://raw.githubusercontent.com/nickshulman/pr-assets/main/<repository>/<folder>/<file>.png`
- It links a document or a folder with its page URL:
  `https://github.com/nickshulman/pr-assets/blob/main/<repository>/<folder>/<file>.md`
- Markdown inside a folder links its own images relatively (`images/s-01.png`), which GitHub renders.

This repository is public so that the images show to anyone reading the pull request. Nothing goes here that
could not be shown in the pull request itself.

## Contents

| Repository | Pull request | Folder |
|---|---|---|
| ProteoWizard/pwiz | [#4726](https://github.com/ProteoWizard/pwiz/pull/4726) AI connector gaps found by walking the tutorials through MCP | [pwiz/4726-mcp-walkthroughs](pwiz/4726-mcp-walkthroughs) |
| ProteoWizard/pwiz | [#4748](https://github.com/ProteoWizard/pwiz/pull/4748) Off-screen rendering fallback for form images | [pwiz/4748-offscreen-rendering](pwiz/4748-offscreen-rendering) |
