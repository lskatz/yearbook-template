"""
Validate that every person listed in _data/people.yml has a corresponding
photo file on disk, and that the photo is a valid image.

These tests answer two questions the site depends on:
  • Are photos being linked properly? (the ID → filename convention is consistent)
  • Are photos being rendered properly? (the file is a real image, not a stub)

Without these checks a volunteer could add a person to people.yml, push, and
only discover the missing photo after the yearbook goes live. The test catches
the gap in CI before anyone sees a broken card.
"""
from __future__ import annotations

import struct
from pathlib import Path

import pytest
import yaml

from tests.conftest import load_yaml


# Recognised image extensions (lower-case).
_VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".svg", ".webp"}

# JPEG magic bytes (SOI marker).
_JPEG_MAGIC = bytes([0xFF, 0xD8])
# PNG magic bytes.
_PNG_MAGIC  = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
# WebP magic: "RIFF" at offset 0, "WEBP" at offset 8.
_WEBP_RIFF  = b"RIFF"
_WEBP_MARK  = b"WEBP"


def _is_valid_image(path: Path) -> bool:
    """Return True if the file has a recognised image header."""
    with path.open("rb") as fh:
        header = fh.read(12)
    ext = path.suffix.lower()
    if ext in (".jpg", ".jpeg"):
        return header[:2] == _JPEG_MAGIC
    if ext == ".png":
        return header[:8] == _PNG_MAGIC
    if ext == ".webp":
        return header[:4] == _WEBP_RIFF and header[8:12] == _WEBP_MARK
    if ext == ".svg":
        # SVG files are XML; check for a valid XML/SVG start marker.
        return header[:1] == b"<" or header[:5] == b"<?xml"
    return False


def _expected_photo_path(root: Path, person: dict, photo_path_default: str) -> Path:
    """
    Return the Path where this person's photo *should* live.

    If the person has an explicit ``photo:`` override, that path is used.
    Otherwise the site-wide default pattern (photo_path_default from
    _config.yml) is applied with {id} substituted.
    """
    raw = person.get("photo") or photo_path_default.replace("{id}", person["id"])
    # Strip leading slash so Path.joinpath works correctly.
    return root / raw.lstrip("/")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def config(root) -> dict:
    return load_yaml(root / "_config.yml")


@pytest.fixture(scope="session")
def photo_path_default(config) -> str:
    return config.get("photo_path_default", "/assets/images/people/{id}.jpg")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_photo_path_default_uses_supported_extension(photo_path_default):
    """photo_path_default must end with a supported image extension."""
    suffix = Path(photo_path_default).suffix.lower()
    assert suffix in _VALID_EXTENSIONS, (
        f"photo_path_default ('{photo_path_default}') uses extension '{suffix}', "
        f"which is not in the supported set {sorted(_VALID_EXTENSIONS)}. "
        f"Update photo_path_default in _config.yml."
    )


def test_photo_path_default_contains_id_placeholder(photo_path_default):
    """{id} must appear in photo_path_default so each person gets a unique URL."""
    assert "{id}" in photo_path_default, (
        f"photo_path_default ('{photo_path_default}') must contain the literal "
        f"string {{id}} so it can be substituted with each person's ID."
    )


def test_every_person_has_a_photo_file(root, people, photo_path_default):
    """
    Every person in _data/people.yml must have a photo file on disk.

    SVG files stored in the repo are converted to JPEG at build time, so an
    SVG source file (e.g. ``mac-katz.svg``) is accepted as a valid stand-in for
    the expected JPEG (``mac-katz.jpg``) when the JPEG is not yet present.

    If this test fails, either:
      • Add the missing photo file at the listed path, OR
      • Add a ``photo:`` override in people.yml pointing to an existing file.
    """
    missing = []
    for person in people:
        photo_path = _expected_photo_path(root, person, photo_path_default)
        # Accept an SVG source file when the expected JPEG hasn't been
        # generated yet (SVGs are rasterised to JPEG during the build).
        svg_path = photo_path.with_suffix(".svg")
        if not photo_path.exists() and not svg_path.exists():
            missing.append(
                f"  {person['id']!r} → expected {photo_path.relative_to(root)}"
            )
    assert not missing, (
        "Photo files missing for these people:\n" + "\n".join(missing) + "\n\n"
        "Add the missing files or set a `photo:` override in _data/people.yml."
    )


def test_every_photo_file_is_a_valid_image(root, people, photo_path_default):
    """
    Each existing photo file must be a valid image (non-empty, correct header).

    An invalid file (e.g. a zero-byte placeholder or a renamed text file) would
    cause the browser to show a broken-image icon — exactly what this test is
    designed to catch.
    """
    invalid = []
    for person in people:
        photo_path = _expected_photo_path(root, person, photo_path_default)
        if not photo_path.exists():
            continue  # Covered by test_every_person_has_a_photo_file
        if photo_path.stat().st_size == 0:
            invalid.append(f"  {person['id']!r} → {photo_path.relative_to(root)} is empty (0 bytes)")
            continue
        if photo_path.suffix.lower() not in _VALID_EXTENSIONS:
            invalid.append(
                f"  {person['id']!r} → {photo_path.relative_to(root)} "
                f"has unrecognised extension '{photo_path.suffix}'"
            )
            continue
        if not _is_valid_image(photo_path):
            invalid.append(
                f"  {person['id']!r} → {photo_path.relative_to(root)} "
                f"does not have a valid image header"
            )
    assert not invalid, (
        "The following photo files exist but are not valid images:\n"
        + "\n".join(invalid)
    )


def test_custom_photo_overrides_point_to_existing_files(root, people):
    """
    If a person has an explicit ``photo:`` field, that file must exist.

    This catches the case where someone sets a custom photo path in people.yml
    but forgets to upload the actual file.
    """
    bad = []
    for person in people:
        if "photo" not in person:
            continue
        photo_path = root / person["photo"].lstrip("/")
        if not photo_path.exists():
            bad.append(
                f"  {person['id']!r} → photo override "
                f"'{person['photo']}' does not exist"
            )
    assert not bad, (
        "Custom photo overrides that point to missing files:\n" + "\n".join(bad)
    )
