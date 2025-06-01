
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import defaultdict, Counter

st.set_page_config(page_title="Phân Tích Roulette", layout="centered")
st.title("🎰 Phân Tích Roulette Theo Nhóm A/B/C/D")

# ==== Cấu hình nhóm ====
group_map = {
    'A': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    'B': [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
    'C': [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
    'D': [90, 91, 92, 93, 94, 95, 96, 97, 98, 99],
}

# ==== Nhập dữ liệu ====
results = st.text_input("Nhập dãy số Roulette (cách nhau bởi dấu cách hoặc phẩy):", "29 21 15 1 0 2 1")
numbers = [int(x) for x in re.findall(r'\d+', results)]
data = pd.DataFrame({"Số": numbers})

def find_group(num):
    for group, numbers in group_map.items():
        if num in numbers:
            return group
    return "?"

data["Nhóm"] = data["Số"].apply(find_group)

# ==== Tính Markov ====
markov_matrix = defaultdict(lambda: defaultdict(int))
markov_prob = {}
for i in range(len(data) - 1):
    from_g = data.loc[i, "Nhóm"]
    to_g = data.loc[i + 1, "Nhóm"]
    markov_matrix[from_g][to_g] += 1
for from_g, targets in markov_matrix.items():
    total = sum(targets.values())
    markov_prob[from_g] = {to_g: round(count / total, 2) for to_g, count in targets.items()}


# Tạo các cột kết quả
suggestions = []
hits = []

for i in range(len(data)):
    if i < 2:
        suggestions.append("—")
        hits.append("⚪")
    else:
        sugg = generate_suggestion(i, data, markov_prob, method_select)
        suggestions.append(sugg)
        actual = data.loc[i, "Nhóm"]
        hits.append("🟢" if actual in sugg else "🔴")

data["Gợi ý từ 2 tay trước"] = suggestions
data["Kết quả"] = hits

# Hiển thị bảng dữ liệu
st.subheader("🧾 Kết quả phân loại")
st.dataframe(data)

# Gợi ý tay tiếp theo
next_suggestion = generate_suggestion(len(data), data, markov_prob, method_select)
st.subheader("📍 Gợi ý cho tay kế tiếp:")
st.write(f"👉 **{next_suggestion}**")

# Bảng Baccarat-style
st.subheader("🎯 Bảng cầu Baccarat-style")

results_seq = data["Kết quả"].tolist()
columns = []
col = []
last = None

for r in results_seq:
    if r == last:
        col.append(r)
    else:
        if col:
            columns.append(col)
        col = [r]
        last = r
if col:
    columns.append(col)

max_len = max(len(c) for c in columns) if columns else 1
fig, ax = plt.subplots(figsize=(len(columns), max_len))
ax.axis('off')

for x, col in enumerate(columns):
    for y, val in enumerate(col):
        color = "#4CAF50" if val == '🟢' else "#F44336"
        ax.add_patch(plt.Rectangle((x, -y), 1, 1, color=color))
        ax.text(x + 0.5, -y + 0.5, val, va='center', ha='center', fontsize=16, color='white')

plt.xlim(0, len(columns))
plt.ylim(-max_len, 1)
plt.tight_layout()
st.pyplot(fig)
