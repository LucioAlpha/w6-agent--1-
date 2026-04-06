import requests

TOOL = {
    "name": "get_weather",
    "description": "查詢目的地的即時天氣資訊",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名稱，例如：Tokyo"}
        },
        "required": ["city"]
    }
}

# weather_tool.py 穩定版
def run(city: str) -> str:
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)
        # 檢查回傳內容是否為 JSON
        if response.status_code == 200 and "application/json" in response.headers.get("Content-Type", ""):
            data = response.json()
            temp = data['current_condition'][0]['temp_C']
            desc = data['current_condition'][0]['weatherDesc'][0]['value']
            return f"{temp}°C, {desc}"
        return "暫時無法取得天氣數據，請稍後再試。"
    except Exception:
        return "天氣服務連線失敗。"