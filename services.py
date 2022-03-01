import requests


def get_countries_from_github(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
