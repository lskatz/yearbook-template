# Customizing the yearbook

Most customization happens in two files:

- **`_config.yml`** — site name, school year, mascot, all the labels on the site
- **`assets/css/main.css`** — colors, fonts, spacing, visual design

Neither file requires HTML knowledge.

---

## Changing the school name, year, and mascot

Top of `_config.yml`:

```yaml
title: "Your Elementary School Yearbook"
description: "2025–2026 school year"
school_year: "2025–2026"
mascot: "The Rockets"
```

---

## Changing colors

Open `assets/css/main.css` and find the `:root` block near the top. The
important variable is:

```css
--color-accent: #7b2d1e;   /* school color — change me! */
```

Some common swaps:

| School color | Hex |
|---|---|
| Burgundy (default) | `#7b2d1e` |
| Forest green | `#2f5236` |
| Navy blue | `#1f3a5f` |
| Royal blue | `#2849a8` |
| Goldenrod | `#b07d1d` |
| Crimson | `#a12830` |
| Teal | `#2a6a6a` |

The full palette is cream paper + dark ink + your accent. If your school
colors don't work well on cream, also change:

```css
--color-bg:      #f4efe5;  →  #ffffff   (pure white background)
--color-surface: #fbf7ed;  →  #fafafa   (off-white cards)
```

---

## Changing fonts

Fonts come from [Google Fonts](https://fonts.google.com/) and are loaded in
two places. You need to update **both**:

1. **`_includes/head.html`** — the `<link>` tag that loads the fonts
2. **`assets/css/main.css`** — the `--font-display` and `--font-body` variables

A few classic combinations to try:

| Display | Body |
|---|---|
| Fraunces *(default)* | Instrument Sans |
| Playfair Display | Source Serif 4 |
| EB Garamond | Lora |
| DM Serif Display | IBM Plex Sans |
| Libre Caslon Text | Libre Franklin |

---

## Changing labels and terminology

If your school says "Pupils" instead of "Students", or "Section" instead of
"Class", edit the `labels:` block in `_config.yml`:

```yaml
labels:
  teachers_one:  "Teacher"
  teachers_many: "Teachers"
  students:      "Students"     # ← change to "Pupils"
  # ...
```

Every page updates automatically. This is also how you'd translate the site
to another language — all user-facing text is in this one block.

---

## Hiding or reordering navigation links

Open `_includes/header.html`. The nav links are near the bottom — each is
a single `<a>` tag:

```html
<nav class="site-nav" aria-label="Primary">
  <a href="{{ '/' | relative_url }}#classes">{{ site.labels.nav_classes }}</a>
  <a href="{{ '/' | relative_url }}#clubs">{{ site.labels.nav_clubs }}</a>
  <a href="{{ '/' | relative_url }}#sports">{{ site.labels.nav_sports }}</a>
  <a href="{{ '/staff/' | relative_url }}">{{ site.labels.nav_staff }}</a>
  <a href="{{ '/help/' | relative_url }}">{{ site.labels.nav_help }}</a>
</nav>
```

- **Remove a link**: delete its entire `<a>` line
- **Reorder**: drag the lines into a new order
- **Add a new link**: copy a line and change the `href` and label

---

## Hiding or reordering sections on the home page

Open `_layouts/home.html`. There are three big `<section>` blocks — Classes,
Clubs, Sports. Each is clearly commented. Drag them into a new order, or
wrap any one of them in `{% comment %}...{% endcomment %}` to hide it.

---

## Adding a new field to people

Say you want to add a "favorite subject" field to student profiles.

### 1. Add the field in `_data/people.yml`

```yaml
- id: jane-smith
  first: Jane
  last: Smith
  grade: 3
  favorite_subject: "Art"      # ← new field
```

### 2. Show it in `_layouts/person.html`

Find a sensible spot in the person hero block and add:

```liquid
{%- if p.favorite_subject %}
  <p class="person-hero__detail">Favorite subject: {{ p.favorite_subject }}</p>
{%- endif %}
```

That's it. The `{% if %}` check means students without the field just skip
the line — so you can roll out new fields gradually.

---

## Adding a new page type (e.g. "Events" or "Field Trips")

This is a bigger change but still straightforward:

1. Create a new folder `_events/` with one `.md` file per event.
2. Add the collection to `_config.yml`:
   ```yaml
   collections:
     events:
       output: true
       permalink: /events/:slug/
   ```
3. Create `_layouts/event.html` (copy `_layouts/club.html` as a starting point).
4. Add a default layout mapping in `_config.yml`:
   ```yaml
   defaults:
     - scope: { path: "", type: "events" }
       values: { layout: "event" }
   ```
5. Add an "Events" section to `_layouts/home.html` (copy one of the existing
   `<section>` blocks).
6. Add a nav link in `_includes/header.html`.

---

## Changing what's on a class page

The whole layout for class pages lives in `_layouts/class.html`, and it's
heavily commented. The file is short — under 70 lines — and each section
(teachers, students, prose) is a clearly labeled block you can reorder,
remove, or duplicate.

Same pattern for `_layouts/club.html` (clubs), `_layouts/sport.html`
(sports teams), and `_layouts/person.html` (profile pages).

---

## Making the design more playful / more formal

The defaults lean "classic editorial" — serif headlines, cream paper, thin
photo borders. To shift the feel:

**More playful**: change `--color-bg` to a pastel, bump `--radius-photo`
from 2px to 12px for rounded corners, swap `--font-display` to something
friendly like "Cooper" or "Fredoka".

**More formal**: reduce `--photo-border` from 6px to 0, change `--font-display`
to "Libre Caslon Text" or "Cormorant Garamond", reduce `--color-accent`
saturation.

**More modern**: swap both fonts to sans-serif ("Inter" + "Space Grotesk"),
set `--radius-photo: 8px`, `--photo-border: 0`, and remove the paper-grain
background effect in the `body` selector.

All of this is reachable from `:root` + a couple lines in the `body` rule.
