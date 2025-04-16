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