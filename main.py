import os
from dotenv import load_dotenv
# 假設你使用 Google Gemini 或其他 LLM SDK
import google.generativeai as genai 

# 匯入組員開發的工具與技能
from tools.weather_tool import TOOL as weather_tool_spec, run as run_weather
from tools.search_tool import TOOL as search_tool_spec, run as run_search
from skills.trip_briefing import trip_briefing_skill

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 讓 Agent 知道有哪些工具可用
tools_list = [weather_tool_spec, search_tool_spec]

# 實際執行的函式映射
available_functions = {
    "get_weather": run_weather,
    "search_attractions": run_search
}

def run_agent(user_prompt):
    # 1. 初始呼叫：將問題與工具定義傳給模型
    model = genai.GenerativeModel('gemini-1.5-flash', tools=tools_list)
    chat = model.start_chat()
    response = chat.send_message(user_prompt)
    
    # 2. 判斷是否需要呼叫工具 (Tool Use)
    if response.candidates[0].content.parts[0].function_call:
        fn_call = response.candidates[0].content.parts[0].function_call
        fn_name = fn_call.name
        fn_args = fn_call.args
        
        # 執行對應的 Tool 函式 [cite: 150]
        print(f"--- 系統提示：正在調用工具 {fn_name} ---")
        result = available_functions[fn_name](**fn_args)
        
        # 3. 將工具結果傳回模型進行總結 
        response = chat.send_message(result)
    
    return response.text

if __name__ == "__main__":
    print("=== 旅遊前哨站 Agent 已啟動 ===")
    while True:
        user_input = input("您想去哪個城市？ (輸入 'exit' 離開): ")
        if user_input.lower() == 'exit': break
        
        # 如果使用者明確要求簡報，直接執行 Skill [cite: 135, 205]
        if "簡報" in user_input or "規劃" in user_input:
            # 解析出城市名稱後呼叫 Skill
            print(trip_briefing_skill(user_input)) 
        else:
            # 否則進入一般 Agent 自動判斷模式 [cite: 140]
            answer = run_agent(user_input)
            print(f"Agent 回覆: {answer}")