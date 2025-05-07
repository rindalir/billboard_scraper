import requests
from bs4 import BeautifulSoup
import csv

# URL of the Billboard Hot 100 chart
url = 'https://www.billboard.com/charts/hot-100/'

# Send a GET request to the URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all chart entries
chart_entries = soup.find_all('li', class_='o-chart-results-list__item')

# Open a CSV file to write the data
with open('billboard_hot_100.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Rank', 'Song Title', 'Artist'])

    rank = 1
    for entry in chart_entries:
        # Extract song title
        title_tag = entry.find('h3', id='title-of-a-story')
        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            continue  # Skip if title not found

        # Extract artist name
        artist_tag = entry.find('span', class_='c-label')
        if artist_tag:
            artist = artist_tag.get_text(strip=True)
        else:
            artist = 'Unknown'

        # Write the data to CSV
        writer.writerow([rank, title, artist])
        rank += 1
