## 前置需求
在使用前請確保電腦裡裝有 `docker`，且可以使用 `docker compose` 命令。

確認方式：
```bash
docker --version
docker compose version
```

在 `env_files/mariadb/.env` 中設定以下環境變量
```ini
MARIADB_ROOT_PASSWORD = "your_root_password"
MARIADB_DATABASE = "your_database_name"
MARIADB_USER = "your_database_username"
MARIADB_PASSWORD = "your_user_password"
```

執行以下命令來創建環境
```bash
docker compose up -d
```

## 資料庫
輸入以下命令可以在終端中開啟 MariaDB Client
```bash
docker compose exec mariadb mariadb -u your_database_username -p
```

## 執行 python 腳本
輸入以下命令來執行 python 腳本
```bash
docker compose exec python python path/to/your/script.py
```

## 有關 docker compose
以下是一些常見的命令
- 建立環境：`docker compose up -d`
    - `-d`：隱藏輸出
- 移除環境：`docker compose down --rmi local -v`
    - `--rmi local`：移除 image
    - `-v`：移除 volume
- 啟動：`docker compose start`
- 停止：`docker compose stop`

這些命令都可以在最後面加上服務名稱來指定某一個特定的服務。這個專案有兩個服務，`mariadb` 和 `python`，分別是 MariaDB 資料庫以及 python 的運行環境。