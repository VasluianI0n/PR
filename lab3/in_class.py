import requests
import bs4
from bs4 import BeautifulSoup



class  scraperTreiDivetci:
    def __init__(self):
        self.url = "https://999.md/ru/list/real-estate/apartments-and-rooms?o_30_241=894&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776?page={}"
        self.url_list = []
        self.page_max = 13
        self.file_name = "urls.txt"

    def scrape(self, page_number = 1):
        return self.get_urls(page_number)
    
    def get_urls(self, page_number):
        if self.page_max < page_number:
            return
        
        url = self.url.format(page_number)
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'lxml')
            
            for url in soup.select(".ads-list-photo-item-title a"):
                href = url.get('href')
                if href and "/booster" not in href:
                    self.url_list.append("https://999.md" + href)
            self.get_urls(page_number+1)
                
        self.save_urls()
            
            

    def save_urls(self):
        with open(self.file_name, "w") as file:
            for url in self.url_list:
                file.write(url + "\n")

def main():
    scraper = scraperTreiDivetci()
    scraper.scrape()

if __name__ == "__main__":
    main()