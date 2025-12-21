# 📘 Study Agent – PDF-based AI Study Assistant (EXE 版)

## 一、簡介

**Study Agent** 是一個基於 Large Language Model（LLM）的學習輔助系統，結合 Flask 後端與 Web 前端，提供：

- 一般即時學習問答
- PDF 文件上傳後的分析（摘要 / 自動出題）

**EXE 版本**將系統封裝成 Windows 執行檔，使用者無需安裝 Python 或其他套件即可使用，特別設計用於 **課堂講義理解、考前複習、自主學習** 等情境。

---

## 二、系統功能

### 1. 一般學習問答

- 使用者可直接輸入問題
- 系統透過 LLM 即時回覆
- 適合概念釐清與即時提問

### 2. PDF 學習輔助（核心功能）

#### PDF 上傳限制

- 最多 **300 頁 PDF**
- 最多擷取 **5000 字文字內容**（避免模型負擔過重）

#### 摘要功能

- **全文重點摘要**（條列式，含頁碼）
- **每一頁重點摘要**（逐頁整理）

#### 自動出考題

- 單選題（含選項、答案與解析）
- 問答題（含標準答案）
- 混合題型（單選 + 問答）
- 每一題皆標示對應頁碼

---

## 三、系統架構

Browser (HTML / JavaScript)
↓
EXE (Flask Backend + PDF Parser)
↓
LLM API (Gemma Model)
---

## 四、技術說明

### 使用技術

- **前端**：HTML, JavaScript
- **後端**：Flask (Python，封裝於 EXE)
- **PDF 解析**：PyPDF2
- **LLM 模型**：Gemma 3 (4B)
- **API 呼叫**：RESTful API

### Prompt Engineering

系統根據使用者選擇的功能（摘要 / 出題），動態產生不同 Prompt，例如：

- 摘要模式：要求條列重點並標示頁碼
- 出題模式：限制題型、數量並附答案

---

## 五、專案結構（打包前）

study-agent/
│
├─ server.py # Flask 後端主程式
├─ templates/
│ └─ index.html # 前端介面
├─ static/
│ └─ style.css # 樣式
└─ README.md # 專案說明文件

---

## 六、安裝與執行方式（EXE 版）

### Step 1. 下載 EXE

- 將 `server.exe` 從 `dist` 資料夾拿出即可。

### Step 2. 執行 EXE

- 雙擊 `server.exe` 或在命令列執行：

```bash
dist\server.exe
```
系統會自動啟動本機 Flask server 並打開瀏覽器。

Step 3. 使用介面
網頁會自動開啟：

```cpp
http://127.0.0.1:5000
```
可直接輸入問題或上傳 PDF 使用摘要/出題功能。

---

## 七、操作流程說明

1. 雙擊 EXE，系統啟動，瀏覽器自動開啟首頁

2. 選擇功能：

- 一般問答
- PDF 文件分析

3. 選擇模式：

- 摘要 / 出題
- 摘要模式或題型

系統分析 PDF 並回傳結果
---
