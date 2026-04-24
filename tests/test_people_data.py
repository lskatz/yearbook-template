"""
Validate _data/people.yml — the master directory of everyone in the yearbook.

This is the file volunteers will edit most often, so these tests catch the
mistakes that are easiest to make: typos in role names, duplicate IDs,
missing required fields, non-kebab-case IDs that break photo lookups, etc.
"""
from __future__ import annotations

import re

VALID_ROLES = {"student", "teacher", "staff"}
KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def test_people_file_parses(people):
    """people.yml must load as a list of dicts."""
    assert isinstance(people, list), "people.yml must be a list at the top level"
    assert len(people) > 0, "people.yml is empty — add at least one person"
    for i, p in enumerate(people):
        assert isinstance(p, dict), f"Entry {i} is not a mapping: {p!r}"


def test_required_fields_present(people):
    """Every person needs id, first, and last."""
    for p in people:
        for field in ("id", "first", "last"):
            assert p.get(field), f"Missing required field '{field}' on {p!r}"


def test_ids_are_unique(people):
    ids = [p["id"] for p in people]
    duplicates = {x for x in ids if ids.count(x) > 1}
    assert not duplicates, f"Duplicate person IDs found: {sorted(duplicates)}"


def test_ids_are_kebab_case(people):
    """IDs double as photo filenames, so they must be filesystem-safe kebab-case."""
    for p in people:
        assert KEBAB_CASE.match(p["id"]), (
            f"Person ID '{p['id']}' must be kebab-case (lowercase letters, "
            f"numbers, and hyphens only). E.g. 'jane-smith', not 'Jane_Smith'."
        )


def test_role_values_are_valid(people):
    """Role must be student / teacher / staff, or omitted (defaults to student)."""
    for p in people:
        role = p.get("role", "student")
        assert role in VALID_ROLES, (
            f"{p['id']} has invalid role '{role}'. Must be one of: {sorted(VALID_ROLES)}"
        )


def test_students_have_sensible_grades(people):
    """If a person is a student and has a grade, it should be 0–8 (K–8)."""
    for p in people:
        role = p.get("role", "student")
        if role == "student" and "grade" in p:
            assert isinstance(p["grade"], int), (
                f"{p['id']}: grade must be a number, got {p['grade']!r}"
            )
            assert 0 <= p["grade"] <= 8, (
                f"{p['id']}: grade {p['grade']} is out of expected range (0–8)"
            )


def test_staff_have_titles_or_at_least_names(people):
    """Staff with a title are nicer to display, but it's not strictly required."""
    # Soft check: warn via assertion only if role=staff AND no title AND no nickname
    # (since a staff person with only first/last will still render fine)
    for p in people:
        if p.get("role") == "staff":
            # just making sure the optional title, if present, is a string
            if "title" in p:
                assert isinstance(p["title"], str) and p["title"].strip(), (
                    f"{p['id']}: title must be a non-empty string if set"
                )
