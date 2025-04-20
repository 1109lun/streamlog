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