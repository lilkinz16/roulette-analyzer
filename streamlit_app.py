
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import defaultdict, Counter

st.set_page_config(page_title="Phân Tích Roulette", layout="centered")
st.title("🎰 Phân Tích Roulette Theo Nhóm A/B/C/D + Tá nhóm + Cột")

# ==== Cấu hình nhóm ====
group_map = {
    'A': [0, 2, 4, 15, 17, 19, 21, 25, 32, 34],
    'B': [6, 8, 10, 11, 13, 23, 27, 30, 36],
    'C': [1, 5, 9, 14, 16, 20, 24, 31, 33],
    'D': [3, 7, 12, 18, 22, 26, 28, 29, 35],
}

column_map = {
    'C1': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
    'C2': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
    'C3': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
}

def find_group(num):
    for group, numbers in group_map.items():
        if num in numbers:
            return group
    return "?"

def find_dozen(num):
    if 1 <= num <= 12:
        return "T1"
    elif 13 <= num <= 24:
        return "T2"
    elif 25 <= num <= 36:
        return "T3"
    else:
        return "T0"

def find_column(num):
    for col, nums in column_map.items():
        if num in nums:
            return col
    return "C0"

# ==== Nhập dữ liệu & chọn phương pháp ====
results = st.text_input("Nhập dãy số Roulette (cách nhau bởi dấu cách hoặc phẩy):", "29,21,15,1,0,2,1")
method = st.radio("🔍 Chọn cách gợi ý cược", [
    "🧠 Voting kết hợp nhóm A/B/C/D + T1/T2/T3 + Cột"
    "1️⃣ Gần nhất + Nhóm ít nhất",
    "2️⃣ Gần nhất + Nhóm chưa xuất hiện gần đây",
    "3️⃣ Gợi ý theo cân bằng nhóm",
    "4️⃣ Mẫu lặp A-x-A hoặc A-A-x",
    "🔟 Markov Chain: xác suất chuyển nhóm",

])

numbers = [int(x) for x in re.findall(r'\d+', results)]
data = pd.DataFrame({"Số": numbers})
data["Nhóm"] = data["Số"].apply(find_group)
data["Tá nhóm"] = data["Số"].apply(find_dozen)
data["Cột"] = data["Số"].apply(find_column)
data["Chu kỳ 5 tay"] = (data.index // 5) + 1

# ==== Tính Markov nếu cần ====
markov_matrix = defaultdict(lambda: defaultdict(int))
markov_prob = {}
for i in range(len(data) - 1):
    from_g = data.loc[i, "Nhóm"]
    to_g = data.loc[i + 1, "Nhóm"]
    markov_matrix[from_g][to_g] += 1
for from_g, targets in markov_matrix.items():
    total = sum(targets.values())
    markov_prob[from_g] = {to_g: round(count / total, 2) for to_g, count in targets.items()}

# ==== Hàm Voting mở rộng ====
def vote_strategy(i, data, markov_prob):
    if i == 0:
        return "—"
    votes = []

    prev = data.loc[i - 1, "Nhóm"]
    prev_t = data.loc[i - 1, "Tá nhóm"]
    prev_c = data.loc[i - 1, "Cột"]
    freq = data.loc[:i - 1, "Nhóm"].value_counts()
    t_freq = data.loc[:i - 1, "Tá nhóm"].value_counts()
    c_freq = data.loc[:i - 1, "Cột"].value_counts()
    least = freq.idxmin()
    least_t = t_freq.idxmin()
    least_c = c_freq.idxmin()

    votes += [prev, least] if prev != least else [prev]
    votes += [prev_t, least_t] if prev_t != least_t else [prev_t]
    votes += [prev_c, least_c] if prev_c != least_c else [prev_c]

    recent = data.loc[max(0, i - 10):i - 1, "Nhóm"]
    missing = [g for g in group_map if g not in recent.values]
    if missing:
        votes.append(missing[0])

    prob_dict = markov_prob.get(prev, {})
    if prob_dict:
        best = max(prob_dict.items(), key=lambda x: x[1])[0]
        votes.append(best)

    vote_count = Counter(votes)
    top_votes = vote_count.most_common(2)
    return " + ".join([v[0] for v in top_votes])

# ==== Gợi ý và đánh giá ====
suggestions, hits = [], []
if method.startswith("🔬"):
    import os
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    from lstm_predictor import train_and_predict_lstm
    group_seq = data["Nhóm"].tolist()
    for i in range(len(data)):
        if i < 10:
            suggestions.append("—")
            hits.append("⚪")
        else:
            try:
                pred = train_and_predict_lstm(group_seq[:i])
                suggestions.append(pred)
                hits.append("🟢" if data.loc[i, "Nhóm"] == pred else "🔴")
            except:
                suggestions.append("Lỗi")
                hits.append("⚪")
else:
    for i in range(len(data)):
        if i == 0:
            suggestions.append("—")
            hits.append("⚪")
            continue
        current = data.loc[i, "Nhóm"]
        prev = data.loc[i - 1, "Nhóm"]
        if method.startswith("1️⃣"):
            freq = data.loc[:i - 1, "Nhóm"].value_counts()
            least = freq.idxmin()
            sugg = f"{prev} + {least}" if prev != least else prev
        elif method.startswith("2️⃣"):
            recent = data.loc[max(0, i - 10):i - 1, "Nhóm"]
            missing = [g for g in group_map if g not in set(recent)]
            sugg = f"{prev} + {missing[0]}" if missing else prev
        elif method.startswith("3️⃣"):
            freq = data.loc[:i - 1, "Nhóm"].value_counts()
            sugg = " + ".join(freq.sort_values().head(2).index)
        elif method.startswith("4️⃣"):
            sugg = data.loc[i - 2, "Nhóm"] if i >= 2 and data.loc[i - 2, "Nhóm"] == data.loc[i - 1, "Nhóm"] else prev
        elif method.startswith("🔟"):
            prob_dict = markov_prob.get(prev, {})
            sugg = max(prob_dict.items(), key=lambda x: x[1])[0] if prob_dict else prev
        elif method.startswith("🧠"):
            sugg = vote_strategy(i, data, markov_prob)
        else:
            sugg = prev
        suggestions.append(sugg)
        hits.append("🟢" if current in sugg else "🔴")


data["Gợi ý trước"] = suggestions
data["Kết quả"] = hits

# ==== Hiển thị kết quả ====
st.subheader("📋 Bảng kết quả chi tiết")
st.dataframe(data)

# ==== Hiển thị bảng Baccarat-style ====
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
# ==== Hiển thị kết quả & thống kê ====


# Biểu đồ thống kê nhóm
st.subheader("📊 Tần suất nhóm A/B/C/D")
st.bar_chart(data["Nhóm"].value_counts())

st.subheader("📊 Tần suất tá nhóm T1/T2/T3")
st.bar_chart(data["Tá nhóm"].value_counts())



latest_group = data["Nhóm"].iloc[-1]
streak = 1
for i in range(len(data) - 2, -1, -1):
    if data["Nhóm"].iloc[i] == latest_group:
        streak += 1
    else:
        break
least_group = data["Nhóm"].value_counts().idxmin()
suggested = f"{latest_group} + {least_group}" if latest_group != least_group else latest_group

st.subheader("📊 Phân tích thống kê")
st.write(f"✅ Nhóm gần nhất: **{latest_group}**")
st.write(f"📌 Độ dài chuỗi liên tiếp: **{streak} lần**")
st.write(f"🎯 Gợi ý nhóm cược: **{suggested}**")
