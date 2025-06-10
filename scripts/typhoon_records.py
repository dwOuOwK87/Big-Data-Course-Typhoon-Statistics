import pymysql
import requests
import json
from typing import List, Dict, Optional


def get_data(year: int) -> Optional[List[Dict]]:
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
    
    except requests.HTTPError as e:
        print(f"在獲取 {year} 年的資料時發生錯誤，錯誤訊息:\n{e}")
        return None
    

def write_records_to_database() -> None:
    try:
        with pymysql.connect(
            user="nutn",
            password="nutn@password",
            host="mariadb-container",
            port=3306,
            database="nutn"
        ) as conn:
            with conn.cursor() as cur:
                # 做一些資料庫的操作
                conn.commit()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    # 執行這個腳本時要執行的指令寫在這裡
    print(get_data(2024))

    