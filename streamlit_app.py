
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import defaultdict

st.set_page_config(page_title="🎰 Roulette Gợi Ý 2-3-4-10", layout="centered")
st.title("🎯 Gợi Ý Cược (Phương pháp 2, 3, 4, 10)")

# Nhóm số
group_map = {
    'A': [0, 2, 4, 15, 17, 19, 21, 25, 32, 34],
    'B': [6, 8, 10, 11, 13, 23, 27, 30, 36],
    'C': [1, 5, 9, 14, 16, 20, 24, 31, 33],
    'D': [3, 7, 12, 18, 22, 26, 28, 29, 35],
}
def find_group(num):
    for g, nums in group_map.items():
        if num in nums:
            return g
    return "?"
# Nhập số
results = st.text_area("Nhập kết quả Roulette:", "0 6 15 33 22 19")
numbers = [int(x) for x in re.findall(r'\d+', results)]
data = pd.DataFrame({"Số": numbers})
data["Nhóm"] = data["Số"].apply(find_group)

# Tạo gợi ý cho tay kế tiếp
next_predictions = ["—"] * len(data)
for i in range(len(data) - 2):
    g1 = data.loc[i, "Nhóm"]
    g2 = data.loc[i + 1, "Nhóm"]
    next_predictions[i + 2] = f"{g1}{g2}"

data["Gợi ý tay kế tiếp"] = next_predictions

# So sánh kết quả với gợi ý ở tay trước đó
results = []
for i in range(len(data)):
    if i == 0 or i == 1:
        results.append("⚪")
    else:
        pred = data.loc[i - 1, "Gợi ý tay kế tiếp"]
        actual = data.loc[i, "Nhóm"]
        results.append("🟢" if actual in pred else "🔴")

data["Kết quả"] = results

# Hiển thị bảng
st.subheader("📋 Bảng kết quả dự đoán tay tiếp theo")
st.dataframe(data.tail(100), use_container_width=True)

# Input
results = st.text_area("Nhập dãy số Roulette (cách nhau bởi dấu cách hoặc phẩy):", height=150)
numbers = [int(x) for x in re.findall(r'\d+', results)]
data = pd.DataFrame({"Số": numbers})
data["Nhóm"] = data["Số"].apply(find_group)

# Tính Markov nếu cần
markov_matrix = defaultdict(lambda: defaultdict(int))
for i in range(len(data)-1):
    markov_matrix[data.loc[i,"Nhóm"]][data.loc[i+1,"Nhóm"]] += 1
markov_prob = {}
for from_g, to_dict in markov_matrix.items():
    total = sum(to_dict.values())
    markov_prob[from_g] = {k: round(v/total,2) for k,v in to_dict.items()}

# Chọn phương pháp
method = st.radio("📌 Chọn phương pháp gợi ý:", [
    "2️⃣ Nhóm chưa xuất hiện gần đây",
    "3️⃣ Gợi ý theo cân bằng nhóm",
    "4️⃣ Mẫu A-A hoặc A-x-A",
    "🔟 Markov Chain"
])

# Dự đoán
predictions = []
for i in range(len(data)):
    if i == 0:
        predictions.append("—")
        continue
    prev = data.loc[i - 1, "Nhóm"]

    if method.startswith("2️⃣"):
        recent = data.loc[max(0, i - 10):i - 1, "Nhóm"]
        missing = [g for g in group_map if g not in recent.values]
        sugg = f"{prev} + {missing[0]}" if missing else prev

    elif method.startswith("3️⃣"):
        freq = data.loc[:i - 1, "Nhóm"].value_counts()
        sugg = " + ".join(freq.sort_values().head(2).index)

    elif method.startswith("4️⃣"):
        sugg = data.loc[i - 2, "Nhóm"] if i >= 2 and data.loc[i - 2, "Nhóm"] == data.loc[i - 1, "Nhóm"] else prev

    elif method.startswith("🔟"):
        prob_dict = markov_prob.get(prev, {})
        sugg = max(prob_dict.items(), key=lambda x: x[1])[0] if prob_dict else prev

    else:
        sugg = prev

    predictions.append(sugg)

# Dịch gợi ý sang tay sau
predictions = ["—"] + predictions[:-1]

# Tính kết quả
hits = ["⚪"]
for i in range(1, len(data)):
    actual = data.loc[i, "Nhóm"]
    pred = predictions[i]
    hit = "🟢" if actual in pred else "🔴"
    hits.append(hit)

data["Gợi ý trước đó"] = predictions
data["Kết quả"] = hits

# Hiển thị kết quả
st.subheader("📋 Kết quả dự đoán (gợi ý của tay trước)")
st.dataframe(data.tail(100), use_container_width=True)
