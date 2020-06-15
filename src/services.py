import os
import requests
from flask import current_app as app


def get_json_from_goodreads(isbn):
    GOODREAD_API_KEY = os.getenv("GOODREAD_API_KEY")
    if not GOODREAD_API_KEY:
        raise RuntimeError("GOODREAD_API_KEY is not set")
    GOODREAD_API_URL = app.config["GOODREAD_API_URL"]
    res = requests.get(
        GOODREAD_API_URL, params={"key": GOODREAD_API_KEY, "isbns": isbn}
    )
    return res.json()

