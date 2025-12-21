import threading
import webbrowser
import time

from flask import Flask, request, jsonify, render_template
import requests
import PyPDF2

app = Flask(__name__)

# =========================
# LLM API 設定
# =========================
LLM_URL = "https://api-gateway.netdb.csie.ncku.edu.tw/api/chat"
API_KEY = "49ffb0933f3932bb3c3b675f0e9cb9be39b45b635d0feeba44ad9f4eb51fd70f"

# =========================
# PDF 限制（設計考量）
# =========================
MAX_PDF_PAGES = 300
MAX_TEXT_LENGTH = 5000


# =========================
# 自動開瀏覽器（exe 用）
# =========================
def open_browser():
    time.sleep(1)  # 等 Flask 起來
    webbrowser.open("http://127.0.0.1:5000")


# =========================
# Routes
# =========================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    payload = {
        "model": "gemma3:4b",
        "messages": [
            {"role": "system", "content": "You are a helpful study agent."},
            {"role": "user", "content": user_msg}
        ],
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(LLM_URL, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        return jsonify(r.json())
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "API request failed",
            "detail": str(e)
        }), 500


@app.route("/pdf_chat", methods=["POST"])
def pdf_chat():
    task = request.form.get("task")        # summary | quiz
    mode = request.form.get("mode")        # overall | per_page
    quiz_type = request.form.get("quiz")   # mcq | qa | mixed
    pdf_file = request.files.get("pdf")

    if not pdf_file:
        return jsonify({"error": "No PDF uploaded"}), 400

    try:
        reader = PyPDF2.PdfReader(pdf_file)
    except Exception:
        return jsonify({"error": "Invalid PDF file"}), 400

    num_pages = len(reader.pages)

    if num_pages > MAX_PDF_PAGES:
        return jsonify({
            "error": f"PDF 超過頁數限制（最多 {MAX_PDF_PAGES} 頁）"
        }), 400

    pages_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages_text.append(f"[Page {i + 1}]\n{text}")

    full_text = "\n".join(pages_text)
    full_text = full_text[:MAX_TEXT_LENGTH]

    # =========================
    # Prompt Engineering
    # =========================
    if task == "summary":
        if mode == "per_page":
            prompt = f"""
以下是 PDF 講義內容，請「每一頁各自摘要重點」。
請用條列式，並清楚標示頁碼。

{full_text}
"""
        else:
            prompt = f"""
以下是 PDF 講義內容，請統整全文重點。
請使用條列式，並在每點後標註來源頁碼。

{full_text}
"""
    else:
        if quiz_type == "mcq":
            quiz_prompt = "請出 5 題單選題（A/B/C/D），並附答案與解析"
        elif quiz_type == "qa":
            quiz_prompt = "請出 5 題問答題，並附標準答案"
        else:
            quiz_prompt = "請出 3 題單選題 + 2 題問答題，並附答案"

        prompt = f"""
以下是課堂講義內容，
{quiz_prompt}
請在每一題後標註該題來自的頁碼。

{full_text}
"""

    payload = {
        "model": "gemma3:4b",
        "messages": [
            {"role": "system", "content": "You are a professional study assistant."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(LLM_URL, json=payload, headers=headers, timeout=60)
        r.raise_for_status()

        return jsonify({
            "pages": num_pages,
            "result": r.json()
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "API request failed",
            "detail": str(e)
        }), 500


# =========================
# Main（exe 入口）
# =========================
if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)





