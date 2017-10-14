from urllib.parse import urlencode
import urllib.request
from json import loads

class Geocoding(object):
    """
    More info: https://developers.google.com/maps/documentation/geocoding/
    """
    def __init__(self, api_key):
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
        self.key = api_key

    def build_request_url(self, address):
        params = {"address": address,
                  "key":self.key}
        return self.base_url + urlencode(params)

    def get_location(self, address):
        url = self.build_request_url(address)
        data = urllib.request.urlopen(url)
        return loads(data.read().decode("utf-8"))

    def format_output(self, address):
        r = []
        locs = self.get_location(address)["results"]
        for res in locs:
            name = res["formatted_address"]
            lat = res["geometry"]["location"]["lat"]
            lng = res["geometry"]["location"]["lng"]
            r.append((name, lat, lng))
        return r
