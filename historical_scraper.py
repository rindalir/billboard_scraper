import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import argparse

def scrape_week_chart(date_str, output_path):
    url = f"https://www.billboard.com/charts/hot-100/{date_str}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch {date_str}: {response.status_code}")
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

            if len(artist) > 1 and not any(x in artist.lower() for x in ['buy', 'new', 'last week']):
                results.append((rank, title, artist))
                rank += 1

        if rank > 100:
            break

    if results:
        with open(output_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Rank", "Title", "Artist"])
            writer.writerows(results)
        print(f"✅ {date_str}: Wrote {len(results)} entries to {output_path}")
    else:
        print(f"⚠️ {date_str}: No results found.")


def daterange(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=7)


def main():
    parser = argparse.ArgumentParser(description="Scrape Billboard Hot 100 charts for a date range")
    parser.add_argument("start_date", help="Start date in YYYY-MM-DD")
    parser.add_argument("end_date", help="End date in YYYY-MM-DD")

    args = parser.parse_args()
    try:
        start = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        end = datetime.strptime(args.end_date, "%Y-%m-%d").date()
    except ValueError:
        print("❌ Error: Dates must be in YYYY-MM-DD format.")
        return

    for date in daterange(start, end):
        date_str = date.strftime("%Y-%m-%d")
        output_file = f"billboard_hot_100_{date_str}.csv"
        scrape_week_chart(date_str, output_file)


if __name__ == "__main__":
    main()
