import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

st.set_page_config(page_title="AION BACCARAT X1", layout="centered")
st.title("🎯 AION BACCARAT X1 – AI Dự đoán Baccarat toàn diện")

# === Session State ===
if "history" not in st.session_state:
    st.session_state.history = []
if "fire_mode" not in st.session_state:
    st.session_state.fire_mode = False
if "mistake_count" not in st.session_state:
    st.session_state.mistake_count = 0
if "model" not in st.session_state:
    st.session_state.model = RandomForestClassifier()
    st.session_state.encoder = LabelEncoder()
    st.session_state.X_train = []
    st.session_state.y_train = []

# === FIRE MODE ===
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🚀 Bật chế độ BẮN"):
        st.session_state.fire_mode = True
    if st.button("🛑 Tắt chế độ BẮN"):
        st.session_state.fire_mode = False
with col2:
    status = "ĐANG BẬT 🔥" if st.session_state.fire_mode else "ĐANG TẮT ❌"
    st.markdown(f"**Chế độ bắn:** `{status}`")

# === Pattern Detection Logic ===
def detect_pattern(streaks):
    if len(streaks) < 2:
        return None
    a, b = streaks[-2:]
    la, lb = len(a), len(b)
    if la == lb:
        return "TYPE_1"
    if la >= 2 and lb == 1:
        return "TYPE_2"
    if la >= 3 and lb == 2:
        return "TYPE_3"
    if la >= 4 and lb == 3:
        return "TYPE_4"
    if la >= 5 and lb == 4:
        return "TYPE_5"
    if la >= 6 and lb == 5:
        return "TYPE_6"
    return None

def parse_streaks(seq):
    streaks = []
    current = ""
    for ch in seq:
        if ch == "T": continue
        if current == "" or current[0] == ch:
            current += ch
        else:
            streaks.append(current)
            current = ch
    if current: streaks.append(current)
    return streaks

# === Tie Probability Detection ===
def tie_probability(seq):
    tie_count = seq.count("T")
    if len(seq) == 0:
        return 0
    return round((tie_count / len(seq)) * 100, 2)

# === Bet Amount by Mistake Count ===
def bet_amount(n):
    base = 20
    return base * (2 ** n) if n < 4 else "STOP"

# === Machine Learning Model Training ===
def update_model():
    if len(st.session_state.X_train) >= 10:
        X = st.session_state.encoder.fit_transform(st.session_state.X_train).reshape(-1, 1)
        y = np.array(st.session_state.y_train)
        st.session_state.model.fit(X, y)

def predict_ml(sequence):
    if len(sequence) < 5:
        return None, 0
    seq5 = sequence[-5:]
    val = st.session_state.encoder.transform([seq5])[0]
    prob = st.session_state.model.predict_proba([[val]])[0]
    labels = st.session_state.model.classes_
    best_idx = np.argmax(prob)
    return labels[best_idx], round(prob[best_idx] * 100, 2)

# === Input Form ===
with st.form("predict_form"):
    result = st.text_input("🔢 Nhập kết quả ván gần nhất (B/P/T):", max_chars=1).upper()
    submitted = st.form_submit_button("📥 Gửi và xử lý")

# === Handle Submission ===
if submitted and result in ["B", "P", "T"]:
    full_seq = ''.join([x["real"] for x in st.session_state.history])
    streaks = parse_streaks(full_seq)
    pattern = detect_pattern(streaks)

    # AI dự đoán bằng rule
    if pattern in ["TYPE_1", "TYPE_3", "TYPE_5"]:
        prediction = "B"
        confidence = 70
        reason = f"Pattern {pattern} → B"
    elif pattern in ["TYPE_2", "TYPE_4", "TYPE_6"]:
        prediction = "P"
        confidence = 75
        reason = f"Pattern {pattern} → P"
    else:
        prediction = None
        confidence = 50
        reason = "Không rõ pattern"

    # Dự đoán Tie
    tie_chance = tie_probability(full_seq)
    tie_warn = tie_chance > 55

    # ML dự đoán
    if len(st.session_state.X_train) >= 10:
        ml_pred, ml_conf = predict_ml(full_seq)
    else:
        ml_pred, ml_conf = None, 0

    # FIRE MODE check
    if st.session_state.fire_mode and confidence < 85:
        prediction = None
        outcome = "⏩ Bỏ qua"
        symbol = "⏩"
    elif prediction:
        if result == prediction:
            outcome = "✅ ĐÚNG"
            symbol = "⚪"
            st.session_state.mistake_count = 0
        elif result == "T":
            outcome = "🟢 HÒA"
            symbol = "🟢"
        else:
            outcome = "❌ SAI"
            symbol = "🟠"
            st.session_state.mistake_count += 1
    else:
        outcome = "⏩ Bỏ qua"
        symbol = "⏩"

    # Lưu lịch sử
    st.session_state.history.append({
        "real": result,
        "predict": prediction,
        "conf": confidence,
        "outcome": outcome,
        "symbol": symbol,
        "tie_warn": tie_warn,
        "ml_pred": ml_pred,
        "ml_conf": ml_conf
    })

    # Thêm dữ liệu huấn luyện
    if len(full_seq) >= 5:
        st.session_state.X_train.append(full_seq[-5:])
        st.session_state.y_train.append(result)
        update_model()

# === Hiển thị Kết quả ===
st.markdown("---")
st.subheader("📊 Thống kê & Kết quả")

total = len(st.session_state.history)
wins = sum(1 for h in st.session_state.history if h["outcome"] == "✅ ĐÚNG")
losses = sum(1 for h in st.session_state.history if h["outcome"] == "❌ SAI")
ties = sum(1 for h in st.session_state.history if h["outcome"] == "🟢 HÒA")
skips = sum(1 for h in st.session_state.history if h["outcome"] == "⏩ Bỏ qua")
acc = round((wins / (wins + losses)) * 100, 2) if (wins + losses) > 0 else 0

dna = "".join([h["symbol"] for h in st.session_state.history])
st.markdown(f"🧬 DNA kết quả: `{dna}`")
st.markdown(f"✅ Tổng: {total} | 🏆 Đúng: {wins} | ❌ Sai: {losses} | 🟢 Hòa: {ties} | ⏩ Bỏ qua: {skips}")
st.markdown(f"🎯 Chính xác: `{acc}%`")
st.markdown(f"💰 Cược đề xuất: `{bet_amount(st.session_state.mistake_count)}`")

# Hiển thị cảnh báo Tie
if st.session_state.history and st.session_state.history[-1]["tie_warn"]:
    st.warning("🟢 CẢNH BÁO: Xác suất HÒA cao hơn 55%!")

# Hiển thị bảng kết quả
for idx, h in enumerate(st.session_state.history, 1):
    ml_info = f" | AI dự đoán: `{h['ml_pred']}` ({h['ml_conf']}%)" if h["ml_pred"] else ""
    st.markdown(f"Ván {idx}: `{h['real']}` → Dự đoán: `{h['predict']}` ({h['conf']}%) → **{h['outcome']}**{ml_info}")

# === Biểu đồ kết quả ===
if total > 0:
    df = pd.DataFrame(st.session_state.history)
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    df['outcome'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax[0])
    ax[0].set_title("Phân loại kết quả")
    ax[0].set_ylabel("")

    ax[1].plot(range(1, total+1), [1 if o == "✅ ĐÚNG" else 0 for o in df["outcome"]], marker='o')
    ax[1].set_title("Kết quả từng ván")
    ax[1].set_xlabel("Ván")
    ax[1].set_ylabel("1 = Đúng")

    st.pyplot(fig)

st.caption("🔧 Phiên bản nâng cấp hoàn chỉnh AION BACCARAT X1 – AI | Streamlit | ML | Charts")
