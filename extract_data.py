from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd

def fetch_all_imdb_movies(base_url: str) -> List[Dict[str, Optional[str]]]:
    """
    Fetches all movies from IMDb based on the given URL until the last page is reached.
    
    Parameters:
    - base_url (str): The IMDb URL to scrape.
    
    Returns:
    - List[Dict[str, Optional[str]]]: A list of dictionaries containing movie details.
    
    Example:
    >>> fetch_all_imdb_movies("https://www.imdb.com/search/title/?release_date=2022-01-01,2022-12-31&sort=num_votes,desc")
    [{'title': 'Movie1', 'audience_rating': '8.5', 'genre': 'Action', 'critic_rating': '67', 'runtime': '120 min', 'votes': '200K'}, ...]
    """
    # Initialize an empty list to store the movie details
    movies = []
    start_index = 1
    
    while True:
        # Update the URL to fetch the next page
        url = f"{base_url}&start={start_index}"
        
        # Fetch the IMDb page content
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch the IMDb page starting at index {start_index}.")
            break
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the movie containers
        movie_containers = soup.find_all('div', class_='lister-item mode-advanced')
        if not movie_containers:
            print("No more movies found. Exiting.")
            break
        
        # Loop through each movie container to extract details
        for container in movie_containers:
            # Initialize a dictionary to store details of each movie
            movie_details = {}
            
            # Extract movie title
            movie_details['title'] = container.h3.a.text
            
            # Extract audience rating
            movie_details['audience_rating'] = container.strong.text if container.strong else 'N/A'
            
            # Extract genre
            genre = container.find('span', class_='genre')
            movie_details['genre'] = genre.text.strip() if genre else 'N/A'
            
            # Extract critic rating (Metascore)
            metascore = container.find('span', class_='metascore')
            movie_details['critic_rating'] = metascore.text.strip() if metascore else 'N/A'
            
            # Extract runtime
            runtime = container.find('span', class_='runtime')
            movie_details['runtime'] = runtime.text if runtime else 'N/A'
            
            # Extract votes
            votes = container.find('span', attrs={'name': 'nv'})
            movie_details['votes'] = votes['data-value'] if votes else 'N/A'
            
            # Append the movie details to the list
            movies.append(movie_details)
        
        # Check for the "Next" button to see if there are more pages
        next_button = soup.find('a', {'class': 'lister-page-next next-page'})
        if not next_button:
            print("Reached the last page. Exiting.")
            break
        
        # Update the start index for the next page (IMDb usually shows 50 movies per page)
        start_index += 50
    
    return movies

# Test the function
if __name__ == "__main__":
    for year in range(2015, 2023, 1):
        print(year)
        base_url = f"https://www.imdb.com/search/title/?release_date={year}-01-01,{year}-12-31&sort=num_votes,desc"
        movies = fetch_all_imdb_movies(base_url)
    movies = pd.DataFrame(movies)
    movies.to_csv("movies.csv")
    size_in_bytes = sys.getsizeof(movies)
    size_in_kilobytes = size_in_bytes / 1024  # Convert to KB

    print(f"Size of movies list in bytes: {size_in_bytes}")
    print(f"Size of movies list in KB: {size_in_kilobytes}")