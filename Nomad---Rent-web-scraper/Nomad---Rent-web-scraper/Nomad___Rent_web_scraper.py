from scrape import Scraper

# Plan:
# 1. Create a class that will be used to scrape the website.
# 2. Create a JSON file that features all search areas and bedroom count.
# 3. Create a function that will loop through the data, modifying the URL where needed, and then scrape the data.
# 4. Create a function that will calculate the average price for each search area and bedroom count, disregarding outliers.
# 5. Create a front end with an API that will display the data in map format.
# 6. Allow for user input to change the bedroom count.
# 7. Deploy to either GitHub Pages or Netlify.

if __name__ == '__main__':
    scraper = Scraper()
    scraper.run()