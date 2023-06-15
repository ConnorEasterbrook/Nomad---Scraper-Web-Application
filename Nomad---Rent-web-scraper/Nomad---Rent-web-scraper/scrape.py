from os import write
import random
import re
import requests
from bs4 import BeautifulSoup
from string_specifier import StringSpecifier

class Scraper:

    def run(self):
       #url = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E91990&maxBedrooms=0&minBedrooms=0&propertyTypes=bungalow%2Cdetached%2Cflat%2Csemi-detached%2Cterraced&mustHave=&dontShow=houseShare%2Cretirement%2Cstudent&furnishTypes=&keywords='
       #url = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E91990&maxBedrooms=1&minBedrooms=1&propertyTypes=bungalow%2Cdetached%2Cflat%2Csemi-detached%2Cterraced&mustHave=&dontShow=houseShare%2Cretirement%2Cstudent&furnishTypes=&keywords='
       
       specifier = StringSpecifier()
       initial_url = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E91990&maxBedrooms=1&minBedrooms=1&propertyTypes=bungalow%2Cdetached%2Cflat%2Csemi-detached%2Cterraced&mustHave=&dontShow=houseShare%2Cretirement%2Cstudent&furnishTypes=&keywords="
       url_array = StringSpecifier.startParsing(specifier, initial_url)
       #print(url_array)

       for i in range(0, 4):
           response = self.fetch(url_array[i])
           self.parse(response.text)

       #response = self.fetch(url)
       #self.parse(response.text)

    def fetch(self, url):
        print("Attempting to fetch URL: " + url + "\n")
        response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        print("Status code: " + str(response.status_code) + "\n")

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
        # There are two ways to go about showcasing average for properties. We get all properties in bulk and assess that way or do four searches for each bedroom count and average independently
        int_prices = []
        for price in prices:
            try:
                tempPrice = re.search(r'\d+', price).group()
                int_prices.append(int(tempPrice))
            except ValueError:
                print("Unable to convert price to integer.")

        listings = []
        for title, price in zip(titles, prices):
            listings.append(f'{title}- {price}')


        output = ", \n".join(listings)
        print(output)
    