# Setup

First-time setup for a new yearbook. This takes about 15 minutes.

## 1. Fork the template

On GitHub, click **"Use this template"** → **"Create a new repository"**.

Choose:

- **Owner**: your school's GitHub organization (recommended) or your personal account.
- **Repository name**: something like `yearbook-2025-2026`.
- **Visibility**: 🔒 **Private.** This is the important one.

> **Why private?** The template itself ships with stock data (the cast of
> *Malcolm in the Middle*) so it's safe to be public. But the moment you add
> a real student's name or photo, the repo contains sensitive data about
> minors. A private repo protects the raw files regardless of whether the
> deployed site is public or gated.

## 2. Pick a hosting posture

GitHub Pages from a private repo is **only available on paid GitHub plans**
(Pro, Team, Enterprise). Your options:

| Approach | Private repo | Public site | Cost |
|----------|:--:|:--:|------|
| **Public repo + public site** | ❌ | ✅ | free — **don't use this for real student data** |
| **Private repo + private Pages** | ✅ | ✅ (gated to org members) | GitHub paid plan |
| **Private repo + public Pages** | ✅ | ✅ | free on Pro, but the site itself is publicly readable — use `<meta name="robots" content="noindex">` (which the template sets by default) and consider putting Cloudflare Access in front of the URL |
| **Private repo + static host with auth** | ✅ | ✅ (auth required) | varies (Netlify, Vercel, Cloudflare Pages — most have free tiers) |

If you're unsure, the **safest** pattern for a real school yearbook is:

1. Private repo on GitHub
2. Build artifact deployed to a static host that supports password
   protection or SSO (Cloudflare Access is free for teams under 50)

For a proof-of-concept or family-only site where everyone has the direct
URL, private repo + private Pages is simplest.

## 3. Configure basics

Open `_config.yml` and change the top block:

```yaml
title: "Your Elementary School Yearbook"
description: "2025–2026 school year"
school_year: "2025–2026"
mascot: "The Rockets"
```

If your site will be deployed to a subpath (e.g. `https://org.github.io/yearbook/`),
also set `baseurl: "/yearbook"`. For a root domain, leave it empty.

## 4. Enable GitHub Pages + Actions

On your repo's GitHub page:

1. **Settings → Pages → Source**: set to **GitHub Actions**.
2. **Settings → Actions → General → Workflow permissions**: set to
   **Read and write permissions** (needed so the image-optimization workflow
   can commit resized photos back).

## 5. First build

Push any commit to `main`. Two workflows run:

- **Tests** (`.github/workflows/tests.yml`) — validates `people.yml` and
  cross-references. Must pass before the build runs.
- **Build & Deploy** (`.github/workflows/build.yml`) — builds Jekyll with the
  custom plugin and deploys to Pages.

Watch them under the **Actions** tab. First build takes ~2 minutes.

Your site URL appears at **Settings → Pages** once deploy completes.

## 6. Replace the example data

Work through [`ADDING-PEOPLE.md`](ADDING-PEOPLE.md). The short version:

1. Delete the example classes/clubs/sports files under `_classes/`,
   `_clubs/`, `_sports/`.
2. Replace `_data/people.yml` with your real roster (one entry per student,
   teacher, and staff member).
3. Drop photos into `assets/images/people/` named `<id>.jpg` to match.
4. Create one `.md` file per class, club, and team, listing members by ID.

## 7. Optional: enable the no-code editor

For volunteers who don't want to edit YAML, Decap CMS provides a form-based
editor at `/admin/`. Setup instructions (and the reasons you might skip
this) are in the comments at the top of `admin/config.yml`.

If your committee is comfortable with the GitHub web UI
(`github.com/<repo>/edit/main/_data/people.yml`), you can skip Decap CMS
entirely.
