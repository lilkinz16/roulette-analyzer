import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

st.set_page_config(page_title="Phân Tích Roulette - Gợi ý tay tiếp theo", layout="centered")
st.title("🎯 Phân Tích Gợi Ý Theo 2 Tay Trước")

group_map = {
    'A': [0, 1, 6, 9, 18, 21, 28, 31, 36],
    'B': [2, 3, 5, 8, 17, 20, 29, 32, 24, 27],
    'C': [4, 7, 10, 13, 16, 19, 30, 33],
    'D': [12, 15, 11, 14, 22, 25, 28, 34, 35],
}

def find_group(num):
    for group, numbers in group_map.items():
        if num in numbers:
            return group
    return "?"

results = st.text_input("Nhập dãy số Roulette (cách nhau bởi dấu cách hoặc phẩy):", "22 19 15 33 19")

# Parse numbers
numbers = [int(x) for x in re.findall(r'\d+', results)]
groups = [find_group(n) for n in numbers]

# Cảnh báo nếu có số không thuộc nhóm nào
invalid_nums = [n for n, g in zip(numbers, groups) if g == "?"]
if invalid_nums:
    st.warning(f"Các số sau không thuộc nhóm nào: {invalid_nums}")

# Prepare dataframe
data = pd.DataFrame({
    "Tay": list(range(1, len(numbers) + 1)),
    "Số": numbers,
    "Nhóm": groups
})

# Generate suggestions
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

# Gợi ý tiếp theo
if len(groups) >= 2:
    next_suggestion = groups[-2] + groups[-1]
    st.markdown(f"🔮 **Gợi ý tay tiếp theo (tay {len(groups)+1}): `{next_suggestion}`**")

# Tính % chính xác
total_checked = sum(x in ["🟢", "🔴"] for x in hits)
correct = hits.count("🟢")
accuracy = correct / total_checked * 100 if total_checked > 0 else 0
st.markdown(f"📊 **Tỷ lệ gợi ý đúng: `{accuracy:.2f}%`** ({correct}/{total_checked})")

# Lọc chuỗi thắng/thua liên tục
def get_streaks(hits_list, symbol):
    max_streak = 0
    current = 0
    streaks = []
    for h in hits_list:
        if h == symbol:
            current += 1
        else:
            if current > 0:
                streaks.append(current)
                max_streak = max(max_streak, current)
            current = 0
    if current > 0:
        streaks.append(current)
        max_streak = max(max_streak, current)
    return max_streak, streaks[-1] if streaks else 0

max_win, current_win = get_streaks(hits, "🟢")
max_lose, current_lose = get_streaks(hits, "🔴")

st.markdown(f"🟢 **Chuỗi thắng dài nhất:** {max_win} | **Hiện tại:** {current_win}")
st.markdown(f"🔴 **Chuỗi thua dài nhất:** {max_lose} | **Hiện tại:** {current_lose}")

# Hiển thị bảng
st.subheader("📋 Bảng Phân Tích")
st.dataframe(data)

# Bảng Cầu Baccarat-style
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
