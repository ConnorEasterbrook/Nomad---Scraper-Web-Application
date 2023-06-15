from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

class StringSpecifier:

    def startParsing(self, url):
        parsed_url = urlparse(url)
        
        search_array = []

        for i in range(1, 6):
            new_url = self.getPropertySearches(parsed_url, i)
            search_array.append(new_url)
            
        return search_array
            
    def getPropertySearches(self, parsed_url, iteration):
        location_search = self.specifyLocation(parsed_url, "REGION%5E91990")
        parsed_location_search = urlparse(location_search)

        bedroom_search = self.specifyBedrooms(parsed_location_search, iteration)
        return bedroom_search

    def specifyLocation(self, parsed_url, location = ""):
        query_params = parse_qs(parsed_url.query)

        if location:
            query_params['locationIdentifier'] = location

        # Manually reconstruct the URL with the new query string to avoid encoding issues
        query_string = '&'.join('{}={}'.format(k, v) for k, v in query_params.items())

        return urlunparse(
            (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, query_string, parsed_url.fragment)
        )

    def specifyBedrooms(self, parsed_url, bedrooms = ""):
        query_params = parse_qs(parsed_url.query)

        if bedrooms:
            query_params['maxBedrooms'] = bedrooms
            query_params['minBedrooms'] = bedrooms

        return urlunparse(
            (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, urlencode(query_params, doseq=True), parsed_url.fragment)
        )