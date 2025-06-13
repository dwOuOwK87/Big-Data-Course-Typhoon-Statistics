import pymysql


def get_number_of_typhoons():
    """
    建立一張包含每年總颱風數量，以及侵台颱風數量的表
    """
    try:
        with pymysql.connect(
            user="nutn",
            password="nutn@password",
            host="mariadb-container", # 如果你不是用 docker compose 執行 python 腳本的話，這裡要改成 localhost
            port=3306,
            database="nutn"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS number_of_typhoons")

                cur.execute(
                    """
                    CREATE TABLE number_of_typhoons AS
                    SELECT
                        YEAR(genesis_datetime) AS year,
                        COUNT(*) AS total_count,
                        SUM(CASE WHEN warning_count IS NOT NULL THEN 1 ELSE 0 END) AS count_entered
                    FROM typhoon_records
                    GROUP BY year
                    ORDER BY year;
                    """
                )
    
                conn.commit()

    except Exception as e:
        print(f"在寫入資料庫時發生錯誤，錯誤訊息:\n{e}")


if __name__ == "__main__":
    get_number_of_typhoons()
