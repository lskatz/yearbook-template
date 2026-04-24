# Elementary School Yearbook — Jekyll Template

A GitHub Pages yearbook template for elementary schools. Class pages with
students and (co-)teachers, club and sports pages, auto-generated individual
profile pages, and client-side name search. Designed so non-technical
volunteers can add a student by editing **one line of YAML** and dropping a
photo in a folder.

> 🎬 **About the demo data.** The live demo site is a fictional elementary
> school — **North Hollywood Elementary, home of the Krelboynes** — populated
> with characters from the TV show *Malcolm in the Middle* (Malcolm, Reese,
> Dewey, Stevie, Dabney, and friends). No real students or staff are included.
> The school, its mascot, its teachers, and all student data are entirely made
> up for demonstration purposes.

> ⚠️ **Privacy first.** This repo is a *template* using those fictional names
> as safe, public-domain-like example data. Before adding any real students,
> **fork this repo to a private repository**. See
> [`docs/SETUP.md`](docs/SETUP.md) for details on hosting options and the
> tradeoffs between a public site and a private one.

---

## Documentation

All of the setup and usage documentation is in [`docs/`](docs/):

- **[`docs/SETUP.md`](docs/SETUP.md)** — fork the repo, enable Pages, deploy.
  Start here.
- **[`docs/ADDING-PEOPLE.md`](docs/ADDING-PEOPLE.md)** — the everyday workflow
  for yearbook committee volunteers: how to add a student, a teacher, a club
  member. Send this link to your volunteers.
- **[`docs/PHOTO-PAGES.md`](docs/PHOTO-PAGES.md)** — how to add freeform photo
  gallery pages (field trips, events, assemblies) with optional captions and
  people labels.
- **[`docs/CUSTOMIZING.md`](docs/CUSTOMIZING.md)** — change school colors,
  fonts, labels, and layout. Most customization requires no HTML knowledge.
- **[`docs/DEVELOPING.md`](docs/DEVELOPING.md)** — local development, the
  test suite, CI workflows, and how the Ruby plugin works.

The public-facing help page at `/help/` on the built site is for **end users**
(families browsing the yearbook). The documentation in `docs/` is for
**maintainers** (the yearbook committee) and is excluded from the Jekyll
build.

---

## Quick start

```bash
# 1. Click "Use this template" on GitHub → create your repo (private)
# 2. Clone it locally
git clone https://github.com/your-org/your-yearbook.git
cd your-yearbook

# 3. Edit _config.yml (school name, year, mascot)
# 4. Run tests + preview locally
pip install -r tests/requirements.txt && pytest
bundle install && bundle exec jekyll serve
# → http://localhost:4000

# 5. Push. GitHub Actions builds and deploys.
```

Full instructions: [`docs/SETUP.md`](docs/SETUP.md).

---

## License

MIT on the template code. Photos and names you add are yours.
