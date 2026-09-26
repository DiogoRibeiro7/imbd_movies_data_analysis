# IMDb Movie Analysis

Exploratory analysis of IMDb movie metadata and box-office data, with historical
snapshots covering films released between 2000 and 2022.

The repository is being modernized from an older notebook-and-scripts project into a
reproducible analysis workflow. The original notebook and data snapshots are preserved
while the extraction, cleaning, validation, and analysis code is progressively moved
into tested modules.

## Current contents

- `movie_analysis.ipynb` — original exploratory notebook.
- `movies.csv` — historical IMDb metadata snapshot.
- `box_office.csv` — historical box-office snapshot.
- `extract_data.py` — legacy IMDb extraction helpers.
- `extract_gross.py` — legacy Box Office Mojo extraction helper.
- `currency_to_int.py` — legacy cleaning and conversion utilities.
- `main.py` — original orchestration script.

## Status

The committed CSV files should be treated as **historical snapshots**, not live data.

The scraping code was written against the HTML structure available in 2023. IMDb and
Box Office Mojo can change their markup, access rules, or anti-automation behavior at
any time, so the legacy selectors should not be assumed to work against the current
sites without validation.

The modernization work will separate:

1. data acquisition;
2. parsing and normalization;
3. validation;
4. analysis;
5. reproducible notebooks and reports.

## Requirements

- Python 3.12, 3.13, or 3.14
- Poetry

## Development setup

Clone the repository and install the environment:

```bash
git clone https://github.com/DiogoRibeiro7/imbd_movies_data_analysis.git
cd imbd_movies_data_analysis
poetry install
```

Start JupyterLab with:

```bash
poetry run jupyter lab
```

## Data provenance

The repository contains data originally collected from:

- IMDb movie-search pages;
- Box Office Mojo yearly worldwide box-office pages.

The source websites remain authoritative for their current data and terms of use.
Committed datasets are retained for reproducibility of the historical analysis.

## Reproducibility

Do not overwrite the historical CSV snapshots when experimenting with new extraction
code. New acquisition workflows should write to a separate generated-data location
until the provenance and schema are validated.

## Roadmap

The next modernization steps are:

- move reusable code into a structured `src/` layout;
- remove import-time execution and duplicated imports;
- add typed data models and deterministic parsing tests;
- separate network access from HTML parsing;
- establish CI with Ruff and pytest;
- move generated data away from the repository root;
- rebuild the notebook against the cleaned analysis API;
- add MkDocs documentation using the repository documentation design standard.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
