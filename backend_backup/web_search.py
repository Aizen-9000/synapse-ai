import httpx
from bs4 import BeautifulSoup

async def search_web(query: str, max_results: int = 3) -> str:
    """
    Perform a simple web search using DuckDuckGo (no API key required).
    Returns summarized top N URLs + snippet.
    """
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for a in soup.find_all("a", {"class": "result__a"}, limit=max_results):
            link = a.get("href")
            text = a.get_text()
            results.append(f"{text}: {link}")
        return "\n".join(results) if results else "[No results found]"
    except Exception as e:
        return f"[Search Error] {e}"