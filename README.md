## 前置需求
在使用前請確保電腦裡裝有 `docker`，且可以使用 `docker compose` 命令。

執行以下命令來創建環境
```bash
docker compose up -d
```

## 資料庫
輸入以下命令可以在終端中開啟 MariaDB Client
```bash
docker compose exec mariadb mariadb --user=nutn --password=nutn@password nutn
```

## 執行 python 腳本
輸入以下命令來執行 python 腳本
```bash
docker compose exec python python path/to/your/script.py
```

- ### 將西北太平洋的颱風紀錄寫入資料庫
    比如你想要 2000 年到 2024 年的資料，這樣輸入
    ```bash
    docker compose exec python python scripts/typhoon_records.py 2000 2024
    ```
    如果你只想要 2024 年的資料，這樣輸入
    ```bash
    docker compose exec python python scripts/typhoon_records.py 2024
    ```

- ### 將每年西北太平洋的颱風總數量，以及侵台的颱風數量，寫成一張新表
    輸入以下指令
    ```bash
    docker compose exec python python scripts/number_of_typhoons.py
    ```

## 有關 docker compose
以下是一些常見的命令

| 指令 | 說明 |
| --- | --- |
| docker compose up &lt;**service**&gt; -d | 建立服務 (service 可選) |
| docker compose down &lt;**service**&gt; --rmi all -v| 移除服務 (service 可選) |
| docker compose start &lt;**service**&gt; | 啟動服務 (service 可選) |
| docker compose stop &lt;**service**&gt; | 關閉服務 (service 可選) |
| docker compose exec &lt;**service**&gt; &lt;**command**&gt; | 執行命令 |

這個專案有兩個服務，`mariadb` 和 `python`，分別是 MariaDB 資料庫以及 python 的運行環境。