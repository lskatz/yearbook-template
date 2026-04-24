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
Name it however you like — `4th-grade-rodriguez.md`, `4a.md`, whatever —
the filename becomes the URL slug.

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
**Optional:** `room`, `teachers`, `students`, and free-form Markdown body.

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
- **Aspect ratio**: portrait (3:4) looks best. Photos are cropped to fill
  their card, so a tight head-and-shoulders crop works better than a full
  body shot.
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
