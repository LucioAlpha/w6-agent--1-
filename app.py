"""
app.py — 旅遊前哨站 Agent Web Server
提供 dashboard.html，並透過 /api/chat 端點與 Agent 互動。
"""
import os
import time
import re
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError

# 匯入工具與技能
from tools.weather_tool import TOOL as weather_tool_spec, run as run_weather
from tools.search_tool import TOOL as search_tool_spec, run as run_search
from skills.trip_briefing import trip_briefing_skill

# ── 初始化 ──────────────────────────────────────────
load_dotenv()
app = Flask(__name__, static_folder=".", static_url_path="")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME  = "gemini-2.5-flash"
MAX_RETRIES = 15

def _make_function_declaration(spec: dict) -> types.FunctionDeclaration:
    return types.FunctionDeclaration(
        name=spec["name"],
        description=spec["description"],
        parameters=spec["parameters"]
    )

tools_list = types.Tool(function_declarations=[
    _make_function_declaration(weather_tool_spec),
    _make_function_declaration(search_tool_spec),
])

available_functions = {
    "get_weather":       run_weather,
    "search_attractions": run_search,
}

# ── Agent 核心邏輯（與 main.py 相同） ────────────────
def _call_model(contents, config):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=config
            )
        except ClientError as e:
            if e.status_code == 429:
                match = re.search(r'retry in ([\d.]+)s', str(e), re.IGNORECASE)
                wait = float(match.group(1)) + 1 if match else 30
                print(f"⚠️  {wait:.0f}s 後重試 ({attempt}/{MAX_RETRIES})")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("已達最大重試次數，請稍後再試。")

def run_agent(user_prompt: str) -> str:
    config = types.GenerateContentConfig(tools=[tools_list])
    response = _call_model(user_prompt, config)
    part = response.candidates[0].content.parts[0]

    if part.function_call:
        fn_name = part.function_call.name
        fn_args = dict(part.function_call.args)
        print(f"[Tool] {fn_name}({fn_args})")
        result = available_functions[fn_name](**fn_args)

        history = [
            types.Content(role="user",  parts=[types.Part.from_text(text=user_prompt)]),
            types.Content(role="model", parts=[part]),
            types.Content(role="user",  parts=[
                types.Part.from_function_response(
                    name=fn_name,
                    response={"result": str(result)}
                )
            ]),
        ]
        response = _call_model(history, config)

    return response.text

# ── Flask 路由 ────────────────────────────────────────
@app.route("/")
def index():
    """提供 dashboard.html"""
    return send_from_directory(".", "dashboard.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    接受 POST {"message": "..."} 
    回傳 {"reply": "...", "type": "briefing"|"agent"}
    """
    data = request.get_json(force=True)
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "訊息不能為空"}), 400

    try:
        # 判斷是否要執行行前簡報 Skill
        if "簡報" in message or "規劃" in message:
            city = message.replace("規劃", "").replace("簡報", "").strip()
            reply = trip_briefing_skill(city)
            return jsonify({"reply": reply, "type": "briefing"})
        else:
            reply = run_agent(message)
            return jsonify({"reply": reply, "type": "agent"})

    except Exception as e:
        print(f"[Error] {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("[INFO] Agent server starting...")
    print("[INFO] Open http://localhost:5000 in your browser")
    app.run(debug=False, host="0.0.0.0", port=5000)
