import requests

def get_travel_fact() -> str:
    # 取得隨機旅遊冷知識
    try:
        res = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random", timeout=5)
        return res.json().get('text', "旅行能開闊視野。")
    except Exception:
        return "旅行能開闊視野。"

def get_motto() -> str:
    # 取得旅遊人生格言
    try:
        res = requests.get("https://api.adviceslip.com/advice", timeout=5)
        return res.json().get('slip', {}).get('advice', "Enjoy your trip.")
    except Exception:
        return "Enjoy your trip."

def get_activity() -> str:
    # 取得隨機活動建議（Bored API）
    try:
        res = requests.get("https://bored-api.appbrewery.com/random", timeout=5)
        data = res.json()
        activity = data.get('activity', '未知活動')
        participants = data.get('participants', 1)
        return f"{activity}（適合 {participants} 人）"
    except Exception:
        return "散步探索當地街道（適合 1 人）"