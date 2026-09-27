"""HTML parsing and HTTP acquisition helpers for historical movie data."""

from __future__ import annotations

from typing import TypedDict

import requests
from bs4 import BeautifulSoup

DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0"}


class ImdbMovieRecord(TypedDict):
    """Movie metadata parsed from the legacy IMDb search layout."""

    title: str
    audience_rating: str
    genre: str
    critic_rating: str
    runtime: str
    votes: str
    gross: str


class ImdbGrossRecord(TypedDict):
    """Title and gross value parsed from the legacy IMDb search layout."""

    title: str
    gross: str


class BoxOfficeRecord(TypedDict):
    """Movie revenue fields parsed from a Box Office Mojo yearly table."""

    Rank: str
    title: str
    Worldwide: str
    Domestic: str
    Foreign: str


def parse_imdb_movies_html(html: str) -> tuple[list[ImdbMovieRecord], bool]:
    """Parse movie metadata from IMDb's legacy advanced-search HTML.

    Returns:
        A tuple containing the parsed records and whether a legacy next-page link
        was present.
    """
    soup = BeautifulSoup(html, "html.parser")
    records: list[ImdbMovieRecord] = []

    for container in soup.find_all("div", class_="lister-item mode-advanced"):
        title_node = container.select_one("h3 a")
        if title_node is None:
            continue

        genre_node = container.find("span", class_="genre")
        metascore_node = container.find("span", class_="metascore")
        runtime_node = container.find("span", class_="runtime")
        rating_node = container.find("strong")
        numeric_nodes = container.find_all("span", attrs={"name": "nv"})

        votes = "N/A"
        if numeric_nodes:
            votes = numeric_nodes[0].get("data-value") or numeric_nodes[0].get_text(
                strip=True
            )

        gross = "N/A"
        if len(numeric_nodes) >= 2:
            gross = numeric_nodes[1].get("data-value") or numeric_nodes[1].get_text(
                strip=True
            )

        records.append(
            ImdbMovieRecord(
                title=title_node.get_text(strip=True),
                audience_rating=(
                    rating_node.get_text(strip=True) if rating_node else "N/A"
                ),
                genre=genre_node.get_text(strip=True) if genre_node else "N/A",
                critic_rating=(
                    metascore_node.get_text(strip=True) if metascore_node else "N/A"
                ),
                runtime=runtime_node.get_text(strip=True) if runtime_node else "N/A",
                votes=votes,
                gross=gross,
            )
        )

    has_next = soup.find("a", class_="lister-page-next next-page") is not None
    return records, has_next


def parse_imdb_gross_html(html: str) -> tuple[list[ImdbGrossRecord], bool]:
    """Parse title/gross records from IMDb's legacy search-result HTML."""
    soup = BeautifulSoup(html, "html.parser")
    records: list[ImdbGrossRecord] = []

    for container in soup.find_all("div", class_="lister-item-content"):
        title_node = container.find("a")
        if title_node is None:
            continue

        gross_node = container.find("span", attrs={"name": "nv"})
        records.append(
            ImdbGrossRecord(
                title=title_node.get_text(strip=True),
                gross=gross_node.get_text(strip=True) if gross_node else "N/A",
            )
        )

    has_next = soup.find("a", class_="lister-page-next next-page") is not None
    return records, has_next


def parse_box_office_html(html: str) -> list[BoxOfficeRecord]:
    """Parse a yearly Box Office Mojo table.

    Malformed or non-data rows are skipped instead of raising an index error.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        return []

    records: list[BoxOfficeRecord] = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) < 6:
            continue

        records.append(
            BoxOfficeRecord(
                Rank=cells[0].get_text(strip=True),
                title=cells[1].get_text(strip=True),
                Worldwide=cells[2].get_text(strip=True),
                Domestic=cells[3].get_text(strip=True),
                Foreign=cells[5].get_text(strip=True),
            )
        )

    return records


def _get_text(
    url: str,
    *,
    session: requests.Session,
    timeout: float,
) -> str:
    """Fetch one HTML document and raise for HTTP failures."""
    response = session.get(
        url,
        headers=DEFAULT_HEADERS,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.text


def fetch_all_imdb_movies(
    base_url: str,
    end_index: int = 0,
    *,
    session: requests.Session | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> list[ImdbMovieRecord]:
    """Fetch and parse paginated IMDb results using the legacy HTML layout."""
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    if end_index < 0:
        raise ValueError("end_index must not be negative")

    owns_session = session is None
    client = session or requests.Session()
    records: list[ImdbMovieRecord] = []
    start_index = 1

    try:
        while True:
            html = _get_text(
                f"{base_url}&start={start_index}",
                session=client,
                timeout=timeout,
            )
            page_records, has_next = parse_imdb_movies_html(html)
            if not page_records:
                break

            records.extend(page_records)

            if not has_next:
                break

            start_index += 50
            if end_index and end_index <= start_index:
                break
    finally:
        if owns_session:
            client.close()

    return records


def fetch_all_imdb_gross(
    base_url: str,
    end_index: int = 0,
    *,
    session: requests.Session | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> list[ImdbGrossRecord]:
    """Fetch and parse paginated IMDb gross results using the legacy layout."""
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    if end_index < 0:
        raise ValueError("end_index must not be negative")

    owns_session = session is None
    client = session or requests.Session()
    records: list[ImdbGrossRecord] = []
    start_index = 1

    try:
        while True:
            html = _get_text(
                f"{base_url}&start={start_index}",
                session=client,
                timeout=timeout,
            )
            page_records, has_next = parse_imdb_gross_html(html)
            if not page_records:
                break

            records.extend(page_records)

            if not has_next:
                break

            start_index += 50
            if end_index and end_index <= start_index:
                break
    finally:
        if owns_session:
            client.close()

    return records


def fetch_box_office_data(
    url: str,
    *,
    session: requests.Session | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> list[BoxOfficeRecord]:
    """Fetch and parse one Box Office Mojo yearly table."""
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    owns_session = session is None
    client = session or requests.Session()
    try:
        html = _get_text(url, session=client, timeout=timeout)
    finally:
        if owns_session:
            client.close()

    return parse_box_office_html(html)
