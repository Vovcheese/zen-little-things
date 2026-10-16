# Publishing the repository

## GitHub About

**Name:** `zen-little-things`

**Description:** Thoughtful CSS mods for Zen Browser: clearer tab previews, a floating find bar, and readable sidebar folders.

**Topics:** `zen-browser`, `zen-mods`, `userchrome`, `css`, `browser-customization`, `firefox`

## Publish an update

The repository is [Vovcheese/zen-little-things](https://github.com/Vovcheese/zen-little-things). From the project directory, review and publish a focused update:

```sh
git status --short
git add .
git diff --cached --stat
git diff --cached --check
git commit -m "Describe the visible change"
git push origin main
```

Review the staged file list before committing. `.gitignore` excludes local logs, root-level development images, Python caches, private tooling directories, and generated browser fixtures. It does not remove files that were already tracked.

## Public preview checklist

- README accurately names supported install methods and known validation gaps.
- Every mod has its own README and versioned metadata.
- License and third-party notices are present.
- Repository contains no profile backups, local logs, or personal browser captures.
- Native screenshots have versioned captions, or illustrations are clearly identified.
- Installation, repeat installation, disabling, and Find highlight restoration have been checked for the build you announce.

Publish the initial collection as a **preview**, not a compatibility-certified stable release. Native visual validation is still pending in the current documentation. Close those gaps before describing it as tested on a build or platform.

## Suggested announcement

> Zen Little Things is a small collection of CSS customizations for Zen Browser: readable tab previews, a floating page-search panel, and clearer sidebar folders. Install each mod independently, keep native browser behavior, and adapt the look with CSS variables. This is an experimental public preview, with a macOS local installer and a documented manual CSS route. Compatibility reports and visual fixes are welcome.

## Later releases

Update each changed package's version and date, record the exact test environment, add a changelog entry, and attach clean captures when available. Local installations do not auto-update; tell users to download the new files and rerun their installer with Zen closed.
