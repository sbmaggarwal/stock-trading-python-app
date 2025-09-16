"""Small module to fetch tickers from Polygon API.

Provides a single function `fetch_tickers(api_key, **kwargs)` that returns the
requests.Response object. This keeps HTTP logic separate from CSV/IO logic.
"""
from typing import Any
import requests


def fetch_tickers(api_key: str, market: str = "stocks", active: str = "true",
                  order: str = "asc", limit: int = 100, sort: str = "ticker") -> requests.Response:
    """Fetch tickers from Polygon and return the Response object.

    The caller is responsible for checking status code and parsing JSON.
    """
    base_url = "https://api.polygon.io/v3/reference/tickers"
    params = {
        "market": market,
        "active": active,
        "order": order,
        "limit": str(limit),
        "sort": sort,
        "apiKey": api_key,
    }

    return requests.get(base_url, params=params)
