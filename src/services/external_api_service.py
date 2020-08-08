import requests


class ExternalApiService:
    def __init__(self, api_url, api_key):
        self._GOODREAD_API_URL = api_url
        self._GOODREAD_API_KEY = api_key

    def get_json_from_goodreads(self, isbn):
        res = requests.get(
            self._GOODREAD_API_URL, params={"key": self._GOODREAD_API_KEY, "isbns": isbn}
        )
        return res.json()
