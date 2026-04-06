from duckduckgo_search import DDGS

TOOL = {
    "name": "search_attractions",
    "description": "搜尋當地的熱門景點或注意事項",
    "parameters": {
        "city": {"type": "string", "description": "城市名稱"}
    }
}

def run(city: str) -> str:
    query = f"{city} 景點"
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
        if not results: return "找不到相關景點"
        return ", ".join([r['title'] for r in results])