import requests
from bs4 import BeautifulSoup

def get_top_touchdown_leaders():
    url = 'https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/all/'

    # Send GET request to fetch the HTML content
    response = requests.get(url)
    response.raise_for_status()

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the table
    stats_table = soup.find('table', class_='TableBase-table')

    if not stats_table:
        print("Could not find the stats table on the page.")
        return

    # Extract header names
    headers = [th.get_text(strip=True) for th in stats_table.find_all('th')]
    print("Detected column headers:", headers)  # Optional debug line

    # Extract all rows from the body
    rows = stats_table.find('tbody').find_all('tr')

    player_stats = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 8:
            continue  # Skip if row is incomplete

        # Extract raw player/team string and split it
        player_team = cols[0].get_text(strip=True).split('•')
        player_name = player_team[0].strip()
        team = player_team[1].strip() if len(player_team) > 1 else 'N/A'

        # Extract position and touchdown types
        try:
            rushing = int(cols[2].text.strip())
            receiving = int(cols[3].text.strip())
            pr = int(cols[4].text.strip())
            kr = int(cols[5].text.strip())
            intr = int(cols[6].text.strip())
            fumr = int(cols[7].text.strip())
        except ValueError:
            continue  # skip rows with invalid data

        total_tds = rushing + receiving + pr + kr + intr + fumr

        player_stats.append({
            'name': player_name,
            'team': team,
            'total_tds': total_tds
        })

    # Sort players by total_tds descending
    top_players = sorted(player_stats, key=lambda x: x['total_tds'], reverse=True)[:20]

    print("\nTop 20 NFL Touchdown Leaders (Regular Season):")
    print("=" * 50)
    for idx, player in enumerate(top_players, start=1):
        print(f"{idx}. {player['name']} | {player['team']} | Total Touchdowns: {player['total_tds']}")

if __name__ == "__main__":
    get_top_touchdown_leaders()