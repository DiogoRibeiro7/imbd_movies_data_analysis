from __future__ import annotations

from typing import Any

from imdb_movie_analysis.scraping import (
    fetch_all_imdb_movies,
    parse_box_office_html,
    parse_imdb_movies_html,
)


IMDB_PAGE = """
<div class="lister-item mode-advanced">
  <div class="lister-item-content">
    <h3><a>The Example Film</a></h3>
    <span class="genre">Drama, Mystery</span>
    <span class="runtime">121 min</span>
    <strong>8.2</strong>
    <span class="metascore">74</span>
    <span name="nv" data-value="123456">123,456</span>
    <span name="nv" data-value="9876543">$9.88M</span>
  </div>
</div>
<a class="lister-page-next next-page">Next</a>
"""

IMDB_PAGE_WITHOUT_NUMERICS = """
<div class="lister-item mode-advanced">
  <div class="lister-item-content">
    <h3><a>No Votes Yet</a></h3>
  </div>
</div>
"""

BOX_OFFICE_PAGE = """
<table>
  <tr><th>Rank</th><th>Title</th><th>Worldwide</th><th>Domestic</th><th>%</th><th>Foreign</th></tr>
  <tr><td>1</td><td>Film A</td><td>$100</td><td>$60</td><td>60%</td><td>$40</td></tr>
  <tr><td>malformed</td></tr>
</table>
"""


class FakeResponse:
    def __init__(self, text: str) -> None:
        self.text = text

    def raise_for_status(self) -> None:
        return None


class FakeSession:
    def __init__(self, pages: list[str]) -> None:
        self._pages = iter(pages)
        self.calls: list[dict[str, Any]] = []

    def get(self, url: str, **kwargs: Any) -> FakeResponse:
        self.calls.append({"url": url, **kwargs})
        return FakeResponse(next(self._pages))

    def close(self) -> None:
        return None


def test_parse_imdb_movies_html() -> None:
    records, has_next = parse_imdb_movies_html(IMDB_PAGE)

    assert has_next is True
    assert records == [
        {
            "title": "The Example Film",
            "audience_rating": "8.2",
            "genre": "Drama, Mystery",
            "critic_rating": "74",
            "runtime": "121 min",
            "votes": "123456",
            "gross": "9876543",
        }
    ]


def test_parse_imdb_movies_handles_missing_numeric_spans() -> None:
    records, has_next = parse_imdb_movies_html(IMDB_PAGE_WITHOUT_NUMERICS)

    assert has_next is False
    assert records[0]["votes"] == "N/A"
    assert records[0]["gross"] == "N/A"


def test_parse_box_office_skips_malformed_rows() -> None:
    assert parse_box_office_html(BOX_OFFICE_PAGE) == [
        {
            "Rank": "1",
            "title": "Film A",
            "Worldwide": "$100",
            "Domestic": "$60",
            "Foreign": "$40",
        }
    ]


def test_fetch_all_imdb_movies_paginates_without_live_network() -> None:
    second_page = IMDB_PAGE.replace(
        '<a class="lister-page-next next-page">Next</a>',
        "",
    )
    session = FakeSession([IMDB_PAGE, second_page])

    records = fetch_all_imdb_movies(
        "https://example.test/search?sort=votes",
        session=session,  # type: ignore[arg-type]
    )

    assert len(records) == 2
    assert [call["url"] for call in session.calls] == [
        "https://example.test/search?sort=votes&start=1",
        "https://example.test/search?sort=votes&start=51",
    ]
    assert all(call["timeout"] == 30.0 for call in session.calls)
