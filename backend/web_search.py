import requests
from os import getenv
from fastapi import HTTPException

SERP_KEY = getenv("SERPAPI_KEY")

def search_web(query: str):
    if not SERP_KEY:
        raise HTTPException(500, "SERPAPI_KEY not set")
    try:
        url = "https://serpapi.com/search.json"
        params = {"q": query, "api_key": SERP_KEY}
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            raise HTTPException(500, "Web search failed")
        data = resp.json()
        results = []
        for r in data.get("organic_results", []):
            results.append({
                "title": r.get("title"),
                "link": r.get("link"),
                "snippet": r.get("snippet")
            })
        return results
    except Exception as e:
        raise HTTPException(500, f"Web search error: {str(e)}")