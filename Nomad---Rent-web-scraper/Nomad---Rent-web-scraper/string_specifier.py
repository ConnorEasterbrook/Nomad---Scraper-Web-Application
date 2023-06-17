from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
import json

class StringSpecifier:

    def startParsing(self, url):
        parsed_url = urlparse(url)
        
        # Get array of region-codes.json
        region_codes = self.getRegionCodes()
        search_array = []

        for i in range(0, region_codes.__len__()):
            for j in range(1, 6):
                new_url = self.getPropertySearches(parsed_url, region_codes, i, j)
                search_array.append(new_url)
            
        return search_array

    # Get region codes as follows:
        # Cardiff postcode CF
        # Newport postcode NP
        # Swansea (county of)
        # Carmarthenshire county
        # Pembrokeshire county
        # Ceridigion county
        # Powys county
        # Llandudno postcode LL
        # Chester postcode CH
    def getRegionCodes(self):
        with open('region-codes.json') as json_file:
            data = json.load(json_file)
            return data['region_codes']
            
    def getPropertySearches(self, parsed_url, region_codes, region_iteration, bedroom_iteration):
        region = region_codes[region_iteration]

        location_search = self.specifyLocation(parsed_url, region)
        parsed_location_search = urlparse(location_search)

        bedroom_search = self.specifyBedrooms(parsed_location_search, bedroom_iteration)
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