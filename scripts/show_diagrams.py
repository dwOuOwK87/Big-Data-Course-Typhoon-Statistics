import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import pymysql
from matplotlib import font_manager



def show_diagrams(years, total, hit, ratio, font):
    # ======================================
    # 1️⃣ 散佈圖 + 趨勢線
    # ======================================
    plt.figure(figsize=(6, 5))
    plt.scatter(total, hit, color='blue', label='每年資料')
    model = LinearRegression()
    model.fit(total.values.reshape(-1, 1), hit)
    pred = model.predict(total.values.reshape(-1, 1))
    plt.plot(total, pred, color='red', linestyle='--', label='趨勢線')

    plt.title("總颱風數 vs 侵台颱風數", fontproperties=font)
    plt.xlabel("總颱風數", fontproperties=font)
    plt.ylabel("侵台颱風數", fontproperties=font)
    plt.legend(prop=font)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output_diagrams/scatter_plot.png")

    # ======================================
    # 2️⃣ 折線圖（年度變化）
    # ======================================
    plt.figure(figsize=(7, 4))
    plt.plot(years, total, marker='o', label='總颱風數')
    plt.plot(years, hit, marker='s', label='侵台颱風數')
    plt.xlabel("年份", fontproperties=font)
    plt.ylabel("颱風數量", fontproperties=font)
    plt.title("歷年颱風數變化", fontproperties=font)
    plt.xticks(rotation=45)
    plt.legend(prop=font)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output_diagrams/line_plot.png")

    # ======================================
    # 3️⃣ 比例圖（侵台佔比）
    # ======================================
    plt.figure(figsize=(7, 4))
    plt.plot(years, ratio, marker='^', color='green')
    plt.title("侵台颱風佔總數比例變化", fontproperties=font)
    plt.xlabel("年份", fontproperties=font)
    plt.ylabel("比例（侵台/總數）", fontproperties=font)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output_diagrams/ratio_plot.png")

    # ======================================
    # 4️⃣ 顯示 Pearson 相關係數
    # ======================================
    corr = np.corrcoef(total, hit)[0, 1]
    print(f"📊 總颱風數 與 侵台颱風數 的相關係數為：{corr:.2f}")



if __name__ == "__main__":

    # 指定中文字體
    font = font_manager.FontProperties(fname=r"msjh.ttc")

    try:
        with pymysql.connect(
            user="nutn",
            password="nutn@password",
            host="mariadb-container", # 如果你不是用 docker compose 執行 python 腳本的話，這裡要改成 localhost
            port=3306,
            database="nutn"
        ) as conn:
            # 讀檔
            df = pd.read_sql_query("SELECT * FROM number_of_typhoons", conn)

            # 折出年份、總颱風數、侵台颱風數
            years = df["year"]
            total = df["total_count"]
            hit = df["count_entered"]

            ratio = hit / total

            # 顯示圖表
            show_diagrams(years, total, hit, ratio, font)
                

    except Exception as e:
        print(f"在寫入資料庫時發生錯誤，錯誤訊息:\n{e}")