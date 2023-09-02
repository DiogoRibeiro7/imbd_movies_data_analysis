import pandas as pd
from extract_data import fetch_all_imdb_movies, fetch_all_imdb_gross
from extract_gross import fetch_box_office_data


data_frame = pd.DataFrame()
for year in range(2000, 2023, 1):
    print(year)
    base_url = f"https://www.imdb.com/search/title/?release_date={year}-01-01,{year}-12-31&sort=num_votes,desc"
    movies = fetch_all_imdb_movies(base_url, 3000)
    movies = pd.DataFrame(movies)
    movies["year"] = year
    data_frame = pd.concat([data_frame, movies]).reset_index(drop=True)
data_frame.to_csv("movies.csv",index=False)

# data_frame = pd.DataFrame()
# for year in range(2000, 2023, 1):
#     print(year)
#     url = f"https://www.boxofficemojo.com/year/world/{year}/"
#     data = fetch_box_office_data(url)
#     box_office = pd.DataFrame(data)
#     box_office["year"] = year
#     data_frame = pd.concat([data_frame, box_office]).reset_index(drop=True)
# data_frame.to_csv("box_office.csv", index=False)

# data_frame = pd.DataFrame()
# for year in range(2000, 2023, 1):
#     print(year)
#     base_url = f"https://www.imdb.com/search/title/?release_date={year}-01-01,{year}-12-31&sort=boxoffice_gross_us,desc"
#     movies = fetch_all_imdb_gross(base_url, 2000)
#     box_office = pd.DataFrame(movies)
#     data_frame = pd.concat([data_frame, box_office]).reset_index(drop=True)
# data_frame.to_csv("box_office.csv", index=False)
