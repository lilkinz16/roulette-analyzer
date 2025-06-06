import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

st.set_page_config(page_title="Phân Tích Roulette - Cầu Nhóm", layout="centered")
st.title("🎯 Phân Tích Cầu Theo Nhóm Roulette")

# ===== Nhập nhóm động =====
st.subheader("✏️ Thiết lập nhóm số Roulette")

group_input = {
    'A': st.text_input("Nhóm A:", "0, 17"),
    'B': st.text_input("Nhóm B:", "16, 18"),
    'C': st.text_input("Nhóm C:", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 19, 20"),
    'D': st.text_input("Nhóm D:", "21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36"),
}

# Parse thành dict group_map
group_map = {
    group: [int(x.strip()) for x in re.findall(r'\d+', val)]
    for group, val in group_input.items()
}

# ===== Hàm phân nhóm =====
def find_group(num):
    for group, numbers in group_map.items():
        if num in numbers:
            return group
    return "?"

# ===== Nhập kết quả roulette =====
results = st.text_input("🎲 Nhập dãy số Roulette (cách nhau bởi dấu cách hoặc phẩy):", "0 16 17 18 19")
numbers = [int(x) for x in re.findall(r'\d+', results)]
groups = [find_group(n) for n in numbers]

# ===== Bảng phân tích =====
data = pd.DataFrame({
    "Tay": list(range(1, len(numbers) + 1)),
    "Số": numbers,
    "Nhóm": groups
})

st.subheader("📋 Kết quả nhóm")
st.dataframe(data, use_container_width=True)

# ===== Bảng Cầu Baccarat-style theo nhóm =====
st.subheader("🧮 Bảng Cầu Baccarat-style")

# Định nghĩa màu cho từng nhóm
group_colors = {
    'A': "#F44336",  # đỏ
    'B': "#2196F3",  # đỏ
    'C': "#4CAF50",  # xanh lá
    'D': "#FF9800",  # xanh lá
    '?': "#9E9E9E"   # xám
}

columns = []
col = []
last = None

for group in groups:
    if group == last:
        col.append(group)
    else:
        if col:
            columns.append(col)
        col = [group]
        last = group
if col:
    columns.append(col)

max_len = max(len(c) for c in columns) if columns else 1
fig, ax = plt.subplots(figsize=(len(columns), max_len))
ax.axis('off')

for x, col in enumerate(columns):
    for y, val in enumerate(col):
        color = group_colors.get(val, "#9E9E9E")
        ax.add_patch(plt.Rectangle((x, -y), 1, 1, color=color))
        ax.text(x + 0.5, -y + 0.5, val, va='center', ha='center', fontsize=16, color='white')

plt.xlim(0, len(columns))
plt.ylim(-max_len, 1)
plt.tight_layout()
st.pyplot(fig)
