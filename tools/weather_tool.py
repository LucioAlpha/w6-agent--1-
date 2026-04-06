import requests

TOOL = {
    "name": "get_weather",
    "description": "查詢目的地的即時天氣資訊",
    "parameters": {
        "city": {"type": "string", "description": "城市名稱，例如：Tokyo"}
    }
}

def run(city: str) -> str:
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        data = response.json()
        temp = data['current_condition'][0]['temp_C']
        desc = data['current_condition'][0]['weatherDesc'][0]['value']
        return f"{temp}°C, {desc}"
    except Exception as e:
        return f"天氣資訊查詢失敗: {e}"