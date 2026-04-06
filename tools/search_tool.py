from duckduckgo_search import DDGS

TOOL = {
    "name": "search_attractions",
    "description": "使用 DuckDuckGo 搜尋旅遊相關資訊，例如景點、美食、購物推薦等",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜尋關鍵字，例如：'Tokyo 景點'、'Taipei 美食'、'Paris 購物 推薦'"}
        },
        "required": ["query"]
    }
}

def run(query: str) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
        if not results: return "找不到相關資訊"
        return ", ".join([r['title'] for r in results])
