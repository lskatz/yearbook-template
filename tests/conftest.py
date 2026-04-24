"""Shared fixtures for the yearbook test suite."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_front_matter(path: Path) -> dict:
    """Parse the YAML front-matter out of a Markdown file."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path} has no YAML front-matter")
    return yaml.safe_load(match.group(1)) or {}


@pytest.fixture(scope="session")
def root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def people(root) -> list[dict]:
    """The raw people list from _data/people.yml."""
    return load_yaml(root / "_data" / "people.yml")


@pytest.fixture(scope="session")
def people_by_id(people) -> dict[str, dict]:
    return {p["id"]: p for p in people}


@pytest.fixture(scope="session")
def classes(root) -> list[dict]:
    return [load_front_matter(p) for p in (root / "_classes").glob("*.md")]


@pytest.fixture(scope="session")
def clubs(root) -> list[dict]:
    return [load_front_matter(p) for p in (root / "_clubs").glob("*.md")]


@pytest.fixture(scope="session")
def sports(root) -> list[dict]:
    return [load_front_matter(p) for p in (root / "_sports").glob("*.md")]


@pytest.fixture(scope="session")
def photo_pages(root) -> list[dict]:
    """Front-matter dicts for all pages in the _photos/ collection."""
    return [load_front_matter(p) for p in (root / "_photos").glob("*.md")]
