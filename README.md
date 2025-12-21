# Study Agent – PDF-based AI Study Assistant

## 一、簡介

**Study Agent** 是一個基於 Large Language Model（LLM）的學習輔助系統，結合 Flask 後端與 Web 前端，提供：

* 一般即時學習問答（Chat Agent）
* PDF 文件上傳後的分析（摘要 / 自動出題）

本系統特別設計用於 **課堂講義理解、考前複習、自主學習** 等情境。

---

## 二、系統功能

### 1. 一般學習問答

* 使用者可直接輸入問題
* 系統透過 LLM 即時回覆
* 適合概念釐清與即時提問

### 2. PDF 學習輔助（核心功能）

####  PDF 上傳限制

* 最多 **300 頁 PDF**
* 最多擷取 **5000 字文字內容**（避免模型負擔過重）

####  摘要功能

* **全文重點摘要**（條列式，含頁碼）
* **每一頁重點摘要**（逐頁整理）

####  自動出考題

* 單選題（含選項、答案與解析）
* 問答題（含標準答案）
* 混合題型（單選 + 問答）
* 每一題皆標示對應頁碼

---

## 三、系統架構

```
Browser (HTML / JavaScript)
        ↓
Flask Backend (Python)
        ↓
PDF Parser (PyPDF2)
        ↓
LLM API (Gemma Model)
```

---

## 四、技術說明

###  使用技術

* **前端**：HTML, JavaScript
* **後端**：Flask (Python)
* **PDF 解析**：PyPDF2
* **LLM 模型**：Gemma 3 (4B)
* **API 呼叫**：RESTful API

###  Prompt Engineering

系統根據使用者選擇的功能（摘要 / 出題），動態產生不同 Prompt，例如：

* 摘要模式：要求條列重點並標示頁碼
* 出題模式：限制題型、數量並附答案

此設計能有效引導模型產出結構化且符合學習需求的內容。

---

## 五、專案結構

```
study-agent/
│
├─ server.py              # Flask 後端主程式
├─ templates/
│   └─ index.html         # 前端介面
├─ static/
│   └─ style.css          # 樣式
└─ README.md              # 專案說明文件
```

---

## 六、安裝與執行方式

### Step 1. 安裝套件

```bash
pip install flask requests PyPDF2
```

### Step 2. 啟動伺服器

```bash
python server.py
```

### Step 3. 開啟瀏覽器

```
http://127.0.0.1:5000
```

---

## 七、操作流程說明

1. 啟動系統並進入首頁
2. 選擇：

   * 一般問答，或
   * 上傳 PDF 文件
3. 選擇功能（摘要 / 出題）與模式
4. 系統分析 PDF 並回傳結果

---

📌 **Study Agent — Your AI-powered Study Partner**
