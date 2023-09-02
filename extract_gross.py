from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd

def fetch_box_office_data(url: str):
    """
    Fetch box office data from the given URL.
    
    Parameters:
        url (str): The URL to scrape.
        
    Returns:
        list: A list of dictionaries containing movie data.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to get data. HTTP status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    
    if not table:
        print("No table found.")
        return []
    
    rows = table.find_all('tr')
    data = []
    
    for row in rows[1:]:  # Skip the header row
        cells = row.find_all('td')
        movie_data = {
            'Rank': cells[0].text.strip(),
            'Title': cells[1].text.strip(),
            'Worldwide': cells[2].text.strip(),
            'Domestic': cells[3].text.strip(),
            'Overseas': cells[4].text.strip()
        }
        data.append(movie_data)
        
    return data


# Test the function
if __name__ == "__main__":
    for year in range(2000, 2023, 1):
        print(year)
        url = f"https://www.boxofficemojo.com/year/world/{year}/"
        data = fetch_box_office_data(url)
    box_office = pd.DataFrame(data)
    box_office.to_csv("box_office.csv")
    size_in_bytes = sys.getsizeof(box_office)
    size_in_kilobytes = size_in_bytes / 1024  # Convert to KB