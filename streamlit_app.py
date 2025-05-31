
import streamlit as st
st.set_page_config(page_title="Phân Tích Roulette", layout="centered")

import pandas as pd
import matplotlib.pyplot as plt
import re
from io import BytesIO
from collections import defaultdict

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
method = st.radio("🔍 Chọn cách gợi ý cược") ,
    "1️⃣ Gần nhất + Nhóm ít nhất",
    "2️⃣ Gần nhất + Nhóm chưa xuất hiện gần đây",
    "3️⃣ Gợi ý theo cân bằng nhóm",
    "4️⃣ Mẫu lặp A-x-A hoặc A-A-x",
    "🔟 Markov Chain: xác suất chuyển nhóm",
"🔬 Dự đoán bằng AI LSTM",
    "🧠 AI Voting: tổng hợp nhiều chiến lược",


# Xử lý đầu vào
numbers = [int(x) for x in re.findall(r'\d+', results)]
data = pd.DataFrame({"Số": numbers})
data["Nhóm"] = data["Số"].apply(find_group)
data["Chu kỳ 5 tay"] = (data.index // 5) + 1

# Tính toán Markov nếu cần
markov_matrix = defaultdict(lambda: defaultdict(int))
if method.startswith("🔟") and len(data) > 1:
    for i in range(len(data) - 1):
        from_g = data.loc[i, "Nhóm"]
        to_g = data.loc[i + 1, "Nhóm"]
        markov_matrix[from_g][to_g] += 1

    # Chuyển sang xác suất
    markov_prob = {}
    for from_g, targets in markov_matrix.items():
        total = sum(targets.values())
        markov_prob[from_g] = {to_g: round(count / total, 2) for to_g, count in targets.items()}


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

    elif method.startswith("🔟"):
        prev = data.loc[i - 1, "Nhóm"]
        prob_dict = markov_prob.get(prev, {})
        if prob_dict:
            best = max(prob_dict.items(), key=lambda x: x[1])[0]
            sugg = best
        else:
            sugg = prev

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

# Nếu chọn Markov, hiển thị ma trận
if method.startswith("🔟") and markov_prob:
    st.subheader("📊 Ma trận chuyển xác suất (Markov Chain)")
    st.write(pd.DataFrame(markov_prob).fillna(0))



# 🚦 Phân tích cầu nâng cao (phát hiện mẫu lặp)

def detect_patterns(group_sequence):
    patterns = {
        "Cầu đuôi (lặp)": 0,
        "Cầu nhảy": 0,
        "Cầu xen kẽ": 0,
    }
    for i in range(2, len(group_sequence)):
        g0 = group_sequence[i - 2]
        g1 = group_sequence[i - 1]
        g2 = group_sequence[i]

        # Cầu đuôi: A-A-A
        if g0 == g1 == g2:
            patterns["Cầu đuôi (lặp)"] += 1
        # Cầu nhảy: A-x-A
        elif g0 == g2 and g0 != g1:
            patterns["Cầu nhảy"] += 1
        # Cầu xen kẽ: A-B-A-B
        elif i >= 3 and group_sequence[i - 3] == g2 and group_sequence[i - 2] == g1 and g0 != g1:
            patterns["Cầu xen kẽ"] += 1
    return patterns

# 🎛 Dashboard & Thống kê Winrate cá nhân

if "history" not in st.session_state:
    st.session_state.history = []

# Lưu dữ liệu nếu có kết quả hợp lệ
if len(data) > 0 and "Kết quả" in data.columns:
    last_row = data.iloc[-1]
    st.session_state.history.append({
        "Số": last_row["Số"],
        "Nhóm": last_row["Nhóm"],
        "Gợi ý": last_row["Gợi ý trước"],
        "Kết quả": last_row["Kết quả"]
    })

# Biểu đồ & thống kê
if st.session_state.history:
    st.subheader("📊 Dashboard Cá Nhân (phiên hiện tại)")

    hist_df = pd.DataFrame(st.session_state.history)
    winrate = hist_df["Kết quả"].value_counts(normalize=True).get("🟢", 0)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🎯 Số lần đúng", int((winrate or 0) * len(hist_df)))
    with col2:
        st.metric("❌ Số lần sai", int(len(hist_df) - (winrate or 0) * len(hist_df)))

    st.write("📈 Lịch sử dự đoán:")
    st.dataframe(hist_df.tail(20), use_container_width=True)

    # Biểu đồ tròn Winrate
    fig2, ax2 = plt.subplots()
    hist_df["Kết quả"].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)



# 🧠 Voting chiến lược gợi ý nhóm
def vote_strategy(i, data, markov_prob):
    if i == 0:
        return "—"
    votes = []

    prev = data.loc[i - 1, "Nhóm"]
    current = data.loc[i, "Nhóm"]

    # 1️⃣ Gần nhất + ít nhất
    freq = data.loc[:i - 1, "Nhóm"].value_counts()
    least = freq.idxmin()
    if prev != least:
        votes += [prev, least]
    else:
        votes += [prev]

    # 2️⃣ Nhóm chưa ra gần đây
    recent = data.loc[max(0, i - 10):i - 1, "Nhóm"]
    missing = [g for g in group_map if g not in set(recent)]
    if missing:
        votes += [missing[0]]

    # 3️⃣ Nhóm ít ra nhất
    sorted_freq = freq.sort_values()
    votes += sorted_freq.head(2).index.tolist()

    # 4️⃣ Cầu A-A hoặc A-x-A
    if i >= 2 and data.loc[i - 2, "Nhóm"] == data.loc[i - 1, "Nhóm"]:
        votes += [data.loc[i - 1, "Nhóm"]]

    elif i >= 2 and data.loc[i - 2, "Nhóm"] == data.loc[i, "Nhóm"]:
        votes += [data.loc[i - 2, "Nhóm"]]

    # 🔟 Markov
    prob_dict = markov_prob.get(prev, {})
    if prob_dict:
        best = max(prob_dict.items(), key=lambda x: x[1])[0]
        votes += [best]

    # Đếm số phiếu
    from collections import Counter
    vote_count = Counter(votes)
    top_votes = vote_count.most_common(1)[0][0]
    return top_votes

# Nếu chọn Voting
if method.startswith("🧠"):
    suggestions = []
    hits = []
    for i in range(len(data)):
        sugg = vote_strategy(i, data, markov_prob)
        suggestions.append(sugg)
        hit = "🟢" if data.loc[i, "Nhóm"] in sugg else "🔴"
        hits.append(hit)
    data["Gợi ý trước"] = suggestions
    data["Kết quả"] = hits



# Tích hợp LSTM vào streamlit app
elif method.startswith("🔬"):
    import os
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Tắt cảnh báo TensorFlow
    from lstm_predictor import train_and_predict_lstm

    group_seq = data["Nhóm"].tolist()
    predictions = []
    results = []
    for i in range(len(data)):
        if i < 10:
            predictions.append("—")
            results.append("⚪")
        else:
            try:
                pred = train_and_predict_lstm(group_seq[:i])
                predictions.append(pred)
                hit = "🟢" if data.loc[i, "Nhóm"] == pred else "🔴"
                results.append(hit)
            except Exception as e:
                predictions.append("Lỗi")
                results.append("⚪")
    data["Gợi ý trước"] = predictions
    data["Kết quả"] = results

# Nếu chọn Markov, hiển thị ma trận
if method.startswith("🔟") and markov_prob:
    st.subheader("📊 Ma trận chuyển xác suất (Markov Chain)")
    st.write(pd.DataFrame(markov_prob).fillna(0))
