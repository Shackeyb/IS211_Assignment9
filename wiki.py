import requests
from bs4 import BeautifulSoup

def scrape_superbowl_champions():
    url = 'https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions'

    # Send GET request to fetch the HTML content
    response = requests.get(url)
    response.raise_for_status()

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table that contains the Super Bowl champions data
    table = soup.find('table', {'class': 'wikitable'})

    if not table:
        print("Could not find the Super Bowl champions table.")
        return

    # Extract all the rows from the table (skip the header row)
    rows = table.find_all('tr')[1:]  # Skip the header row

    print(f"Super Bowl Number | Year | Winning Team | Losing Team | Final Score")
    print("=" * 80)

    for row in rows:
        cols = row.find_all('td')

        # Check if the row has enough columns before extracting
        if len(cols) > 4:
            superbowl_number = cols[0].text.strip()
            year = cols[1].text.strip()
            winning_team = cols[2].text.strip()
            losing_team = cols[3].text.strip()
            final_score = cols[4].text.strip()

            print(f"{superbowl_number} | {year} | {winning_team} | {losing_team} | {final_score}")
        else:
            print(f"Skipping incomplete row: {row.text.strip()}")

if __name__ == "__main__":
    scrape_superbowl_champions()