import os
import time
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError

# 匯入組員開發的工具與技能
from tools.weather_tool import TOOL as weather_tool_spec, run as run_weather
from tools.search_tool import TOOL as search_tool_spec, run as run_search
from skills.trip_briefing import trip_briefing_skill

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"
MAX_RETRIES = 15

def _make_function_declaration(spec: dict) -> types.FunctionDeclaration:
    return types.FunctionDeclaration(
        name=spec["name"],
        description=spec["description"],
        parameters=spec["parameters"]
    )

# 讓 Agent 知道有哪些工具可用
tools_list = types.Tool(function_declarations=[
    _make_function_declaration(weather_tool_spec),
    _make_function_declaration(search_tool_spec),
])

# 實際執行的函式映射（search_attractions 現在接受 query 參數）
available_functions = {
    "get_weather": run_weather,
    "search_attractions": run_search  # run(query: str)
}

def _call_model(contents, tools_config):
    """呼叫模型，自動處理 429 rate limit 並重試"""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=tools_config
            )
        except ClientError as e:
            if e.status_code == 429:
                # 從錯誤訊息中解析等待秒數
                match = re.search(r'retry in ([\d.]+)s', str(e), re.IGNORECASE)
                wait = float(match.group(1)) + 1 if match else 30
                print(f"⚠️  API 配額限制，等待 {wait:.0f} 秒後重試 ({attempt}/{MAX_RETRIES})...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("已達最大重試次數，API 仍然回傳 429，請稍後再試或檢查 API Key 配額。")

def run_agent(user_prompt):
    config = types.GenerateContentConfig(tools=[tools_list])
    
    # 1. 初始呼叫
    response = _call_model(user_prompt, config)
    part = response.candidates[0].content.parts[0]

    if part.function_call:
        fn_name = part.function_call.name
        fn_args = dict(part.function_call.args)

        # 執行 Tool [cite: 148]
        print(f"--- 系統提示：正在調用工具 {fn_name} ---")
        result = available_functions[fn_name](**fn_args)

        # 2. 建立正確的對話上下文回傳給 LLM
        # 必須包含：原始用戶問題、模型的 function_call、以及工具的 function_response
        history = [
            types.Content(role="user", parts=[types.Part.from_text(text=user_prompt)]),
            types.Content(role="model", parts=[part]),
            types.Content(role="user", parts=[
                types.Part.from_function_response(
                    name=fn_name,
                    response={"result": str(result)} # 確保轉為字串 [cite: 177]
                )
            ]),
        ]
        
        # 取得最終總結回答
        response = _call_model(history, config)

    return response.text

if __name__ == "__main__":
    print("=== 旅遊前哨站 Agent 已啟動 ===")
    while True:
        user_input = input("您想去哪個城市？ (輸入 'exit' 離開): ")
        if user_input.lower() == 'exit': break

        try:
            # 如果使用者明確要求簡報，直接執行 Skill
            if "簡報" in user_input or "規劃" in user_input:
                # 去除「規劃」、「簡報」等字眼，只留下城市名
                city_name = user_input.replace("規劃", "").replace("簡報", "").strip()
                print(trip_briefing_skill(city_name))
            else:
                # 否則進入一般 Agent 自動判斷模式
                answer = run_agent(user_input)
                print(f"Agent 回覆: {answer}")
        except Exception as e:
            print(f"❌ 發生錯誤: {e}")
            print("請稍等片刻再試，或檢查你的 API Key 配額。")
