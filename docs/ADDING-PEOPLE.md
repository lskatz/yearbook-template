# Adding people and pages

This is the guide for yearbook committee volunteers. It covers the everyday
workflow: adding students, teachers, classes, clubs, and sports teams.

You don't need any programming experience — the whole system is designed so
that adding a student is two small edits and one photo upload.

---

## The mental model

Every person in the yearbook — every student, every teacher, every staff
member — lives in **one place**: `_data/people.yml`. That's the master list.

Class pages, club pages, and sports pages don't re-list people. They just
**reference** them by a short ID. So if a student is in two clubs and one
sports team, you add them to `people.yml` **once**, and reference their ID
four times (their class + two clubs + one team).

This means:

- Fixing a typo in a student's name is one edit.
- Replacing a student's photo is one file upload.
- A student's profile page at `/people/<id>/` automatically lists every
  class/club/team they're in.

---

## Adding a student

### Step 1: Save their photo

Crop and save the photo as a JPEG in `assets/images/people/`, named after
the student's ID. The ID is just their name in lowercase with hyphens:

```
assets/images/people/jane-smith.jpg
assets/images/people/malcolm-wilkerson.jpg
```

Don't worry about the photo being too large — the site's image-optimization
workflow automatically resizes oversized photos to 1200px wide and strips
out GPS/camera metadata the next time you push.

### Step 2: Add them to `_data/people.yml`

Open `_data/people.yml` and add an entry under the "STUDENTS" section:

```yaml
- id: jane-smith       # must match the photo filename
  first: Jane
  last: Smith
  grade: 3
```

**Grade values:**

| Value | Meaning |
|-------|---------|
| `PK`  | Pre-Kindergarten |
| `K`   | Kindergarten |
| `1` – `5` | 1st through 5th grade (use bare numbers, no quotes) |

Note that `PK` and `K` are written as quoted strings, while numeric grades
are plain integers:

```yaml
grade: PK   # Pre-K
grade: K    # Kindergarten
grade: 3    # 3rd grade
```

Optional fields you can add:

```yaml
- id: jane-smith
  first: Jane
  last: Smith
  grade: 3
  nickname: "Janie"           # displayed instead of first name everywhere
  pronouns: "she/her"         # shown on profile page
  quote: "I love art class!"  # shown on profile page (nice for 5th graders)
```

### Step 3: Add their ID to their class

Open the appropriate class file in `_classes/` (e.g. `3rd-grade-smith.md`)
and add the student's ID to the `students:` list:

```yaml
---
title: "3rd Grade — Mrs. Garcia"
grade: 3
teachers:
  - mrs-garcia
students:
  - alice-johnson
  - jane-smith          # ← added
  - kevin-ross
---
```

That's it. Commit and push. The tests will run, then the site will rebuild.

---

## Adding a teacher

Same three steps, except the `role:` is `teacher` and there's no `grade`:

```yaml
# in _data/people.yml, under "TEACHERS"
- id: mrs-garcia
  first: Maria
  last: Garcia
  role: teacher
  nickname: "Mrs. Garcia"     # so "Mrs. Garcia" appears, not "Maria Garcia"
```

Then reference them in a class file under `teachers:`:

```yaml
teachers:
  - mrs-garcia
```

**Co-teachers?** Just list both:

```yaml
teachers:
  - mrs-garcia
  - mr-patel
```

---

## Adding staff (principal, nurse, counselors, etc.)

Staff go on the Staff page automatically — you don't need to add them to any
roster manually.

```yaml
# in _data/people.yml, under "STAFF"
- id: principal-block
  first: Alan
  last: Block
  role: staff
  title: "Principal"
```

The `title:` field is what appears on their card (e.g. "Principal",
"School Nurse", "Librarian").

---

## Creating a new class

To add a class that doesn't exist yet, create a new file in `_classes/`.
Name it however you like — `4th-grade-rodriguez.md`, `prek-rivera.md`,
`k-lopez.md` — the filename becomes the URL slug.

```markdown
---
title: "4th Grade — Ms. Rodriguez"
grade: 4
room: "Room 12"
teachers:
  - ms-rodriguez
students:
  - alice-johnson
  - bob-lee
  - jane-smith
---

Optional write-up about the class year goes here. You can use
**bold**, *italics*, and [links](https://example.com).
```

**Required fields:** `title`, `grade`.  
**Optional:** `room`, `teachers`, `students`, `thumbnail`, and free-form Markdown body.

Pre-K and Kindergarten classes use the string grade values:

```yaml
grade: PK    # Pre-Kindergarten
grade: K     # Kindergarten
grade: 1     # 1st grade, and so on
```

### Adding a thumbnail photo to a class

Each class page displays a banner-style photo between the title and the
roster. By default every class shows a shared placeholder image. To use a
real class photo, add a `thumbnail:` field to the class's front-matter:

```yaml
---
title: "4th Grade — Ms. Rodriguez"
grade: 4
thumbnail: "/assets/images/classes/4th-grade-rodriguez.jpg"
teachers:
  - ms-rodriguez
students:
  - alice-johnson
  - jane-smith
---
```

Save the photo at the path you listed (`assets/images/classes/` is a good
home for class photos). Recommended size: **800 × 300 px** landscape.

To hide the thumbnail for a specific class altogether, set:

```yaml
thumbnail: ""
```

To change the default placeholder used by every class that doesn't set
`thumbnail:`, see *[Changing the default class thumbnail](CUSTOMIZING.md#changing-the-default-class-thumbnail)*
in CUSTOMIZING.md.

---

## Creating a new club

Add a file in `_clubs/`:

```markdown
---
title: "Robotics Club"
meets: "Tuesdays after school"
advisors:
  - mr-herkabe
members:
  - malcolm-wilkerson
  - stevie-kenarban
  - dabney-hooper
---

Optional description of the club and what they did this year.
```

**Optional fields:** `meets`, `advisors`, `members`, `group_photo`,
`photo_caption`, `photo_annotation`.

### Adding a group photo to a club

You can display an annotated group photo on any club page:

```markdown
---
title: "Chess Club"
meets: "Wednesdays after school"
advisors:
  - mr-herkabe
members:
  - malcolm-wilkerson
  - stevie-kenarban
  - dabney-hooper
group_photo: "/assets/images/groups/chess-club.jpg"
photo_caption: "Chess Club, left to right:"
photo_annotation:
  - malcolm-wilkerson
  - stevie-kenarban
  - dabney-hooper
---
```

| Field | Purpose |
|---|---|
| `group_photo` | Path to the group photo image. Save the file there first. |
| `photo_caption` | Short label shown before the list of names (optional). |
| `photo_annotation` | Ordered list of person IDs matching left-to-right order in the photo. Names are looked up automatically from `people.yml`. |

The template ships with placeholder SVG images in `assets/images/groups/`
for each built-in club and sport. Replace any of these files with a real
photo at the same path, or point `group_photo:` at a new path.

To remove the group photo section from a club page, simply delete the
`group_photo:`, `photo_caption:`, and `photo_annotation:` lines from its
front-matter.

---

## Creating a new sports team

Add a file in `_sports/`:

```markdown
---
title: "Basketball"
season: "Winter"
record: "6–4"
coaches:
  - mr-woodward
members:
  - reese-wilkerson
  - francis-wilkerson
  - kevin
---

Optional recap of the season.
```

**Optional fields:** `season`, `record`, `coaches`, `members`, `group_photo`,
`photo_caption`, `photo_annotation`.

### Adding a group photo to a sports team

Group photos work exactly the same way for sports teams as for clubs:

```markdown
---
title: "Soccer"
season: "Fall"
record: "8–2"
coaches:
  - mr-woodward
members:
  - reese-wilkerson
  - julie-houlerman
group_photo: "/assets/images/groups/soccer.jpg"
photo_caption: "Soccer team, left to right:"
photo_annotation:
  - reese-wilkerson
  - julie-houlerman
---
```

See [Adding a group photo to a club](#adding-a-group-photo-to-a-club) above
for a full description of each field.

---

## Adding a photo page (events, field trips, etc.)

Photo pages are freeform gallery pages you can use for any occasion that
doesn't fit into a class, club, or sports roster — field day, science fair,
spring concert, etc. Each page holds any number of photos, and each photo
can have an optional description and a list of people labels.

Create a `.md` file in `_photos/`:

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
    # No description or labels — both are optional.
---

Field Day was a huge success this year!
```

The filename becomes the URL slug (`field-day.md` → `/photos/field-day/`).
The page automatically appears as a card in the **Photos** section of the
home page.

For the full reference — all front-matter fields, labeling tips, thumbnail
configuration, and the full error table — see
**[`docs/PHOTO-PAGES.md`](PHOTO-PAGES.md)**.

---

## Common mistakes (and how you'll find out)

The test suite (runs automatically on every push) catches the usual
slip-ups and tells you exactly what's wrong:

| Mistake | What the test says |
|---|---|
| Typo in a person ID (`malcom` instead of `malcolm`) | `Found references to person IDs that don't exist in _data/people.yml: 'malcom-wilkerson' (in Chess Club → members)` |
| Same person listed twice in one class | `Class '3rd Grade — Ms. Garcia' lists these students more than once: ['jane-smith']` |
| Duplicate ID in people.yml | `Duplicate person IDs found: ['jane-smith']` |
| A teacher accidentally in a student list | `Class '...' lists 'mrs-garcia' as a student, but that person's role is 'teacher'` |
| An ID with capital letters or spaces | `Person ID 'Jane Smith' must be kebab-case` |
| Invalid grade value | `grade must be a number or one of ['K', 'PK'], got 'Kindergarten'` |

If the tests fail, check the **Actions** tab on GitHub — the failure message
points at the exact file and bad value.

---

## Photos: a few notes

- **Format**: JPEG is best. PNG and WebP also work and will be converted.
- **Size**: anything up to ~10 MB is fine. Oversized photos are auto-resized
  to 1200px wide on push. Smaller photos are left alone.
- **EXIF metadata**: automatically stripped on upload. This removes GPS
  coordinates and camera info that modern phones embed in every photo —
  important for privacy.
- **Portrait photos**: portrait (3:4) ratio looks best for individual
  student/teacher cards. Photos are cropped to fill their card, so a tight
  head-and-shoulders crop works better than a full body shot.
- **Class thumbnails**: landscape (8:3) ratio works best, around 800 × 300 px.
- **Group photos**: landscape is recommended; width × height ratio is
  flexible. Photos are displayed at full column width.
- **Missing photos**: if a student is added before their photo is ready,
  their card will show their initials instead of a broken image. So you can
  add everyone to the roster first and fill in photos later.

---

## Editing without knowing Git

Two options for committee members who don't want to clone the repo:

1. **GitHub web editor.** Open any file on github.com and click the pencil
   icon. Commit directly to `main` (or to a branch for review).
2. **Decap CMS** (optional). A form-based editor at `https://<site>/admin/`.
   Setup requires ~10 minutes of one-time configuration — see the comments
   at the top of `admin/config.yml`.
