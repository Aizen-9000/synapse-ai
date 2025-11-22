import requests
from fastapi import HTTPException
from os import getenv

SERP_KEY = getenv("SERPAPI_KEY")

def search_web(query: str):
    url = f"https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERP_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(500, "Web search failed")

    data = response.json()

    results = []
    for r in data.get("organic_results", []):
        results.append({
            "title": r.get("title"),
            "link": r.get("link"),
            "snippet": r.get("snippet")
        })

    return results