# Developing

This doc is for people hacking on the template itself — fixing bugs,
adding features, or adapting it significantly beyond what
[`CUSTOMIZING.md`](CUSTOMIZING.md) covers.

## Prerequisites

- **Ruby 3.2+** with Bundler (for Jekyll)
- **Python 3.10+** (for the test suite)
- **Node 20+** (only if you want to run the image-optimization script locally)

## Local preview

```bash
bundle install
bundle exec jekyll serve
# → http://localhost:4000
```

Jekyll watches for file changes and rebuilds automatically.

## Running tests

```bash
pip install -r tests/requirements.txt
pytest
```

The suite is pure Python (no Ruby needed) and validates data integrity,
cross-references, and site structure. It runs in under a second. See
[`../tests/`](../tests/) for the actual test files — each is heavily
commented.

## Repository layout

```
_config.yml              Site config. Labels, collections, identity.
_data/
  people.yml             THE master people list. Everything else references this.
_classes/                One .md file per class. Minimal front-matter.
_clubs/                  One .md file per club.
_sports/                 One .md file per team.
_layouts/
  default.html           Shared page chrome
  home.html              Landing page
  class.html             Class page
  club.html              Club page
  sport.html             Sports team page
  person.html            Individual profile (auto-generated from people.yml)
  staff.html             Staff directory
_includes/
  head.html              <head> contents (fonts, CSS, meta tags)
  header.html            Top nav bar + search input
  footer.html            Footer + deferred script load
  person-card.html       Reusable photo card for a person
_plugins/
  people_generator.rb    Custom Jekyll plugin — creates /people/<id>/ pages +
                         builds the memberships reverse index
assets/
  css/main.css           All styles. CSS variables at the top.
  js/search.js           Client-side search (fetches /people.json)
  images/
    people/              Student/teacher/staff photos, named <id>.jpg
    site/                Favicon, placeholder SVG
admin/                   Decap CMS (optional form-based editor)
tests/                   pytest suite — validates data and structure
docs/                    Maintainer docs (this folder). Excluded from the build.
.github/workflows/
  tests.yml              Runs pytest on every push/PR
  build.yml              Builds Jekyll + deploys to Pages (gated on tests)
  optimize-images.yml    Resizes + strips EXIF from pushed photos
people.json              Liquid template → auto-generated search index
index.md                 Home page (uses home.html layout)
staff.md                 Staff page
help.md                  End-user help page at /help/
404.html                 404 page
```

## How the people pipeline works

This is the one non-obvious bit of the site.

1. A volunteer adds a person to `_data/people.yml` and references their ID
   in a class/club/sport roster.
2. At build time, `_plugins/people_generator.rb` runs:
   - **Normalization pass**: walks `site.data.people` and adds derived
     fields to each record — `display_name`, `initials`, `photo` URL,
     profile `url`. Also builds a lookup table at `site.data.people_by_id`.
   - **Reverse index pass**: walks every doc in the classes/clubs/sports
     collections and records which rosters reference each person.
   - **Page generation**: creates a `Jekyll::Page` at `/people/<id>/` for
     every person, passing their record and memberships to `person.html`.
3. `people.json` is a Liquid template with `permalink: /people.json` — at
   build time Jekyll renders it into a real JSON file at the site root.
4. The header's search `<input>` is wired up by `assets/js/search.js`, which
   fetches `/people.json` on first focus and filters in the browser.

## Why GitHub Actions for the build

GitHub's native Pages builder only allows a whitelisted set of Jekyll
plugins, and the custom `people_generator.rb` isn't on it. Building via
Actions (`.github/workflows/build.yml`) lets us run any plugin we want.

The tradeoff is a slightly more involved CI config — but it's also what
enables the test-gating: tests run in `tests.yml`, and `build.yml` is
`needs: test`, so a failing test stops the deploy cold.

## Common tasks

### Adding a new field that every person should have

1. Add the field to example entries in `_data/people.yml`.
2. Add a test in `tests/test_people_data.py` validating its presence/shape.
3. Reference it wherever you want it displayed (`_layouts/person.html`,
   `_includes/person-card.html`).

### Changing the photo URL convention

Edit `photo_path_default` in `_config.yml`. The Ruby plugin reads this at
build time and applies it to any person without an explicit `photo:` field.

### Changing what appears in search results

Edit `people.json` (the Liquid template — it emits the fields the search
index contains) and `assets/js/search.js` (how results are rendered).

### Adding a new collection (events, field trips, etc.)

See the "Adding a new page type" section in [`CUSTOMIZING.md`](CUSTOMIZING.md).
You'll also want to:

- Add the new collection's roster fields to the reverse-index pass in
  `_plugins/people_generator.rb` if you want the new pages to appear in
  "Appears in" on person profiles.
- Add a test in `tests/test_references.py` that validates person-ID
  references in the new collection resolve.

## Debugging tips

- **Page not generated for a person**: check the plugin's `priority :high`
  is firing early enough. Look at the Jekyll build output for any plugin
  exceptions.
- **"Unknown: some-id" showing up in the rendered site**: you have a bad
  reference. The test suite catches these in CI, but you'll see them in
  local preview if you bypass tests.
- **Liquid error about `nil` method**: almost always means
  `site.data.people_by_id` wasn't populated yet when a template tried to
  read it. The plugin's high priority should prevent this.
- **EXIF metadata still present on a photo**: the optimize workflow only
  runs on push; locally, run `node scripts/optimize-photos.js` manually.

## Known limitations

- **Single school year per repo.** Multi-year archives aren't built in. The
  suggested workflow is "Use this template" → make a new repo for each year.
- **No native access control.** Privacy posture is up to the host (see
  [`SETUP.md`](SETUP.md)).
- **No bulk import.** There's no "upload a CSV of students" flow yet. For
  large rosters, scripting a one-time conversion into `people.yml` is
  straightforward — it's just a YAML list.
