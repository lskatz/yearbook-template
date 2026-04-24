# Photo pages

Photo pages are freeform scrapbook-style pages you can add anywhere in the
yearbook. Unlike class, club, or sports pages — which are tied to a roster of
students — a photo page is just a collection of photos grouped under a single
title. Use them for school events, field trips, assemblies, science fairs, or
any occasion that doesn't have its own roster page.

Each photo on the page can optionally have:

- a **description** — a short free-text caption
- **labels** — a list of person IDs identifying people in the photo; their
  names are resolved automatically from `_data/people.yml` and each name links
  back to that person's profile page

---

## Quick example

Create a file in `_photos/`. The filename becomes the URL slug
(e.g. `field-day.md` → `/photos/field-day/`):

```markdown
---
title: "Field Day 2026"
date: "May 15, 2026"
thumbnail: "/assets/images/photos/field-day-thumb.jpg"
photos:
  - src: "/assets/images/photos/field-day-race.jpg"
    description: "Students at the sack race"
    labels:
      - malcolm-wilkerson
      - reese-wilkerson
  - src: "/assets/images/photos/field-day-pie.jpg"
    description: "Pie-eating contest winners!"
    labels:
      - dewey-wilkerson
  - src: "/assets/images/photos/field-day-group.jpg"
    # no description or labels — both are optional
---

Field Day was a huge success! Everyone competed in relay races,
a sack race, and the always-popular pie-eating contest.
```

---

## Front-matter reference

| Field | Required | Description |
|---|---|---|
| `title` | **yes** | Page title, shown in the page header and on the home page card |
| `date` | no | Optional date string shown beneath the title, e.g. `"May 15, 2026"` |
| `thumbnail` | no | Path to the image used for the home page index card. Falls back to `photo_thumbnail_default` in `_config.yml`. Set to `""` to suppress. |
| `photos` | no | List of photo objects — see below. Omit entirely for a text-only page. |

### Photo object fields

Each entry in the `photos:` list accepts:

| Field | Required | Description |
|---|---|---|
| `src` | **yes** | Path to the image file, e.g. `"/assets/images/photos/field-day-race.jpg"` |
| `description` | no | Short free-text caption displayed under the photo |
| `labels` | no | Ordered list of person IDs identifying people in the photo. Names are looked up from `_data/people.yml` and linked to their profile pages. |

---

## Step-by-step: adding a photo page

### Step 1: Upload your photos

Save your photos anywhere under `assets/images/`. A dedicated folder makes
things tidy:

```
assets/images/photos/field-day-race.jpg
assets/images/photos/field-day-pie.jpg
```

**Tips:**
- JPEG is preferred; PNG and WebP also work.
- Landscape (3:2 or 4:3) photos look best in the gallery grid.
- Anything up to ~10 MB is fine — oversized images are auto-resized to
  1200 px wide and GPS/EXIF metadata is stripped on push.

### Step 2: Create the page file

Add a `.md` file in `_photos/`. Name it in kebab-case — the filename
becomes the URL slug:

```
_photos/field-day.md          → /photos/field-day/
_photos/science-fair.md       → /photos/science-fair/
_photos/spring-concert-2026.md → /photos/spring-concert-2026/
```

### Step 3: Fill in the front-matter

At minimum you need a `title:` and at least one entry in `photos:`:

```yaml
---
title: "Science Fair 2026"
photos:
  - src: "/assets/images/photos/science-fair-1.jpg"
---
```

Add `description:` and `labels:` to enrich individual photos:

```yaml
photos:
  - src: "/assets/images/photos/science-fair-1.jpg"
    description: "Malcolm presents his volcano project"
    labels:
      - malcolm-wilkerson
  - src: "/assets/images/photos/science-fair-2.jpg"
    description: "Winners at the judging table"
    labels:
      - stevie-kenarban
      - dabney-hooper
      - julie-houlerman
```

### Step 4: Add an optional intro (body text)

Anything you write in the Markdown body (below the closing `---`) is shown
above the photo grid as a free-text intro paragraph:

```markdown
---
title: "Science Fair 2026"
photos:
  - src: "..."
---

This year's science fair had over 40 entries! Judges awarded prizes in three
categories: life sciences, earth sciences, and engineering.
```

### Step 5: Commit and push

That's it. GitHub Actions will rebuild the site and the new photo page will
appear at `/photos/<slug>/` and as a card in the **Photos** section of the
home page.

---

## Labeling people in photos

The `labels:` field on each photo accepts a list of person IDs from
`_data/people.yml`. The IDs are looked up at build time, so:

- Display names are always up-to-date (fix a typo in `people.yml` once and
  every label on every photo updates automatically).
- Each name links to that person's individual profile page.
- If an ID can't be found in `people.yml`, the label is silently skipped —
  the page still builds. The test suite catches dangling IDs at CI time.

**Order matters** — `labels:` is a list, so you can use the order to
indicate left-to-right position in the photo:

```yaml
labels:
  - reese-wilkerson    # far left
  - malcolm-wilkerson  # centre
  - dewey-wilkerson    # far right
```

---

## Thumbnail for the home page card

Every photo page appears as a card in the **Photos** section of the home
page. By default the card shows the `photo_thumbnail_default` placeholder
image. To use a real photo, add a `thumbnail:` field:

```yaml
thumbnail: "/assets/images/photos/field-day-thumb.jpg"
```

Recommended size: **800 × 300 px** landscape (same as class and club
thumbnails).

To hide the thumbnail for a specific page, set:

```yaml
thumbnail: ""
```

To change the default image used by **all** photo pages that don't set their
own `thumbnail:`, update `_config.yml`:

```yaml
photo_thumbnail_default: "/assets/images/site/my-photos-placeholder.jpg"
```

---

## Common mistakes (caught by the test suite)

| Mistake | What the test says |
|---|---|
| Missing `title:` | `Photo page is missing a title: field` |
| Photo entry without `src:` | `Photo page 'Field Day 2026': entry #2 is missing a src: value` |
| Typo in a `labels:` person ID | `Found photo labels referencing person IDs not in _data/people.yml: 'malcom-wilkerson' (in 'Field Day 2026', photo #1)` |
| Same person labeled twice in one photo | `Photo page 'Field Day 2026', photo #1 labels the same person more than once: ['malcolm-wilkerson']` |

---

## Hiding or reordering the Photos section

The **Photos** section on the home page is just another `<section>` block in
`_layouts/home.html`. To hide it, wrap it in `{% comment %}...{% endcomment %}`.
To reorder it relative to Classes, Clubs, and Sports, drag the block.

The **Photos** nav link is in `_includes/header.html`. Delete the `<a>` line
to remove it from the nav bar.

---

## Multiple photos pages

You can add as many photo pages as you like — one per event, one per month,
one per grade level's activities. Each `.md` file in `_photos/` becomes its
own page:

```
_photos/field-day.md
_photos/science-fair.md
_photos/spring-concert.md
_photos/kindergarten-activities.md
```

All of them appear as cards in the **Photos** section on the home page.
