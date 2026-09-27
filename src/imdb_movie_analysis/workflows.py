"""Explicit data-collection workflows for the analysis project."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pandas as pd

from imdb_movie_analysis.scraping import (
    BoxOfficeRecord,
    ImdbMovieRecord,
    fetch_all_imdb_movies,
    fetch_box_office_data,
)

MovieFetcher = Callable[[str, int], list[ImdbMovieRecord]]
BoxOfficeFetcher = Callable[[str], list[BoxOfficeRecord]]


def collect_imdb_movies(
    start_year: int,
    end_year: int,
    *,
    max_results_per_year: int = 10_000,
    fetcher: MovieFetcher = fetch_all_imdb_movies,
) -> pd.DataFrame:
    """Collect IMDb movie metadata for an inclusive year range."""
    if end_year < start_year:
        raise ValueError("end_year must be greater than or equal to start_year")
    if max_results_per_year < 0:
        raise ValueError("max_results_per_year must not be negative")

    frames: list[pd.DataFrame] = []
    for year in range(start_year, end_year + 1):
        base_url = (
            "https://www.imdb.com/search/title/"
            f"?release_date={year}-01-01,{year}-12-31&sort=num_votes,desc"
        )
        records = fetcher(base_url, max_results_per_year)
        frame = pd.DataFrame(records)
        if frame.empty:
            continue

        frame["year"] = year
        frames.append(frame)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def collect_box_office(
    start_year: int,
    end_year: int,
    *,
    fetcher: BoxOfficeFetcher = fetch_box_office_data,
) -> pd.DataFrame:
    """Collect Box Office Mojo yearly tables for an inclusive year range."""
    if end_year < start_year:
        raise ValueError("end_year must be greater than or equal to start_year")

    frames: list[pd.DataFrame] = []
    for year in range(start_year, end_year + 1):
        url = f"https://www.boxofficemojo.com/year/world/{year}/"
        records = fetcher(url)
        frame = pd.DataFrame(records)
        if frame.empty:
            continue

        frame["year"] = year
        frames.append(frame)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def write_csv(data_frame: pd.DataFrame, output: Path) -> Path:
    """Write a collected dataset without overwriting parent-directory structure."""
    output.parent.mkdir(parents=True, exist_ok=True)
    data_frame.to_csv(output, index=False)
    return output
