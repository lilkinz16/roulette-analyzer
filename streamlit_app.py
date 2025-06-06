
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

st.set_page_config(page_title="Phân Tích Roulette - Gợi ý tay tiếp theo", layout="centered")
st.title("🎯 Phân Tích Gợi Ý Theo 2 Tay Trước")

group_map = {
    'A': [0, 17],
    'B': [16, 18],
    'C': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 19, 20,],
    'D': [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
}

def find_group(num):
    for group, numbers in group_map.items():
        if num in numbers:
            return group
    return "?"

results = st.text_input("Nhập dãy số Roulette (cách nhau bởi dấu cách hoặc phẩy):", "0 16 17 18 19")

# Parse numbers
numbers = [int(x) for x in re.findall(r'\d+', results)]
groups = [find_group(n) for n in numbers]

# Prepare dataframe
data = pd.DataFrame({
    "Tay": list(range(1, len(numbers) + 1)),
    "Số": numbers,
    "Nhóm": groups
})

# Generate suggestions for next round
suggestions = ["—", "—"]
for i in range(2, len(groups)):
    pair = groups[i-2] + groups[i-1]
    suggestions.append(pair)
data["Gợi ý từ 2 tay trước"] = suggestions

# Generate result comparison
hits = ["⚪", "⚪"]
for i in range(2, len(groups)):
    suggestion = suggestions[i]
    actual = groups[i]
    hits.append("🟢" if actual in suggestion else "🔴")
data["Kết quả"] = hits

# Show table
st.dataframe(data)

# Show suggestion for next (n+1) hand
if len(groups) >= 2:
    next_suggestion = groups[-2] + groups[-1]
    st.markdown(f"🔮 **Gợi ý tay tiếp theo (tay {len(groups)+1}): `{next_suggestion}`**")

# === Bảng Baccarat-style hiển thị kết quả đúng/sai ===
st.subheader("🧮 Bảng Cầu Baccarat-style")

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
