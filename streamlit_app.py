
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="📈 Gợi Ý Tay Tiếp Theo", layout="centered")
st.title("🎰 Dự đoán nhóm cho tay TIẾP THEO dựa vào 2 tay gần nhất")

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
