
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import defaultdict, Counter

st.set_page_config(page_title="Phân Tích Roulette", layout="centered")
st.title("🎰 Phân Tích Roulette Theo Nhóm A/B/C/D")

# ==== Cấu hình nhóm ====
group_map = {
    'A': [0, 2, 4, 15, 17, 19, 21, 25, 32, 34],
    'B': [6, 8, 10, 11, 13, 23, 27, 30, 36],
    'C': [1, 5, 9, 14, 16, 20, 24, 31, 33],
    'D': [3, 7, 12, 18, 22, 26, 28, 29, 35],
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

# ==== Gợi ý ====
def generate_suggestion(i, data, markov_prob, method="2️⃣"):
    if i < 2:
        return "—"

    prev_1 = data.loc[i - 1, "Nhóm"]
    prev_2 = data.loc[i - 2, "Nhóm"]
    freq = data.loc[:i - 1, "Nhóm"].value_counts()
    recent = data.loc[max(0, i - 10):i - 1, "Nhóm"]
    markov_prev = prev_1
    missing = [g for g in group_map if g not in recent.values]

    if method == "2️⃣":
        return f"{prev_1} + {missing[0]}" if missing else prev_1

    elif method == "3️⃣":
        return " + ".join(freq.sort_values().head(2).index)

    elif method == "4️⃣":
        if prev_1 == prev_2:
            return prev_1
        elif i >= 3 and prev_2 == data.loc[i - 3, "Nhóm"]:
            return prev_2
        else:
            return prev_1

    elif method == "🔟":
        prob_dict = markov_prob.get(markov_prev, {})
        if prob_dict:
            best = max(prob_dict.items(), key=lambda x: x[1])[0]
            return best
        else:
            return markov_prev

    return prev_1

method_select = st.selectbox("📌 Chọn phương pháp gợi ý:", ["2️⃣", "3️⃣", "4️⃣", "🔟"])

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
