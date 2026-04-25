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

Also update `github_repo` to point to **your fork's** URL. This value
appears on the public `/help/` page so visitors who want their own yearbook
can find the template:

```yaml
github_repo: "https://github.com/your-org/your-yearbook"
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
heavily commented. The file is short — under 100 lines — and each section
(thumbnail, teachers, students, prose) is a clearly labeled block you can
reorder, remove, or duplicate.

Same pattern for `_layouts/club.html` (clubs), `_layouts/sport.html`
(sports teams), and `_layouts/person.html` (profile pages).

---

## Changing the default class thumbnail

Every class page displays a banner-style photo at the top. Each class can
have its own photo (set via `thumbnail:` in the class's front-matter), and
any class without one falls back to a site-wide default image.

To change the default for **all** classes at once, update `_config.yml`:

```yaml
# Default thumbnail shown at the top of every class page.
# Recommended size: 800 × 300 px (landscape).
class_thumbnail_default: "/assets/images/site/class-thumbnail-default.svg"
```

Point it at any image file you like (JPEG, PNG, SVG). The template ships
with a placeholder SVG at `assets/images/site/class-thumbnail-default.svg`
— replace that file, or change the path to one of your own photos.

To set a **per-class** thumbnail, add `thumbnail:` to that class's
front-matter. See [Adding a class thumbnail](ADDING-PEOPLE.md#adding-a-thumbnail-photo-to-a-class)
in ADDING-PEOPLE.md.

---

## Customizing group photos on club and sport pages

Club and sports-team pages support an optional group photo section with
auto-generated name annotations. The photo appears below the member roster.

The relevant front-matter fields (add to any `_clubs/*.md` or `_sports/*.md`):

```yaml
group_photo: "/assets/images/groups/chess-club.jpg"
photo_caption: "Chess Club, left to right:"
photo_annotation:
  - malcolm-wilkerson
  - stevie-kenarban
  - dabney-hooper
```

The template ships with placeholder SVG group photos in
`assets/images/groups/` — one per built-in club and sport. To replace one,
simply upload a real photo at the same path:

```
assets/images/groups/chess-club.jpg     ← replace the .svg with a real JPEG
assets/images/groups/soccer.jpg
# etc.
```

If you change the file extension, also update `group_photo:` in the
matching `.md` file to point to the new path.

To remove the group photo section from a page entirely, delete the
`group_photo:`, `photo_caption:`, and `photo_annotation:` lines from its
front-matter.

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

---

## Custom theme graphics

The yearbook template ships with a set of SVG graphics that give the site a
classic yearbook feel. Every piece is designed to be replaced or tweaked with
minimal effort.

---

### Hero cover art

The home page hero is decorated by an **inline SVG layer** embedded in
`_layouts/home.html`, immediately before the text `<div class="wrap ...">`.

The SVG creates:
- A subtle diagonal cross-hatch background texture
- Thin accent-colour stripes at the very top and bottom of the hero
- A pair of ruled border lines (double-rule, top and bottom)
- Decorative L-shaped corner bracket ornaments
- Diamond ornaments at the inner corner of each bracket
- Evenly-spaced accent dots along the top and bottom rules
- A central horizontal divider line with a diamond centrepiece
- 4-pointed star ornaments at the exact centre of the top/bottom rules

**Colours are inherited automatically.** All elements inside the SVG use
`style="... var(--color-accent) ..."` and similar CSS custom properties, so
changing `--color-accent` in `_config.yml` / `main.css` updates the hero art
with no extra steps.

**To tweak the art intensity** — find any SVG group or element and adjust its
`opacity` attribute:

```xml
<!-- make corner brackets bolder -->
<g style="stroke:var(--color-accent);…;opacity:0.7">
```

**To remove the hero art entirely** — delete the whole `<svg class="hero__art"…>`
block from `_layouts/home.html`.

---

### Favicon / site icon

The browser-tab icon lives at `assets/images/site/favicon.svg`. It's a
heraldic shield design containing a school initial.

To customise it:
1. Open `assets/images/site/favicon.svg`
2. Change the `fill` on the first `<path>` (shield body) to your school colour
3. Change the character inside `<text>` to your school's initial letter

```xml
<!-- change shield colour -->
<path d="M16 2 …" fill="#1f3a5f"/>   <!-- navy instead of burgundy -->

<!-- change initial -->
<text …>W</text>                      <!-- "W" for your school name -->
```

---

### Default thumbnail graphics

All placeholder images are SVG files in `assets/images/site/`. Each has:
- A coloured accent band at the top and bottom (branded to the content type)
- A content-type illustration (class rows, club circle, team rows, camera lens)
- L-shaped corner accent marks framing the content area
- A label in the top band and a hint in the bottom band

| Content type | SVG file | `_config.yml` key |
|---|---|---|
| Class pages | `class-thumbnail-default.svg` | `class_thumbnail_default` |
| Club pages  | `club-thumbnail-default.svg`  | `club_thumbnail_default`  |
| Sport pages | `sport-thumbnail-default.svg` | `sport_thumbnail_default` |
| Photo pages | `photo-thumbnail-default.svg` | `photo_thumbnail_default` |

To swap the placeholder for a real photo across all pages of one type:

```yaml
# _config.yml
class_thumbnail_default: "/assets/images/my-school-banner.jpg"
```

To override the image for just one page, add `thumbnail:` to that page's
front-matter (see [Changing the default class thumbnail](#changing-the-default-class-thumbnail)).

To customise the placeholder SVG colours, open the file and edit the `fill`
values on the top/bottom `<rect>` elements (the accent bands) and the `stroke`
values on the corner marks.

---

### Corner tick marks on index cards

Home-page index cards display subtle **L-shaped corner tick marks** on hover,
evoking classic photo-album corner tabs. They are purely CSS and cost nothing
in terms of HTML or JavaScript.

```css
/* assets/css/main.css — "Corner tick marks on index cards" section */
.index-list a::before { … }   /* top-left bracket */
.index-list a::after  { … }   /* bottom-right bracket */
```

- **Show at all times** (not just hover): remove `opacity: 0` from the default
  rule and delete the `.index-list a:hover::before / ::after` block.
- **Remove entirely**: delete the two `.index-list a::before / ::after` blocks.
- **Change colour**: the marks inherit `border-color: var(--color-accent)`, so
  changing your accent colour automatically updates them.
- **Change size**: edit the `width` / `height` values (default: 9px × 9px).

---

### Ornamental section dividers

Home-page sections (Classes, Clubs, Sports …) are separated by a centred ✦
ornament sitting on a hairline rule, instead of a plain dashed border.

This is a CSS `::after` pseudo-element on `.index-section`:

```css
/* assets/css/main.css */
.index-section:not(:last-child)::after {
  content: '✦';
  …
}
```

- **Change the ornament**: replace `'✦'` with any character (`◆`, `·`, `❖`, `★`)
- **Increase line width**: change `background-size: 75% 1px` to `90% 1px`
- **Revert to a simple dashed line**: remove the `::after` rule and add
  `border-bottom: 1px dashed var(--color-border-soft);` back to `.index-section`

---

### Autograph page decorative frame

Each autograph page has a **double-border frame** with accent-colour corner
marks — perfect for print.

- Outer border: `1.5px solid var(--color-border)`
- Inner second border: `inset box-shadow` using `--color-border-soft`
- Corner marks: `::before` (top-left) and `::after` (bottom-right)

To remove the frame, find the `.autograph-page` rule block in `main.css` and
delete the `border`, `box-shadow`, and `::before / ::after` declarations.

---

### Background texture

The page background combines two effects — both are CSS `background-image`
layers on the `body` rule in `main.css`:

| Layer | What it does |
|---|---|
| Two offset dot patterns | Fine grain (simulates paper texture) |
| Horizontal + vertical linear gradients | Subtle large-scale grid overlay |

To **increase the texture** intensity, raise the `rgba(…)` opacity values
(e.g. `0.06` → `0.10`). To **disable** the texture, remove the
`background-image` declaration from `body` entirely.

