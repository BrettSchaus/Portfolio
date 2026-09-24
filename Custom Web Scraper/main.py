import requests
from bs4 import BeautifulSoup
import csv
import re


audible_URL = "https://www.audible.it/charts?searchLanguage=english&page=0"
header = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:152.0) Gecko/20100101 Firefox/152.0",
}

response = requests.get(audible_URL, headers=header, allow_redirects=False)


soup = BeautifulSoup(response.content, "html.parser")
# print(soup.prettify())


# Find the HTML element that contains the book title
# Find each audiobook
book_data = []
seen = set()

for item in soup.find_all("li", class_="bc-list-item"):

    title_element = item.find("h3")

    if title_element:
        text = title_element.get_text(" ", strip=True)

        match = re.match(r"^(\d+)\.\s*(.*)", text)

        if match:
            ranking = match.group(1)
            title = match.group(2)

            # Prevent duplicate books
            key = (ranking, title)

            if key not in seen:
                seen.add(key)

                book_data.append({
                    "Title": title,
                    "Ranking": ranking
                })

# Print results
print(book_data[:20])

with open("Custom_Web_Scraper_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Title", "Ranking"]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(book_data)