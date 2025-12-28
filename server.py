import threading              # 用於背景執行（自動開瀏覽器）
import webbrowser             # 控制系統瀏覽器
import time

from flask import Flask, request, jsonify, render_template
import requests
import PyPDF2                 # PDF 文字擷取套件

# Flask App 初始化
app = Flask(__name__)

# LLM API 設定
LLM_URL = "https://api-gateway.netdb.csie.ncku.edu.tw/api/chat"
API_KEY = "49ffb0933f3932bb3c3b675f0e9cb9be39b45b635d0feeba44ad9f4eb51fd70f"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# PDF 限制
MAX_PDF_PAGES = 300
MAX_TEXT_LENGTH = 100000

# 對話歷史紀錄
conversation_history = []

# System Prompt
SYSTEM_PROMPT = "你是一個專業的學習助理，請使用繁體中文回答。"

# 自動開瀏覽器
def open_browser():
    time.sleep(1)    # Flask 啟動後延遲 1 秒，自動打開瀏覽器
    webbrowser.open("http://127.0.0.1:5000")

# Routes
# 首頁
@app.route("/")
def index():
    return render_template("index.html")

# 清空對話紀錄
@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "ok"})

# 一般聊天模式
@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history

    data = request.json
    user_msg = data.get("message", "")

    # 若是第一輪對話，先放入 system prompt
    if not conversation_history:
        conversation_history.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })

    # 加入使用者訊息
    conversation_history.append({
        "role": "user",
        "content": user_msg
    })

    # LLM API payload
    payload = {
        "model": "gemma3:4b",
        "messages": conversation_history,
        "stream": False
    }

    # 呼叫 LLM API
    try:
        r = requests.post(LLM_URL, json=payload, headers=HEADERS, timeout=30)
        r.raise_for_status()
        result = r.json()
        print("LLM Response:", result)

        # 解析不同可能的回傳格式
        assistant_msg = ""
        if "message" in result and "content" in result["message"]:
            assistant_msg = result["message"]["content"]
        elif "choices" in result and len(result["choices"]) > 0:
            assistant_msg = result["choices"][0].get("message", {}).get("content", "")
        else:
            assistant_msg = "LLM 回傳格式不正確"

        # 將 assistant 回覆存入歷史紀錄
        conversation_history.append({
            "role": "assistant",
            "content": assistant_msg
        })

        # 回傳給前端
        return jsonify({"reply": assistant_msg})

    # API錯誤處理
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# PDF學習模式
@app.route("/pdf_chat", methods=["POST"])
def pdf_chat():
    global conversation_history

    # 取得表單參數
    task = request.form.get("task")        # summary | quiz
    quiz_type = request.form.get("quiz")   # mcq | qa | mixed
    pdf_file = request.files.get("pdf")

    print("Received PDF task:", task, "quiz_type:", quiz_type)

    # 檢查是否有上傳PDF
    if not pdf_file:
        return jsonify({"error": "No PDF uploaded"}), 400

    # 嘗試讀取PDF
    try:
        reader = PyPDF2.PdfReader(pdf_file)
    except Exception:
        return jsonify({"error": "Invalid PDF"}), 400

    if len(reader.pages) > MAX_PDF_PAGES:
        return jsonify({"error": "PDF pages exceed limit"}), 400

    pages_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages_text.append(f"[Page {i+1}]\n{text}")

    full_text = "\n".join(pages_text)[:MAX_TEXT_LENGTH]

    if not full_text.strip():
        return jsonify({"error": "PDF 無法提取文字"}), 400

    # 初始化system prompt
    if not conversation_history:
        conversation_history.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })

    # 根據任務生成prompt
    if task == "summary":
        prompt = f"""
以下是 PDF 講義內容，請統整全文重點。
請使用條列式。

{full_text}
"""
    else:  # quiz
        if quiz_type == "mcq":
            quiz_prompt = "請依據以下內容出 5 題單選題（A/B/C/D），每題附正確答案與解析"
        elif quiz_type == "qa":
            quiz_prompt = "請依據以下內容出 5 題問答題，每題附標準答案"
        else:
            quiz_prompt = "請依據以下內容出 3 題單選題 + 2 題問答題，每題附答案"

        prompt = f"""
以下是課堂講義內容：
{full_text}

{quiz_prompt}
請以清楚編號格式列出每一題。
"""

    # 將PDF prompt當作user訊息送出
    conversation_history.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "model": "gemma3:4b",
        "messages": conversation_history,
        "stream": False
    }

    try:
        r = requests.post(LLM_URL, json=payload, headers=HEADERS, timeout=60)
        r.raise_for_status()
        result = r.json()
        print("LLM PDF Response:", result)

        assistant_msg = ""
        if "message" in result and "content" in result["message"]:
            assistant_msg = result["message"]["content"]
        elif "choices" in result and len(result["choices"]) > 0:
            assistant_msg = result["choices"][0].get("message", {}).get("content", "")
        else:
            assistant_msg = "LLM 回傳格式不正確"

        conversation_history.append({
            "role": "assistant",
            "content": assistant_msg
        })

        return jsonify({
            "pages": len(reader.pages),
            "reply": assistant_msg
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# Main
if __name__ == "__main__":
    threading.Thread(target=open_browser).start()      # 背景執行自動開瀏覽器
    app.run(host="127.0.0.1", port=5000, debug=False)  # 啟動Flask Server





