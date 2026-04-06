from tools.weather_tool import run as run_weather
from tools.search_tool import run as run_search
from tools.fun_facts_tool import get_travel_fact, get_motto, get_activity

# trip_briefing.py 建議微調
def trip_briefing_skill(city: str):
    # 確保傳入的 city 不包含 "規劃" 或 "簡報"
    clean_city = city.replace("規劃", "").replace("簡報", "").strip()
    
    weather     = run_weather(clean_city)
    # 搜尋時手動加上主題關鍵字，這是主題 A 的核心要求 [cite: 115, 120]
    attractions = run_search(f"{clean_city} 景點")
    food        = run_search(f"{clean_city} 必吃美食")
    shopping    = run_search(f"{clean_city} 購物 推薦")
    activity    = get_activity()
    fact        = get_travel_fact()
    motto       = get_motto()

    report  = f"=== {city} 行前簡報 ===\n"
    report += f"[天氣] {weather}\n"
    report += f"[景點] {attractions}\n"
    report += f"[美食] {food}\n"
    report += f"[購物] {shopping}\n"
    report += f"[活動] {activity}\n"
    report += f"[知識] {fact}\n"
    report += f"[格言] {motto}"
    return report