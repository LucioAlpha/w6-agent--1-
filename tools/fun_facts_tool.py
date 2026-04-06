import requests

def get_travel_fact():
    # 取得隨機冷知識 [cite: 9]
    res = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    return res.json().get('text', "旅行能開闊視野。")

def get_motto():
    # 取得旅遊格言 [cite: 13]
    res = requests.get("https://api.adviceslip.com/advice")
    return res.json().get('slip', {}).get('advice', "Enjoy your trip.")