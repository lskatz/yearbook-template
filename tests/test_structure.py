"""
Validate site structure and configuration.

These are the "did you break something structural?" tests — checks that
Jekyll's expected files exist, _config.yml parses, and the generated
people.json Liquid template is syntactically plausible. They're quick and
cheap and catch a surprising number of "I renamed a folder and forgot to
update X" bugs.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml
from tests.conftest import load_yaml, load_front_matter

REQUIRED_PATHS = [
    "_config.yml",
    "_data/people.yml",
    "_layouts/default.html",
    "_layouts/home.html",
    "_layouts/class.html",
    "_layouts/club.html",
    "_layouts/sport.html",
    "_layouts/person.html",
    "_layouts/staff.html",
    "_includes/head.html",
    "_includes/header.html",
    "_includes/footer.html",
    "_includes/person-card.html",
    "_plugins/people_generator.rb",
    "assets/css/main.css",
    "assets/js/search.js",
    "assets/images/site/placeholder.svg",
    "people.json",
    "index.md",
    "staff.md",
    "help.md",
    "Gemfile",
    "README.md",
    "docs/SETUP.md",
    "docs/ADDING-PEOPLE.md",
    "docs/CUSTOMIZING.md",
    "docs/DEVELOPING.md",
]


def test_required_files_exist(root):
    missing = [p for p in REQUIRED_PATHS if not (root / p).exists()]
    assert not missing, f"Required files are missing: {missing}"


def test_config_declares_expected_collections(root):
    cfg = load_yaml(root / "_config.yml")
    collections = cfg.get("collections", {})
    for expected in ("classes", "clubs", "sports", "people"):
        assert expected in collections, f"_config.yml missing collection: {expected}"
        assert collections[expected].get("output") is True, (
            f"Collection '{expected}' must have `output: true` to render pages"
        )


def test_config_has_labels_block(root):
    """Labels must exist and cover every user-facing string the layouts reference."""
    cfg = load_yaml(root / "_config.yml")
    labels = cfg.get("labels")
    assert isinstance(labels, dict), "_config.yml must define a `labels:` block"
    required = {
        "nav_classes", "nav_clubs", "nav_sports", "nav_staff", "nav_help",
        "eyebrow_class", "eyebrow_club", "eyebrow_sport", "eyebrow_staff",
        "teachers_one", "teachers_many", "students",
        "advisors_one", "advisors_many", "members",
        "coaches_one", "coaches_many", "roster",
        "appears_in",
        "section_classes", "section_clubs", "section_sports",
        "search_placeholder",
    }
    missing = required - set(labels.keys())
    assert not missing, f"labels block is missing keys: {sorted(missing)}"
    # All values should be non-empty strings
    for k, v in labels.items():
        assert isinstance(v, str) and v.strip(), f"labels.{k} must be a non-empty string"


def test_config_excludes_maintainer_files(root):
    """docs/, tests/, and README.md must be excluded from the built site."""
    cfg = load_yaml(root / "_config.yml")
    exclude = set(cfg.get("exclude", []))
    for must_exclude in ("docs", "tests", "README.md"):
        assert must_exclude in exclude, (
            f"_config.yml must exclude '{must_exclude}' from the built site "
            f"(it contains maintainer-only content)"
        )


def test_help_page_has_expected_front_matter(root):
    """The on-site /help/ page is for end users — must exist with a permalink."""
    fm = load_front_matter(root / "help.md")
    assert fm.get("permalink") == "/help/", "help.md must have permalink: /help/"
    assert fm.get("title"), "help.md must have a title"


def test_admin_config_is_valid_yaml(root):
    """Decap CMS config must be valid YAML even if editors don't use the admin UI."""
    path = root / "admin" / "config.yml"
    assert path.exists()
    data = load_yaml(path)
    assert "collections" in data
    assert "backend" in data


def test_people_json_template_has_front_matter(root):
    """people.json is a Liquid template — must start with YAML front-matter."""
    text = (root / "people.json").read_text(encoding="utf-8")
    assert text.startswith("---"), "people.json must start with Jekyll front-matter"
    assert "permalink: /people.json" in text


def test_people_json_simulation_produces_valid_json(people):
    """
    Simulate what Jekyll's Liquid engine will emit for people.json, using our
    actual _data/people.yml as input. Verifies the output is valid JSON and
    every record has the fields the search JS expects.
    """
    out = []
    for p in people:
        display = p.get("nickname") or p["first"]
        role = p.get("role", "student")
        if role == "student" and "grade" in p:
            meta = f"Grade {p['grade']}"
        elif p.get("title"):
            meta = p["title"]
        elif role == "teacher":
            meta = "Teacher"
        elif role == "staff":
            meta = "Staff"
        else:
            meta = ""
        out.append({
            "name": f"{display} {p['last']}",
            "search": f"{display} {p['last']} {p['first']}".lower(),
            "meta": meta,
            "url": f"/people/{p['id']}/",
        })

    # Must round-trip through JSON cleanly
    serialized = json.dumps(out)
    parsed = json.loads(serialized)
    assert len(parsed) == len(people)
    for record in parsed:
        assert set(record.keys()) == {"name", "search", "meta", "url"}
        assert record["name"].strip()
        assert record["search"].strip()
        assert record["url"].startswith("/people/") and record["url"].endswith("/")


def test_css_braces_balanced(root):
    """Cheap syntax check — unbalanced braces in CSS usually mean a bad paste."""
    css = (root / "assets" / "css" / "main.css").read_text(encoding="utf-8")
    # Strip comments before counting
    css_no_comments = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    assert css_no_comments.count("{") == css_no_comments.count("}"), (
        "Unbalanced braces in main.css — probably a missing } somewhere"
    )


def test_liquid_tags_balanced_in_layouts(root):
    """
    Count {% ... %} block tags across layouts and includes and make sure each
    opener has a matching closer of the same kind. Catches {% if %}...{% endfor %}
    mismatches as well as plain unclosed blocks.
    """
    openers = {"if", "unless", "for", "capture", "case", "comment"}
    for path in list((root / "_layouts").glob("*.html")) + list((root / "_includes").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        stack = []
        for tag in re.findall(r"\{%-?\s*(\w+)", text):
            if tag in openers:
                stack.append(tag)
            elif tag.startswith("end"):
                expected = tag[3:]
                assert stack, f"{path.name}: {{% {tag} %}} with no matching opener"
                opener = stack.pop()
                assert opener == expected, (
                    f"{path.name}: {{% {tag} %}} doesn't match opener {{% {opener} %}}"
                )
        assert not stack, f"{path.name}: unclosed Liquid blocks: {stack}"
