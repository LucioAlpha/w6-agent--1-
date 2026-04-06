from tools.weather_tool import run as run_weather
from tools.search_tool import run as run_search
from tools.fun_facts_tool import get_travel_fact, get_motto, get_activity

def trip_briefing_skill(city: str):
    """
    整合多個工具，輸出旅遊行前簡報：
    - 天氣（wttr.in）
    - 景點、美食、購物推薦（DuckDuckGo）
    - 活動建議（Bored API）
    - 旅遊知識（Useless Facts）
    - 人生格言（Advice Slip）
    """
    weather     = run_weather(city)
    attractions = run_search(f"{city} 景點")
    food        = run_search(f"{city} 美食")
    shopping    = run_search(f"{city} 購物 推薦")
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