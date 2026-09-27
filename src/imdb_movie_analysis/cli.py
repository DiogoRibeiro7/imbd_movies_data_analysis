"""Command-line interface for explicit data collection."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from imdb_movie_analysis.workflows import (
    collect_box_office,
    collect_imdb_movies,
    write_csv,
)

DEFAULT_START_YEAR = 2000
DEFAULT_END_YEAR = 2022


def build_parser() -> argparse.ArgumentParser:
    """Build the project command-line parser."""
    parser = argparse.ArgumentParser(
        prog="imdb-movie-analysis",
        description=(
            "Collect fresh IMDb or Box Office Mojo data without modifying the "
            "historical snapshots committed at the repository root."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    imdb = subparsers.add_parser("imdb", help="Collect IMDb movie metadata.")
    imdb.add_argument("--start-year", type=int, default=DEFAULT_START_YEAR)
    imdb.add_argument("--end-year", type=int, default=DEFAULT_END_YEAR)
    imdb.add_argument("--max-results-per-year", type=int, default=10_000)
    imdb.add_argument(
        "--output",
        type=Path,
        default=Path("data/generated/movies.csv"),
    )

    box_office = subparsers.add_parser(
        "box-office",
        help="Collect Box Office Mojo yearly worldwide tables.",
    )
    box_office.add_argument("--start-year", type=int, default=DEFAULT_START_YEAR)
    box_office.add_argument("--end-year", type=int, default=DEFAULT_END_YEAR)
    box_office.add_argument(
        "--output",
        type=Path,
        default=Path("data/generated/box_office.csv"),
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the requested collection workflow."""
    args = build_parser().parse_args(argv)

    if args.command == "imdb":
        data_frame = collect_imdb_movies(
            args.start_year,
            args.end_year,
            max_results_per_year=args.max_results_per_year,
        )
    else:
        data_frame = collect_box_office(
            args.start_year,
            args.end_year,
        )

    output = write_csv(data_frame, args.output)
    print(f"Wrote {len(data_frame)} rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
