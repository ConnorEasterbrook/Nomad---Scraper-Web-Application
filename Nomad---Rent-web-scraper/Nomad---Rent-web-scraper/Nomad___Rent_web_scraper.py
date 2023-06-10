from os import write
import random
import re
import requests
from bs4 import BeautifulSoup

class ZooplaScraper:

    def run(self):
       url = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E91990&propertyTypes=bungalow%2Cdetached%2Cflat%2Csemi-detached%2Cterraced&mustHave=&dontShow=houseShare%2Cretirement%2Cstudent&furnishTypes=&keywords='
       response = self.fetch(url)

       html = ''
       with open('rightmove.html', 'r', encoding='utf-8') as html_file:
            for line in html_file:
                html += html_file.read()

       self.parse(html)

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        print('HTTP GET request to URL: %s' % url, end='')
        response = requests.get(url, headers = headers)
        print(' | Status code: %s' % response.status_code)

        return response

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml') 
        titles = [title.text.replace('\n', '').replace(' ', '') for title in content.select( ".propertyCard-title")]

        # Get and clean listing information for each property so we can show it
        titles = [title.text for title in content.select( ".propertyCard-title")]
        titles = [title.replace('\n', '') for title in titles]
        titles = [re.sub(r'\s+', ' ', title) for title in titles]
        titles = [title.replace('  ', '') for title in titles]
        prices = [price.text for price in content.select(".propertyCard-priceValue")]

        # Get the integer value of the price for each property so we can calculate with it
        intPrices = []
        for price in prices:
            try:
                tempPrice = re.search(r'\d+', price).group()
                intPrices.append(int(tempPrice))
            except ValueError:
                print("Unable to convert price to integer.")

        listings = []

        for title, price in zip(titles, prices):
            listings.append(f'{title}- {price}')


        output = ",".join(listings)
        print(output)

    
if __name__ == '__main__':
    scraper = ZooplaScraper()
    scraper.run()