from pathlib import Path

from imdb_movie_analysis.cli import build_parser


def test_imdb_cli_defaults() -> None:
    args = build_parser().parse_args(["imdb"])

    assert args.command == "imdb"
    assert args.start_year == 2000
    assert args.end_year == 2022
    assert args.max_results_per_year == 10_000
    assert args.output == Path("data/generated/movies.csv")


def test_box_office_cli_accepts_explicit_range() -> None:
    args = build_parser().parse_args(
        [
            "box-office",
            "--start-year",
            "2018",
            "--end-year",
            "2020",
            "--output",
            "custom.csv",
        ]
    )

    assert args.command == "box-office"
    assert args.start_year == 2018
    assert args.end_year == 2020
    assert args.output == Path("custom.csv")
