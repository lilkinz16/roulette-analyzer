
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Phân Tích Roulette", layout="centered")

# Nhóm quy ước
group_map = {
    'A': [0, 2, 4, 15, 17, 19, 21, 25, 32, 34],
    'B': [6, 8, 10, 11, 13, 23, 27, 30, 36],
    'C': [1, 5, 9, 14, 16, 20, 24, 31, 33],
    'D': [3, 7, 12, 18, 22, 26, 28, 29, 35],
}

def find_group(num):
    for group, numbers in group_map.items():
        if num in numbers:
            return group
    return "?"

st.title("🎰 Phân Tích Roulette Theo Nhóm A/B/C/D")

results = st.text_input("Nhập dãy số Roulette (cách nhau bởi dấu cách hoặc phẩy):", "29 21 15 1 0 2 1")
method = st.radio("🔍 Chọn cách gợi ý cược", [
    "1️⃣ Gần nhất + Nhóm ít nhất",
    "2️⃣ Gần nhất + Nhóm chưa xuất hiện gần đây",
    "3️⃣ Gợi ý theo cân bằng nhóm",
    "4️⃣ Mẫu lặp A-x-A hoặc A-A-x"
])

# Xử lý dữ liệu
import re
numbers = [int(x) for x in re.findall(r'\d+', results)]
data = pd.DataFrame({"Số": numbers})
data["Nhóm"] = data["Số"].apply(find_group)
data["Chu kỳ 5 tay"] = (data.index // 5) + 1

# Gợi ý theo phương pháp
suggestions = []
hits = []
for i in range(len(data)):
    if i == 0:
        suggestions.append("—")
        hits.append("⚪")
        continue
    current = data.loc[i, "Nhóm"]

    if method.startswith("1️⃣"):
        prev = data.loc[i - 1, "Nhóm"]
        freq = data.loc[:i - 1, "Nhóm"].value_counts()
        least = freq.idxmin()
        sugg = f"{prev} + {least}" if prev != least else prev

    elif method.startswith("2️⃣"):
        recent = data.loc[max(0, i - 10):i - 1, "Nhóm"]
        missing = [g for g in group_map if g not in set(recent)]
        prev = data.loc[i - 1, "Nhóm"]
        sugg = f"{prev} + {missing[0]}" if missing else prev

    elif method.startswith("3️⃣"):
        freq = data.loc[:i - 1, "Nhóm"].value_counts()
        sorted_freq = freq.sort_values()
        sugg = " + ".join(sorted_freq.head(2).index)

    elif method.startswith("4️⃣"):
        sugg = data.loc[i - 2, "Nhóm"] if i >= 2 and data.loc[i - 2, "Nhóm"] == data.loc[i - 1, "Nhóm"] else data.loc[i - 1, "Nhóm"]

    suggestions.append(sugg)
    hit = "🟢" if current in sugg else "🔴"
    hits.append(hit)

data["Gợi ý trước"] = suggestions
data["Kết quả"] = hits

# Thống kê
freq = data["Nhóm"].value_counts().sort_index()
latest_group = data["Nhóm"].iloc[-1] if not data.empty else ""
streak = 1
for i in range(len(data) - 2, -1, -1):
    if data["Nhóm"].iloc[i] == latest_group:
        streak += 1
    else:
        break
least_group = freq.idxmin() if not freq.empty else ""
suggested = f"{latest_group} + {least_group}" if latest_group != least_group else latest_group

# Kết quả phân loại
st.subheader("🧾 Kết quả phân loại")
st.dataframe(data)

# Phân tích
st.subheader("📊 Phân tích thống kê")
st.write(f"✅ Nhóm gần nhất: **{latest_group}**")
st.write(f"📌 Độ dài chuỗi liên tiếp: **{streak} lần**")
st.write(f"🎯 Gợi ý nhóm cược: **{suggested}**")

# Bảng chi tiết
st.subheader("📋 Bảng chi tiết kết quả")
st.dataframe(data)

# Biểu đồ
st.subheader("📈 Biểu đồ tần suất nhóm")
fig, ax = plt.subplots()
freq.plot(kind="bar", ax=ax)
plt.xlabel("Nhóm")
plt.ylabel("Số lần xuất hiện")
plt.title("Tần suất xuất hiện của các nhóm")
st.pyplot(fig)

