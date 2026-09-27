#!/usr/bin/env python3
"""Validate the structure and metadata of Claude Agent Skills.

The validator intentionally implements only the small frontmatter subset used
by this repository.  It does not import a YAML package, which keeps the module
safe to import in a clean Python installation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable, Optional, Tuple, Union


_MAX_DESCRIPTION_LENGTH = 1024
_MAX_BODY_LINES = 500
_FRONTMATTER_DELIMITER = "---"
_FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$")
_REFERENCE_PREFIX = "references/"
_KEBAB_CASE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_REFERENCE_TRAILING_PUNCTUATION = ".,;:!?)]}>\"'`*_~"
_REFERENCE_LEADING_PUNCTUATION = "([<{\"'"


def _normalise_text(raw: bytes) -> Tuple[str, Optional[str]]:
    """Decode UTF-8 and normalise BOM and line endings."""

    encoding_error: str | None = None
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        encoding_error = f"encoding: SKILL.md is not valid UTF-8 ({exc})"
        text = raw.decode("utf-8-sig", errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n"), encoding_error


def _is_block_indicator(value: str) -> bool:
    return value in {">", ">-", "|", "|-"}


def _parse_quoted(value: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse one supported YAML-like quoted scalar."""

    if not value:
        return "", None
    if value[0] == "'":
        if len(value) < 2 or value[-1] != "'":
            return None, "unclosed single-quoted scalar"
        inner = value[1:-1].replace("''", "'")
        return inner, None
    if value[0] == '"':
        if len(value) < 2 or value[-1] != '"':
            return None, "unclosed double-quoted scalar"
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return None, "invalid double-quoted scalar"
        if not isinstance(parsed, str):
            return None, "invalid double-quoted scalar"
        return parsed, None
    return value, None


def _block_scalar(
    lines: list[str], start: int, indicator: str
) -> Tuple[str, int, Optional[str]]:
    """Read a ``>``/``|`` scalar and return value, next line, and an error."""

    end = start
    while end < len(lines):
        line = lines[end]
        if line.strip() and (not line.startswith(" ") or line.startswith("\t")):
            break
        end += 1

    content = lines[start:end]
    nonblank = [line for line in content if line.strip()]
    if nonblank:
        if any(line.startswith("\t") for line in content):
            return "", end, "tabs are not supported for block scalar indentation"
        # YAML takes the indentation from the first non-blank line; a later
        # line indented less is a parse error for real YAML loaders.
        indentation = len(nonblank[0]) - len(nonblank[0].lstrip(" "))
        if any(len(line) - len(line.lstrip(" ")) < indentation for line in nonblank):
            return "", end, "inconsistent block scalar indentation"
        content = [line[indentation:] if line.strip() else "" for line in content]

    if indicator.startswith(">"):
        folded: list[str] = []
        for line in content:
            if not line:
                if folded and folded[-1] != "\n":
                    folded.append("\n")
            elif folded and folded[-1] != "\n":
                folded.append(" ")
            folded.append(line)
        value = "".join(folded)
    else:
        value = "\n".join(content)

    if indicator in {">", "|"} and content:
        value += "\n"
    return value, end, None


def _parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], int, list[str]]:
    """Parse the supported scalar subset and return fields, body start, errors."""

    errors: list[str] = []
    fields: dict[str, str] = {}
    if not lines or lines[0] != _FRONTMATTER_DELIMITER:
        return fields, 0, ["frontmatter: missing opening --- delimiter"]

    closing = None
    for index in range(1, len(lines)):
        if lines[index] == _FRONTMATTER_DELIMITER:
            closing = index
            break

    frontmatter_end = closing if closing is not None else len(lines)
    if closing is None:
        errors.append("frontmatter: missing closing --- delimiter")

    index = 1
    while index < frontmatter_end:
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line[0].isspace():
            errors.append(f"frontmatter: invalid line {index + 1}")
            index += 1
            continue

        match = _FIELD_RE.match(line)
        if not match:
            errors.append(f"frontmatter: invalid line {index + 1}")
            index += 1
            continue

        key, raw_value = match.groups()
        if key in fields:
            errors.append(f"frontmatter: duplicate field {key!r}")

        if _is_block_indicator(raw_value):
            value, next_index, block_error = _block_scalar(lines, index + 1, raw_value)
            if block_error:
                errors.append(f"frontmatter: {block_error} on field {key!r}")
            fields[key] = value.rstrip("\n") if raw_value.endswith("-") else value
            index = next_index
            continue

        if raw_value.startswith((">", "|")):
            errors.append(
                f"frontmatter: unsupported scalar form for field {key!r}; "
                "supported forms are plain, quoted, >, >-, |, |-"
            )
            fields[key] = ""
            index += 1
            continue

        value, scalar_error = _parse_quoted(raw_value)
        if scalar_error:
            errors.append(f"frontmatter: {scalar_error} on field {key!r}")
            fields[key] = ""
        else:
            fields[key] = value or ""
        index += 1

    # With no closing delimiter, the remainder is still useful body material
    # for independent body-length and reference checks.
    return fields, (closing + 1 if closing is not None else 1), errors


def _normalised_description(value: str) -> str:
    """Normalise scalar whitespace for the documented length check."""

    return " ".join(value.replace("\r\n", "\n").replace("\r", "\n").split())


def _is_placeholder(path: str) -> bool:
    """Return whether a reference contains a non-concrete path component."""

    if any(token in path for token in ("*", "?", "...", "…", "\\")):
        return True
    if any(mark in path for mark in ("<", ">", "{", "}", "[", "]", "$")):
        return True
    return any(segment.startswith(":") for segment in path.split("/"))


def _reference_candidates(text: str) -> list[str]:
    """Find concrete-looking ``references/...`` tokens in document text."""

    found: set[str] = set()
    position = 0
    while True:
        start = text.find(_REFERENCE_PREFIX, position)
        if start < 0:
            break
        position = start + len(_REFERENCE_PREFIX)
        if start and text[start - 1] == "\\":
            continue

        end = position
        while end < len(text) and not text[end].isspace():
            end += 1
        candidate = text[start:end].strip(_REFERENCE_LEADING_PUNCTUATION)
        # A Markdown link may add an anchor after the concrete file path.
        # Treat that fragment as punctuation, rather than looking for a file
        # whose literal name includes the anchor.
        if "#" in candidate:
            candidate = candidate.split("#", 1)[0]
        candidate = candidate.rstrip(_REFERENCE_TRAILING_PUNCTUATION)
        if not candidate or candidate == _REFERENCE_PREFIX.rstrip("/"):
            continue
        if not candidate.startswith(_REFERENCE_PREFIX) or _is_placeholder(candidate):
            continue
        found.add(candidate)
    return sorted(found)


def _reference_errors(text: str, skill_dir: Path) -> list[str]:
    errors: list[str] = []
    try:
        root = skill_dir.resolve()
    except (OSError, RuntimeError, ValueError) as exc:
        return [f"references: cannot resolve skill directory ({exc})"]
    for reference in _reference_candidates(text):
        relative = Path(reference)
        try:
            target = (skill_dir / relative).resolve()
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(f"references: cannot resolve {reference} ({exc})")
            continue
        try:
            target.relative_to(root)
        except ValueError:
            errors.append(f"references: path escapes skill directory: {reference}")
            continue
        try:
            exists = target.exists()
        except OSError as exc:
            errors.append(f"references: cannot inspect {reference} ({exc})")
            continue
        if not exists:
            errors.append(f"references: missing {reference}")
    return errors


def validate_skill(path: Union[str, Path]) -> list[str]:
    """Return all validation errors for the skill directory at *path*."""

    skill_dir = Path(path)
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_dir.is_dir():
        return [f"skill directory does not exist: {skill_dir}"]
    if not skill_file.is_file():
        return ["SKILL.md: missing"]

    try:
        raw = skill_file.read_bytes()
    except OSError as exc:
        return [f"encoding: cannot read SKILL.md ({exc})"]

    text, encoding_error = _normalise_text(raw)
    if encoding_error:
        errors.append(encoding_error)
    lines = text.splitlines()
    fields, body_start, frontmatter_errors = _parse_frontmatter(lines)
    errors.extend(frontmatter_errors)

    expected_name = skill_dir.name
    actual_name = fields.get("name", "").strip()
    if not actual_name:
        errors.append("name: missing")
    elif actual_name != expected_name:
        errors.append(f"name: expected {expected_name!r}, got {actual_name!r}")
    if actual_name and not _KEBAB_CASE.fullmatch(actual_name):
        errors.append(f"name: {actual_name!r} is not lowercase kebab-case")

    description = fields.get("description")
    if description is None or not _normalised_description(description):
        errors.append("description: missing")
    elif len(_normalised_description(description)) > _MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"description: normalized length exceeds {_MAX_DESCRIPTION_LENGTH} characters"
        )

    body_lines = lines[body_start:] if body_start else lines
    if len(body_lines) > _MAX_BODY_LINES:
        errors.append(f"body: exceeds {_MAX_BODY_LINES} lines")

    errors.extend(_reference_errors(text, skill_dir))
    if "rules.md" in text and not (skill_dir / "rules.md").is_file():
        errors.append("rules: SKILL.md mentions rules.md but the file is missing")
    return errors


def validate_all(directory: Union[str, Path]) -> dict[str, list[str]]:
    """Validate every immediate, non-hidden directory in deterministic order."""

    root = Path(directory)
    if not root.is_dir():
        return {}
    skill_dirs = sorted(
        (entry for entry in root.iterdir() if not entry.name.startswith(".") and entry.is_dir()),
        key=lambda entry: entry.name,
    )
    return {entry.name: validate_skill(entry) for entry in skill_dirs}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Claude Agent Skills.")
    parser.add_argument(
        "directory",
        nargs="?",
        default="skills",
        help="directory containing skill directories (default: skills)",
    )
    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    root = Path(args.directory)
    if not root.is_dir():
        print(f"ERROR {root}: directory does not exist", file=sys.stderr)
        return 2

    results = validate_all(root)
    failed = False
    for name, errors in results.items():
        if errors:
            failed = True
            print(f"FAIL {name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {name}")
    if not results:
        print(f"ERROR {root}: no visible skill directories found", file=sys.stderr)
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
