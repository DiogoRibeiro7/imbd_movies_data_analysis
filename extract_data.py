"""Compatibility imports for the original IMDb extraction module.

New code should import from :mod:`imdb_movie_analysis.scraping`.
"""

from imdb_movie_analysis.scraping import (
    fetch_all_imdb_gross,
    fetch_all_imdb_movies,
)

__all__ = ["fetch_all_imdb_gross", "fetch_all_imdb_movies"]
