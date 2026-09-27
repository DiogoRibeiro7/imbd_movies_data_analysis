"""Compatibility imports for the original box-office extraction module.

New code should import from :mod:`imdb_movie_analysis.scraping`.
"""

from imdb_movie_analysis.scraping import fetch_box_office_data

__all__ = ["fetch_box_office_data"]
