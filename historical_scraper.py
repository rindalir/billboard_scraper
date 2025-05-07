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

    soup = BeautifulSoup(response.text, "html.parser")

    # Each song entry
    chart_items = soup.select("li.o-chart-results-list__item > h3")
    artist_spans = soup.select("li.o-chart-results-list__item > span.c-label")

    songs = []
    for i in range(100):
        try:
            title = chart_items[i].get_text(strip=True)
            # Billboard uses multiple span.c-labels, artist is usually at index 1 or 2
            artist = artist_spans[i * 4 + 1].get_text(strip=True)
            songs.append((i + 1, title, artist))
        except IndexError:
            break  # Page may not be fully populated or layout has shifted

    # Save to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Title", "Artist"])
        writer.writerows(songs)

    print(f"Scraped {len(songs)} songs to {output_csv}")

# Example usage
scrape_billboard_chart("2025-03-01")
