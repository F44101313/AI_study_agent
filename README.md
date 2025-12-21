# Study Agent – PDF-based AI Study Assistant

## 一、簡介

**Study Agent** 是一個基於 Large Language Model（LLM）的學習輔助系統，結合 Flask 後端與 Web 前端，提供：

* 一般即時學習問答（Chat Agent）
* PDF 文件上傳後的智慧分析（摘要 / 自動出題）

本系統特別設計用於 **課堂講義理解、考前複習、自主學習** 等情境。

---

## 二、系統功能

### 1. 一般學習問答

* 使用者可直接輸入問題
* 系統透過 LLM 即時回覆
* 適合概念釐清與即時提問

### 2. PDF 學習輔助

####  PDF 上傳限制

* 最多 **300 頁 PDF**
* 最多擷取 **5000 字文字內容**（避免模型負擔過重）

####  摘要功能

* **全文重點摘要**（條列式）

### 3. 自動出考題

* 單選題（含選項、答案與解析）
* 問答題（含標準答案）
* 混合題型（單選 + 問答）

---

## 三、系統架構

```
使用者 (瀏覽器) 
        ↓
Study Agent EXE
 ├─ Flask Web Server (後端處理請求)
 ├─ PDF Parser (PyPDF2 讀取與抽取文字)
 └─ LLM API (Gemma 3 模型進行摘要/出題)
        ↓
回傳結果到瀏覽器

```

---

## 四、技術說明

###  使用技術

* **Frontend**：HTML, JavaScript, CSS
* **Backend**：Flask (Python)
* **PDF 解析**：PyPDF2
* **LLM 模型**：Gemma 3 (4B)
* **API 呼叫**：RESTful API

###  Prompt Engineering

系統根據使用者選擇的功能（摘要 / 出題），動態產生不同 Prompt，例如：

* 摘要模式：要求條列重點
* 出題模式：限制題型、數量並附答案

---

## 五、專案結構(打包成exe前)

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

### Step 1.

- 從 `dist` 資料夾找到`server.exe`。

### Step 2. 執行 EXE

- 點擊 `server.exe` 或在命令列執行：

```bash
dist\server.exe
```
* 系統會自動啟動本機 Flask server 並打開瀏覽器。

### Step 3. 使用介面
- 網頁會自動開啟：
```cpp
http://127.0.0.1:5000
```
- 可直接輸入問題或上傳 PDF 使用摘要/出題功能。

## 七、操作流程說明

1. 啟動系統並進入首頁
2. 選擇：
   * 一般問答，或
   * 上傳 PDF 文件
3. 選擇功能（摘要 / 出題）與模式
4. 系統分析 PDF 並回傳結果
5. 可以選擇新對話以重置對話

---
