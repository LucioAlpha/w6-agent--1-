from tools.weather_tool import run as run_weather
from tools.search_tool import run as run_search
from tools.fun_facts_tool import get_travel_fact, get_motto

def trip_briefing_skill(city: str):
    """
    Step 1: 呼叫 get_weather 取得天氣資訊 [cite: 215]
    Step 2: 呼叫 search_attractions 搜尋熱門景點
    Step 3: 呼叫 fun_facts 取得冷知識與格言
    Step 4: 整合輸出「行前簡報」 [cite: 15, 217]
    """
    weather = run_weather(city)
    attractions = run_search(city)
    fact = get_travel_fact()
    motto = get_motto()
    
    # 依照範例格式輸出 [cite: 17]
    report = f"=== {city} 行前簡報 ===\n"
    report += f"[天氣] {weather}\n"
    report += f"[景點] {attractions}\n"
    report += f"[知識] {fact}\n"
    report += f"[格言] {motto}"
    return report