import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from matplotlib import font_manager

# 指定中文字體
my_font = font_manager.FontProperties(fname=r"C:\Windows\Fonts\msjh.ttc")

# 讀檔與前處理
df = pd.read_csv(r"C:\Users\dsa69\Desktop\新增資料夾\typhoon_utf8.csv", encoding="utf-8")
df.columns = df.columns.str.strip()
print(df.columns.tolist())

# 拆出欄位
years = df["年份"]
total = df["總颱風數"]
hit = df["侵台颱風數"]
ratio = hit / total

# ======================================
# 1️⃣ 散佈圖 + 趨勢線
# ======================================
plt.figure(figsize=(6, 5))
plt.scatter(total, hit, color='blue', label='每年資料')
model = LinearRegression()
model.fit(total.values.reshape(-1, 1), hit)
pred = model.predict(total.values.reshape(-1, 1))
plt.plot(total, pred, color='red', linestyle='--', label='趨勢線')

plt.title("總颱風數 vs 侵台颱風數", fontproperties=my_font)
plt.xlabel("總颱風數", fontproperties=my_font)
plt.ylabel("侵台颱風數", fontproperties=my_font)
plt.legend(prop=my_font)
plt.grid(True)
plt.tight_layout()
plt.show()

# ======================================
# 2️⃣ 折線圖（年度變化）
# ======================================
plt.figure(figsize=(7, 4))
plt.plot(years, total, marker='o', label='總颱風數')
plt.plot(years, hit, marker='s', label='侵台颱風數')
plt.xlabel("年份", fontproperties=my_font)
plt.ylabel("颱風數量", fontproperties=my_font)
plt.title("歷年颱風數變化", fontproperties=my_font)
plt.xticks(rotation=45)
plt.legend(prop=my_font)
plt.grid(True)
plt.tight_layout()
plt.show()

# ======================================
# 3️⃣ 比例圖（侵台佔比）
# ======================================
plt.figure(figsize=(7, 4))
plt.plot(years, ratio, marker='^', color='green')
plt.title("侵台颱風佔總數比例變化", fontproperties=my_font)
plt.xlabel("年份", fontproperties=my_font)
plt.ylabel("比例（侵台/總數）", fontproperties=my_font)
plt.grid(True)
plt.tight_layout()
plt.show()

# ======================================
# 4️⃣ 顯示 Pearson 相關係數
# ======================================
corr = np.corrcoef(total, hit)[0, 1]
print(f"📊 總颱風數 與 侵台颱風數 的相關係數為：{corr:.2f}")
