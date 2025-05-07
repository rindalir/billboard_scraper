import requests
from bs4 import BeautifulSoup
import csv

def scrape_billboard_chart(date_str, output_csv='billboard_hot_100.csv'):
    url = f"https://www.billboard.com/charts/hot-100/{date_str}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    chart_items = soup.select('li.o-chart-results-list__item')

    results = []
    rank = 1

    for item in chart_items:
        title_tag = item.find('h3', id='title-of-a-story')
        artist_tag = item.find('span', class_='c-label')

        if title_tag and artist_tag:
            title = title_tag.get_text(strip=True)
            artist = artist_tag.get_text(strip=True)

            # Sanity check: skip items like 'Buy', 'New', or blank
            if len(artist) > 1 and not any(x in artist.lower() for x in ['buy', 'new', 'last week']):
                results.append((rank, title, artist))
                rank += 1

        if rank > 100:
            break

    with open(output_csv, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Title', 'Artist'])
        writer.writerows(results)

    print(f"Wrote {len(results)} songs to {output_csv}")

# Example usage
scrape_billboard_chart('2025-03-01')
