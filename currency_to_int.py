"""Compatibility wrappers for the original cleaning helper module.

New code should import from :mod:`imdb_movie_analysis`.
"""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from imdb_movie_analysis.cleaning import (
    currency_to_number,
    extract_first_category,
    extract_minutes,
    normalize_missing_currency,
    parse_gross_usd,
)


def replace_hyphen_in_columns(
    data_frame: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    """Backward-compatible alias for :func:`normalize_missing_currency`."""
    return normalize_missing_currency(data_frame, columns)


def convert_gross_to_numeric(gross: str | int | float) -> int | float:
    """Backward-compatible alias for :func:`parse_gross_usd`."""
    return parse_gross_usd(gross)


__all__ = [
    "convert_gross_to_numeric",
    "currency_to_number",
    "extract_first_category",
    "extract_minutes",
    "replace_hyphen_in_columns",
]
