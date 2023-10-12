import requests
from bs4 import BeautifulSoup
import json

def scrape_details(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')
    details = {"page_name": soup.select_one(".adPage__header h1").text.strip(),
               "surface": soup.select_one("div.adPage__content__features__col.grid_9.suffix_1 ul li:nth-child(1) span.adPage__content__features__value").text.strip(),
               "floor": soup.select_one("div.adPage__content__inner div:nth-child(5) div.adPage__content__features__col.grid_9.suffix_1 ul li:nth-child(2) span.adPage__content__features__value").text.strip(),
               "max_floors": soup.select_one("div.adPage__content__inner div:nth-child(5) div.adPage__content__features__col.grid_9.suffix_1 ul li:nth-child(3) span.adPage__content__features__value").text.strip(),
               "rooms": soup.select_one("div.adPage__content__inner div:nth-child(5) div.adPage__content__features__col.grid_9.suffix_1 ul li:nth-child(4) span.adPage__content__features__value").text.strip(),
               "author": soup.select_one("div.adPage__content__inner div:nth-child(5) div.adPage__content__features__col.grid_9.suffix_1 ul li:nth-child(5)").text.strip()}
    return details

urls = ["https://999.md/ro/83963056"]
FILENAME = "info.json"
detail_list = []

for url in urls:
    details = scrape_details(url)
    detail_list.append(details)

with open(FILENAME, "w", encoding="utf-8") as file:
    json.dump(detail_list, file, indent=4, ensure_ascii=False)