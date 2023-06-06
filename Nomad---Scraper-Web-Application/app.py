"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

from scrape import get_zoopla_data

@app.route('/')
def hello():
    url = "https://www.zoopla.co.uk/to-rent/property/wales/?price_frequency=per_month&q=Wales&results_sort=newest_listings&search_source=to-rent"
    table_data = get_zoopla_data(url)

    for row in table_data:
        print(row)

    """Renders a sample page."""
    return "Hello World!"

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
