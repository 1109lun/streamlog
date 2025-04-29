# 📦 Streamlog 專案後端環境建置教學（for macOS / WSL）

本指南針對第一次建立本地端後端開發環境的使用者，涵蓋 Python / MySQL 安裝、Poetry 建置、Flask 執行、測試 API 等完整流程。

---

## 📁 專案資料夾結構

```
streamlog/
├── backend/              # Flask + SQLAlchemy 專案後端
│   ├── app/              # Flask 主程式、routes、models 等
│   ├── pyproject.toml    # Poetry 設定檔
│   ├── .env.example      # 資料庫連線設定範例
│   ├── main.py           # Flask 主程式
│   └── db/               # schema 與假資料 SQL
│       ├── schema.sql
│       └── backup.sql
├── frontend/             # HTML + Bootstrap 靜態頁面
│   ├── index.html
│   └── assets/
├── .gitignore            # 忽略檔案設定
└── README.md             # 專案說明文件
```

---

## 🧰 開發工具需求

| 工具              | 推薦版本      | 備註                                 |
|-------------------|---------------|--------------------------------------|
| Python            | 3.11.10       | 使用 `pyenv` 統一                    |
| Poetry            | 最新穩定版    | 套件與虛擬環境管理工具               |
| MySQL             | 8.x           | 可使用 Homebrew（mac）或 APT（WSL） |
| MySQL Workbench   | 最新版        | GUI 工具，選用                       |
| Git + GitHub      | -             | 版本控管                             |

---

## 🔧 一、Python 與虛擬環境建置（pyenv + Poetry）

### ✅ 0. 安裝 pyenv , Poetry

### ✅ 1. 安裝 Python 版本（3.11.10）
```bash
pyenv install 3.11.10
pyenv local 3.11.10
```

確認版本：
```bash
python3 --version  # 應顯示 Python 3.11.10
```

### ✅ 2. 安裝 Poetry 並初始化虛擬環境
```bash
cd backend
poetry install
```

---

## 📁 二、.env 設定

### ✅ 1. 複製 .env.example 成為 .env
```bash
cp .env.example .env
```

### ✅ 2. 修改 .env 密碼（與 MySQL root 設定一致）
```env
DB_USER=streamlog_user
DB_PASSWORD=你的密碼
DB_HOST=localhost
DB_NAME=streamlog
```

---

## 🧱 三、MySQL 資料庫初始化（僅 root 執行一次）

### ✅ 1. 啟動 MySQL

#### macOS:
```bash
mysql.server start
```

#### WSL:
```bash
sudo service mysql start
```

### ✅ 2. 修改 schema.sql 中密碼欄位為你的密碼（如有 `CREATE USER`）

### ✅ 3. 匯入資料庫 schema
```bash
mysql -u root -p < db/schema.sql
```

### ✅ 4. 匯入假資料
```bash
mysql -u root -p < db/backup.sql
```

---

## 🚀 四、啟動 Flask 開發伺服器

```bash
poetry run python main.py
```

看到：
```
* Running on http://127.0.0.1:5000
```
代表啟動成功 ✅

---

## 🔍 五、測試 API 是否成功

### ✅ 測試 GET /api/v1/logs
```bash
curl http://localhost:5000/api/v1/logs
```

預期回應：會顯示一筆你組員事先加上的測試資料，例如：

```json
[
  {
    "id": 1,
    "level": "INFO",
    "message": "測試日誌訊息",
    "source": "test",
    "timestamp": "2025-04-19T17:13:59",
    "created_at": "2025-04-19T17:13:59"
  }
]
```

---

## 💡 注意事項

- 所有 Python 套件請使用 `poetry add` 安裝，避免混用 pip。
- clone 專案後，在 backend 資料夾中執行 `poetry install` 建立虛擬環境。
- 敏感資訊（如 DB 密碼）請放在 `.env`，並加入 `.gitignore` 中。

---

🌟 一次設好環境後，之後每次只要執行：

#### macOS:
```bash
mysql.server start
poetry run python main.py
curl http://localhost:5000/api/v1/logs
```

#### WSL:
```bash
sudo service mysql start
poetry run python main.py
curl http://localhost:5000/api/v1/logs
```

就可以順利開發與測試了！


# Streamlog 資料庫建立指引

---

## 此段功能目的

這份文件用來指導組員如何將本地 MySQL 資料庫環境，完成 Streamlog 必要的資料表建立。

---

## 操作流程

### 1. 拉取最新代碼

在你自己的工作目錄，先確保 main 是最新：

```bash
git checkout main
git pull origin main
```

---

### 2. 登入 MySQL

開啟你自己的 MySQL，使用下列指令登入：

```bash
mysql -u root -p
```

入內後，輸入 root 密碼。

---

### 3. 執行 schema.sql 建立資料表

在 mysql> prompt 上，執行：

```sql
source backend/db/schema.sql;
```

(請根據你自己的目錄路徑修正)

---

### 4. 確認資料表建立成功

切換到 streamlog 資料庫：

```sql
USE streamlog;
```

查看現有資料表：

```sql
SHOW TABLES;
```

應該看到以下四張資料表：

| Tables_in_streamlog |
|:-------------------|
| User               |
| Movie              |
| WatchLog           |
| UserNote           |

---

## 資料表說明

### ▶ User
- 記錄組員基本資料
- 欄位：user_id (PK), user_name, email, age

### ▶ Movie
- 記錄電影基礎資料
- 欄位：movie_id (PK), title, genre, duration, release_year, rating

### ▶ WatchLog
- 編錄用戶看電影記錄
- 欄位：watch_id (PK), user_id (FK), movie_id (FK), watch_date, mood, rating

### ▶ UserNote
- 編錄用戶閱影後留下的笔記/心得
- 欄位：note_id (PK), user_id (FK), movie_id (FK), content, created_at, like_count

---

## 注意事項

- **source schema.sql 不會自動變更原本的資料，只會增加新表或覆蓋。**
- **如果重複 source ，請確保有配合 `IF NOT EXISTS` 以防止錯誤。**
- **如果目前資料庫有舊的 logs 表，請使用 `DROP TABLE logs;` 刪除。**

---

(本文件最後一段不要刪掉，接著各組員可以操作使用。)

# Streamlog 資料庫頁面啟動流程 ( 前後端不分離版 )

## 🚀 本地開發啟動流程

### 1️⃣ 安裝必要套件

請先進入 `backend/` 資料夾：

```bash
cd backend
poetry install
```

(第一次下載專案需要，之後如果環境沒變可省略)

---

### 2️⃣ 啟動後端伺服器

```bash
poetry run python -m main
```

- Flask 會啟動於 `http://localhost:5000`
- 不需要另外啟動前端 server

---

### 3️⃣ 打開瀏覽器測試

請直接打開：

```
http://localhost:5000/
```

- 未登入時：會引導至登入畫面
- 登入後：顯示首頁，並有下拉式功能選單

---

## 🔹 功能簡介

| 項目 | 說明 |
|:--|:--|
| 登入 | 使用 email + password 驗證 (目前是純文字驗證) |
| 註冊 | 新增使用者，email 必須唯一 |
| 登出 | 清除 session，回到登入畫面 |
| 填寫日記/觀看日記 | 功能預留（待開發） |

---

## 🔹 注意事項

- 本專案已改為 **前後端不分離**，前端頁面通過 Flask `render_template` 顯示
- 登入狀態使用 Flask `session` 管理，必須設定 `app.secret_key`
- 目前密碼驗證是純文字比對，正式上線建議改用 bcrypt 加密
- CORS 問題已解決，但請確認從 `http://localhost:5000/` 開啟

---
