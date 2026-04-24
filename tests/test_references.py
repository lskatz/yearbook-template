"""
Validate cross-references between classes/clubs/sports and the people directory.

The single most common mistake volunteers will make is listing a person in a
class roster with a typo'd ID. Jekyll builds fine, but the person-card
silently renders as "Unknown: malcom-wilkerson". These tests catch that at
CI time so the typo never reaches the site.
"""
from __future__ import annotations

import pytest


def _collect_refs(docs: list[dict], fields: list[str]) -> list[tuple[str, str, str]]:
    """Return (source_title, field_name, person_id) for every reference."""
    refs = []
    for doc in docs:
        title = doc.get("title", "<untitled>")
        for field in fields:
            for pid in doc.get(field, []) or []:
                refs.append((title, field, pid))
    return refs


def test_class_references_resolve(classes, people_by_id):
    refs = _collect_refs(classes, ["teachers", "students"])
    assert refs, "No class references found — did you forget to add any classes?"
    broken = [(t, f, pid) for (t, f, pid) in refs if pid not in people_by_id]
    assert not broken, _format_broken(broken)


def test_club_references_resolve(clubs, people_by_id):
    refs = _collect_refs(clubs, ["advisors", "members"])
    broken = [(t, f, pid) for (t, f, pid) in refs if pid not in people_by_id]
    assert not broken, _format_broken(broken)


def test_sport_references_resolve(sports, people_by_id):
    refs = _collect_refs(sports, ["coaches", "members"])
    broken = [(t, f, pid) for (t, f, pid) in refs if pid not in people_by_id]
    assert not broken, _format_broken(broken)


def test_teachers_field_contains_teachers_or_staff(classes, people_by_id):
    """A class's `teachers:` list should only contain people with role teacher/staff."""
    for doc in classes:
        for pid in doc.get("teachers", []) or []:
            p = people_by_id.get(pid)
            if p is None:
                continue  # covered by resolution test above
            role = p.get("role", "student")
            assert role in ("teacher", "staff"), (
                f"Class '{doc.get('title')}' lists '{pid}' as a teacher, "
                f"but that person's role is '{role}'. Fix role in people.yml "
                f"or move them to students."
            )


def test_students_field_contains_students(classes, people_by_id):
    """Catches the inverse — a teacher accidentally placed in the student list."""
    for doc in classes:
        for pid in doc.get("students", []) or []:
            p = people_by_id.get(pid)
            if p is None:
                continue
            role = p.get("role", "student")
            assert role == "student", (
                f"Class '{doc.get('title')}' lists '{pid}' as a student, "
                f"but that person's role is '{role}'."
            )


def test_no_duplicate_student_in_same_class(classes):
    """Catch copy-paste errors where the same kid is listed twice in one class."""
    for doc in classes:
        students = doc.get("students", []) or []
        dupes = {x for x in students if students.count(x) > 1}
        assert not dupes, (
            f"Class '{doc.get('title')}' lists these students more than once: {sorted(dupes)}"
        )


def _format_broken(broken: list[tuple[str, str, str]]) -> str:
    lines = ["Found references to person IDs that don't exist in _data/people.yml:"]
    for source, field, pid in broken:
        lines.append(f"  • '{pid}'  (in {source} → {field})")
    lines.append("\nEither fix the typo or add the person to _data/people.yml.")
    return "\n".join(lines)
