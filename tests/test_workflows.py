from pathlib import Path

import pandas as pd
import pytest

from imdb_movie_analysis.workflows import (
    collect_box_office,
    collect_imdb_movies,
    write_csv,
)


def test_collect_imdb_movies_adds_year() -> None:
    calls: list[tuple[str, int]] = []

    def fake_fetcher(url: str, limit: int):
        calls.append((url, limit))
        return [
            {
                "title": "Example",
                "audience_rating": "8.0",
                "genre": "Drama",
                "critic_rating": "70",
                "runtime": "120 min",
                "votes": "100",
                "gross": "1000",
            }
        ]

    result = collect_imdb_movies(
        2020,
        2021,
        max_results_per_year=500,
        fetcher=fake_fetcher,
    )

    assert result["year"].tolist() == [2020, 2021]
    assert calls == [
        (
            "https://www.imdb.com/search/title/"
            "?release_date=2020-01-01,2020-12-31&sort=num_votes,desc",
            500,
        ),
        (
            "https://www.imdb.com/search/title/"
            "?release_date=2021-01-01,2021-12-31&sort=num_votes,desc",
            500,
        ),
    ]


def test_collect_box_office_adds_year() -> None:
    def fake_fetcher(url: str):
        return [
            {
                "Rank": "1",
                "title": url.rsplit("/", maxsplit=2)[-2],
                "Worldwide": "$100",
                "Domestic": "$60",
                "Foreign": "$40",
            }
        ]

    result = collect_box_office(2021, 2022, fetcher=fake_fetcher)

    assert result["year"].tolist() == [2021, 2022]


@pytest.mark.parametrize(
    "function,args",
    [
        (collect_imdb_movies, (2022, 2021)),
        (collect_box_office, (2022, 2021)),
    ],
)
def test_collectors_reject_reversed_year_ranges(function, args) -> None:
    with pytest.raises(ValueError):
        function(*args)


def test_write_csv_creates_parent_directories(tmp_path: Path) -> None:
    output = tmp_path / "data" / "generated" / "movies.csv"
    frame = pd.DataFrame({"title": ["Example"]})

    result = write_csv(frame, output)

    assert result == output
    assert pd.read_csv(output).to_dict(orient="list") == {"title": ["Example"]}
