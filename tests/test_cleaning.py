import pandas as pd
import pytest

from imdb_movie_analysis.cleaning import (
    currency_to_number,
    extract_first_category,
    extract_minutes,
    normalize_missing_currency,
    parse_gross_usd,
)


def test_currency_to_number() -> None:
    assert currency_to_number("$2,320,250,281") == 2_320_250_281
    assert currency_to_number(42) == 42


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("176 min", 176),
        ("1,234 min", 1234),
        (95, 95),
        (95.9, 95),
    ],
)
def test_extract_minutes(value: str | int | float, expected: int) -> None:
    assert extract_minutes(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Action, Crime, Drama", "Action"),
        ("Drama", "Drama"),
        (7, "7"),
    ],
)
def test_extract_first_category(value: str | int | float, expected: str) -> None:
    assert extract_first_category(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("$16.46M", 16_460_000),
        ("$0.01M", 10_000),
        ("$850K", 850_000),
        ("$1.2B", 1_200_000_000),
        ("5,581", 5_581),
        ("13", 13),
        ("32,131,830", 32_131_830),
        (1200, 1200),
    ],
)
def test_parse_gross_usd(value: str | int | float, expected: int | float) -> None:
    assert parse_gross_usd(value) == expected


def test_normalize_missing_currency_returns_copy() -> None:
    frame = pd.DataFrame({"Domestic": ["-", "$10"], "Foreign": ["$5", "-"]})

    result = normalize_missing_currency(frame, ["Domestic", "Foreign"])

    assert result.to_dict(orient="list") == {
        "Domestic": ["$0", "$10"],
        "Foreign": ["$5", "$0"],
    }
    assert frame.to_dict(orient="list") == {
        "Domestic": ["-", "$10"],
        "Foreign": ["$5", "-"],
    }


@pytest.mark.parametrize(
    "call",
    [
        lambda: currency_to_number(""),
        lambda: extract_minutes(""),
        lambda: extract_first_category(""),
        lambda: parse_gross_usd(""),
    ],
)
def test_empty_values_raise_value_error(call) -> None:
    with pytest.raises(ValueError):
        call()
