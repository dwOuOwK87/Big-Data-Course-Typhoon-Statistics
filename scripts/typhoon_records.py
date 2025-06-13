import pymysql
import requests
import json
from typing import List, Dict, Optional
import argparse
from tqdm import trange


def get_records(year: int) -> Optional[List[Dict]]:
    """
    給一個 `年份 (西元)` 作為傳入值，回傳一個 json 的列表，其中的元素有以下屬性
    
    - `id`：                       颱風的編號
    - `cht_name`：                 颱風的中文名稱
    - `eng_name`：                 颱風的英文名稱
    - `genesis_datetime`：         颱風的生成時間
    - `dead_datetime`：            颱風的死亡時間
    - `max_intensity`：            每幾分鐘測得的所有 `平均` 風速中的最大風速 (m/s)
    - `max_gust_speed`：           每幾分鐘測得的所有 `最大` 風速中的最大風速 (m/s)
    - `min_pressure`：             最低氣壓 (hPa)
    - `max_class7_radius`：        7 級風暴的最大半徑 (km)
    - `max_class10_radius`：       10 級風暴的最大半徑 (km)
    - `warning_count`：            警報的次數

    ---

    補充：1994 年之前是用 1 分鐘平均，而 1995 年之後是用 10 分鐘平均。
    """
    try:
        payload = { "year": year } # 指定獲取某一年份的資料
        headers = { "X-Requested-With": "XMLHttpRequest" } # 必須要加上這個才能正確獲取資料

        response = requests.post(
            url="https://rdc28.cwa.gov.tw/TDB/public/typhoon_list/get_typhoon",
            data=payload,
            headers=headers,
        )

        response.raise_for_status()

        # 獲得的資料是一個 list of json，直接使用 response.json() 會有問題
        # 這裡的方法是用 json.loads，傳入一個 bytes 值，也就是 response.content
        data = json.loads(response.content)

        return data
    
    except Exception as e:
        print(f"在獲取 {year} 年的資料時發生錯誤，錯誤訊息:\n{e}")
        return None
    

def try_convert_str_to_int(string: str) -> Optional[int]:
    try:
        return int(string)
    except:
        return None
    

def write_records_to_database(start_year: int, end_year: Optional[int] = None) -> None:
    """
    將 `[start_year, end_year]` 區間的颱風紀錄寫入資料庫的 `typhoon_records` 表中。  
    如果不提供 `end_year` 則只會寫入 `start_year` 的颱風資料。
    """
    if end_year is None:
        end_year = start_year

    try:
        with pymysql.connect(
            user="nutn",
            password="nutn@password",
            host="mariadb-container", # 如果你不是用 docker compose 執行 python 腳本的話，這裡要改成 localhost
            port=3306,
            database="nutn"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS typhoon_records")

                cur.execute(
                    """
                    CREATE TABLE typhoon_records (
                        id INT PRIMARY KEY,
                        cht_name VARCHAR(100),
                        eng_name VARCHAR(100),
                        genesis_datetime DATETIME,
                        dead_datetime DATETIME,
                        max_wind_speed INT,
                        max_gust_speed INT,
                        min_pressure INT,
                        max_class7_radius INT,
                        max_class10_radius INT,
                        warning_count INT
                    )
                    """
                )

                for year in trange(start_year, end_year + 1):
                    records = get_records(year)

                    if records is None:
                        continue

                    for record in records:
                        id = record.get("id")
                        
                        if id is None:
                            continue

                        cht_name           = record.get("cht_name")
                        eng_name           = record.get("eng_name")
                        genesis_datetime   = record.get("genesis_datetime")
                        dead_datetime      = record.get("dead_datetime")

                        # max_intensity 理應是最大颱風強度
                        # API 將 max_intensity 當作了最大風速，這裡用更好理解的名稱代替
                        max_wind_speed     = try_convert_str_to_int( record.get("max_intensity") ) 

                        max_gust_speed     = try_convert_str_to_int( record.get("max_gust_speed") )
                        min_pressure       = try_convert_str_to_int( record.get("min_pressure") )
                        max_class7_radius  = try_convert_str_to_int( record.get("max_class7_radius") )
                        max_class10_radius = try_convert_str_to_int( record.get("max_class10_radius") )
                        warning_count      = try_convert_str_to_int( record.get("warning_count") )

                        cur.execute(
                            """
                            INSERT INTO typhoon_records(
                                id, cht_name, eng_name, genesis_datetime, dead_datetime, max_wind_speed, max_gust_speed,
                                min_pressure, max_class7_radius, max_class10_radius, warning_count
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                id, cht_name, eng_name, genesis_datetime, dead_datetime, max_wind_speed, max_gust_speed, 
                                min_pressure, max_class7_radius, max_class10_radius, warning_count
                            )
                        ) 

                conn.commit()

    except Exception as e:
        print(f"在寫入資料庫時發生錯誤，錯誤訊息:\n{e}")



if __name__ == "__main__":
    # 執行這個腳本時要執行的指令寫在這裡
    parser = argparse.ArgumentParser()

    parser.add_argument("start", help="資料的起始年分(西元)", type=int)
    parser.add_argument("end", help="資料的結束年分(西元)", type=int, default=None, nargs='?')

    args = parser.parse_args()

    write_records_to_database(args.start, args.end)