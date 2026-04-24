"""
Tests for the _photos/ collection (photo pages feature).

Photo pages live in `_photos/*.md`. Each page can list any number of photos
under a `photos:` key. Every photo entry supports:
  - src         (required) — path to the image file
  - description (optional) — free-text caption
  - labels      (optional) — list of person IDs who appear in the photo

These tests verify:
  1. Every photo page has a `title:` field.
  2. Every `src:` value is a non-empty string.
  3. Every person ID listed under `labels:` resolves to a real person in
     `_data/people.yml` (catches typos before they reach the live site).
  4. No person is labeled more than once in the same photo.
"""
from __future__ import annotations

import pytest


def test_photo_pages_have_titles(photo_pages):
    """Every photo page must have a title (it's the only required field)."""
    for page in photo_pages:
        assert page.get("title"), (
            f"Photo page is missing a `title:` field: {page}"
        )


def test_photo_entries_have_src(photo_pages):
    """Every photo entry in a photo page must supply a `src:` path."""
    for page in photo_pages:
        title = page.get("title", "<untitled>")
        for i, photo in enumerate(page.get("photos") or []):
            assert photo.get("src"), (
                f"Photo page '{title}': entry #{i + 1} is missing a `src:` value"
            )


def test_photo_labels_resolve(photo_pages, people_by_id):
    """
    Every person ID listed under a photo's `labels:` key must exist in
    `_data/people.yml`. Catches typos before they reach the live site.
    """
    broken = []
    for page in photo_pages:
        title = page.get("title", "<untitled>")
        for i, photo in enumerate(page.get("photos") or []):
            for pid in photo.get("labels") or []:
                if pid not in people_by_id:
                    broken.append((title, i + 1, pid))

    assert not broken, _format_broken_labels(broken)


def test_no_duplicate_labels_in_same_photo(photo_pages):
    """A person should not be labeled more than once in the same photo."""
    for page in photo_pages:
        title = page.get("title", "<untitled>")
        for i, photo in enumerate(page.get("photos") or []):
            labels = photo.get("labels") or []
            dupes = {x for x in labels if labels.count(x) > 1}
            assert not dupes, (
                f"Photo page '{title}', photo #{i + 1} labels the same "
                f"person more than once: {sorted(dupes)}"
            )


def _format_broken_labels(broken: list[tuple[str, int, str]]) -> str:
    lines = ["Found photo labels referencing person IDs not in _data/people.yml:"]
    for page_title, photo_num, pid in broken:
        lines.append(f"  • '{pid}'  (in '{page_title}', photo #{photo_num})")
    lines.append("\nEither fix the typo or add the person to _data/people.yml.")
    return "\n".join(lines)
