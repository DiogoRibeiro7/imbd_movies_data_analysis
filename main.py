import pandas as pd
from extract_data import fetch_all_imdb_movies
from extract_gross import fetch_box_office_data



for year in range(2000, 2023, 1):
    print(year)
    base_url = f"https://www.imdb.com/search/title/?release_date={year}-01-01,{year}-12-31&sort=num_votes,desc"
    movies = fetch_all_imdb_movies(base_url)
movies = pd.DataFrame(movies)
movies.to_csv("movies.csv")


for year in range(2000, 2023, 1):
    print(year)
    url = f"https://www.boxofficemojo.com/year/world/{year}/"
    data = fetch_box_office_data(url)
box_office = pd.DataFrame(data)
box_office.to_csv("box_office.csv")

