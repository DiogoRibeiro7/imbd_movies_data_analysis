"""Deterministic cleaning helpers for movie and box-office data."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def currency_to_number(value: str | int) -> int:
    """Convert a dollar-formatted integer value into an integer.

    Examples:
        `"$2,320,250,281"` becomes `2320250281`.
    """
    if isinstance(value, int):
        return value

    cleaned = value.strip().replace("$", "").replace(",", "")
    if not cleaned:
        raise ValueError("currency value must not be empty")

    return int(cleaned)


def normalize_missing_currency(
    data_frame: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    """Replace dash placeholders with a zero-dollar string in selected columns.

    A copy is returned so callers do not get an unexpected in-place mutation.
    """
    normalized = data_frame.copy()
    for column in columns:
        normalized[column] = normalized[column].replace("-", "$0")
    return normalized


def extract_minutes(value: str | int | float) -> int:
    """Extract a runtime in minutes from values such as `"176 min"`."""
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)

    normalized = value.strip().replace(",", "")
    if not normalized:
        raise ValueError("runtime value must not be empty")

    return int(normalized.split()[0])


def extract_first_category(value: str | int | float) -> str:
    """Return the first category from a comma-separated genre string."""
    text = str(value).strip()
    if not text:
        raise ValueError("category value must not be empty")

    return text.split(",", maxsplit=1)[0].strip()


def parse_gross_usd(value: str | int | float) -> int | float:
    """Parse common IMDb/box-office gross formats into US-dollar values.

    Supported examples include `"$16.46M"`, `"$850K"`,
    `"32,131,830"`, and already-numeric values.

    Plain numeric strings are interpreted literally rather than implicitly as
    millions. This removes an ambiguity in the legacy helper.
    """
    if isinstance(value, (int, float)):
        return value

    normalized = value.strip().replace("$", "").replace(",", "")
    if not normalized:
        raise ValueError("gross value must not be empty")

    multiplier = 1
    suffix = normalized[-1].upper()
    if suffix == "M":
        multiplier = 1_000_000
        normalized = normalized[:-1]
    elif suffix == "K":
        multiplier = 1_000
        normalized = normalized[:-1]
    elif suffix == "B":
        multiplier = 1_000_000_000
        normalized = normalized[:-1]

    if not normalized:
        raise ValueError("gross value must contain a number")

    number = float(normalized)
    result = number * multiplier
    return int(result) if result.is_integer() else result
