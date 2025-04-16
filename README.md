# streamlog
串流平台觀影筆記與分享平台

> 📽️ 串流平台觀影紀錄與分享平台（支援 Netflix、Disney+ 等）

本專案採用 Python + Flask 作為後端，HTML + Bootstrap 作為前端介面，資料庫使用 MySQL，並透過 Poetry 管理 Python 套件與虛擬環境，確保跨平台開發一致性。

---

## 📦 專案架構

```
streamlog/
├── backend/              # Flask + SQLAlchemy 專案後端
│   ├── app/              # Flask 主程式、routes、models 等
│   └── pyproject.toml    # Poetry 設定檔
├── frontend/             # HTML + Bootstrap 靜態頁面
│   ├── index.html
│   └── assets/
├── database/             # 資料庫設計文件、SQL 腳本
│   ├── schema.sql
│   └── ER-diagram.png
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

## 🛠️ 環境建置步驟（macOS / Windows WSL 適用）

> 建議先完成 Git 環境與 repo clone，再依以下步驟安裝後端、資料庫等開發環境。

### ✅ 前置需求工具

| 工具             | 建議安裝方式                      | 用途說明 |
|------------------|----------------------------------|----------|
| Git              | 官網 / Homebrew / apt            | 版本控制工具 |
| pyenv            | Homebrew（mac）/ curl（WSL）     | Python 版本管理 |
| Poetry           | 官方 script 安裝                 | Python 套件與虛擬環境管理 |
| MySQL            | brew / apt 安裝                  | 專案資料庫 |
| MySQL Workbench  | 官網下載                         | GUI 管理工具（選用） |

---

## 🧰 Python 環境建置（pyenv + Poetry）

### 1. 安裝 pyenv

#### macOS：
```bash
brew install pyenv
```

#### Windows / WSL：
```bash
curl https://pyenv.run | bash
```

> 加入以下到你的 ~/.bashrc 或 ~/.zshrc，儲存後重新啟動終端機：
```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

---

### 2. 安裝 Python 版本（3.11.10）
```bash
pyenv install 3.11.10
pyenv global 3.11.10
```

檢查是否成功：
```bash
python3 --version
```

---

### 3. 安裝 Poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

設定 Poetry 使用 pyenv 安裝的 Python：
```bash
poetry env use $(pyenv which python)
```

---

## 📦 後端專案初始化

```bash
cd backend
poetry install
```

若是第一次建立，可以這樣：
```bash
poetry init
poetry add flask flask_sqlalchemy pymysql
```

---

## 🛢️ 安裝 MySQL 資料庫

### macOS：
```bash
brew install mysql
brew services start mysql
```

### WSL（Ubuntu）：
```bash
sudo apt update
sudo apt install mysql-server
sudo service mysql start
```

登入測試：
```bash
mysql -u root -p
```

---

## 📐 初始化資料庫

可執行 `database/schema.sql`：
```bash
mysql -u root -p < database/schema.sql
```

或使用 MySQL Workbench 匯入資料表。

---

## 🧪 啟動 Flask 伺服器

```bash
cd backend
poetry shell
flask run
```

開啟瀏覽器前往： [http://localhost:5000](http://localhost:5000)

---

## 💡 注意事項

- 所有 Python 套件請使用 `poetry add` 安裝，避免混用 pip。
- clone 專案後，在 backend 資料夾中執行 `poetry install` 建立虛擬環境。
- 敏感資訊（如 DB 密碼）請放在 `.env`，並加入 `.gitignore` 中。

---

本文件為初次環境建置流程，若有更新，請至 GitHub repo 上查閱最新版。

