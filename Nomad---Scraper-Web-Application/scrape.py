"""
This script scrapes the Zoopla website for the latest rental properties in Wales.
"""

import requests
from bs4 import BeautifulSoup

def get_zoopla_data(url):
    zoopla_get = requests.get(url)
    zoopla_get_bsobj = BeautifulSoup(zoopla_get.content, "lxml")

    scrape_table_data = []
    for i in zoopla_get_bsobj.findAll("div", {"class": "listing-results-right clearfix"}):
        scrape_table_data.append(i.a.text.strip())

    return scrape_table_data
