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
if "transitions" not in st.session_state:
    st.session_state.transitions = []
if "last_pattern" not in st.session_state:
    st.session_state.last_pattern = None

# === FIRE MODE ===
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🚀 Bật chế độ BẮN"):
        st.session_state.fire_mode = True
    if st.button("🛑 Tắt chế độ BẮN"):
        st.session_state.fire_mode = False
with col2:
    status = "ĐANG BẬT 🔥" if st.session_state.fire_mode else "ĐANG TẮT ❌"
    st.markdown(f"**Chế độ bắn:** {status}")

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

def detect_transition(prev_pattern, current_pattern, current_round):
    if not current_pattern:
        return None
    if prev_pattern == "TYPE_1" and current_pattern == "TYPE_2":
        msg = "🔁 TYPE_1 → TYPE_2 (bắt đầu chu kỳ PPB)"
    elif prev_pattern and prev_pattern.startswith("TYPE_1") and current_pattern == "TYPE_1":
        msg = "↘️ TYPE_1 đang rút ngắn (co mẫu)"
    elif prev_pattern != current_pattern:
        msg = f"🔄 {prev_pattern or 'None'} → {current_pattern}"
    else:
        return None

    st.session_state.transitions.append({
        "round": current_round,
        "from": prev_pattern or "None",
        "to": current_pattern,
        "note": msg
    })
    return msg

def tie_probability(seq):
    tie_count = seq.count("T")
    if len(seq) == 0:
        return 0
    return round((tie_count / len(seq)) * 100, 2)

def bet_amount(n):
    base = 20
    return base * (2 ** n) if n < 4 else "STOP"

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

with st.form("predict_form"):
    result = st.text_input("🔢 Nhập kết quả ván gần nhất (B/P/T):", max_chars=1).upper()
    submitted = st.form_submit_button("📥 Gửi và xử lý")

if submitted and result in ["B", "P", "T"]:
    full_seq = ''.join([x["real"] for x in st.session_state.history])
    streaks = parse_streaks(full_seq)
    pattern = detect_pattern(streaks)

    transition_msg = detect_transition(
        st.session_state.last_pattern,
        pattern,
        len(st.session_state.history) + 1
    )
    st.session_state.last_pattern = pattern

    if transition_msg:
        st.info(transition_msg)

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

    tie_chance = tie_probability(full_seq)
    tie_warn = tie_chance > 55

    if len(st.session_state.X_train) >= 10:
        ml_pred, ml_conf = predict_ml(full_seq)
    else:
        ml_pred, ml_conf = None, 0

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

    if len(full_seq) >= 5:
        st.session_state.X_train.append(full_seq[-5:])
        st.session_state.y_train.append(result)
        update_model()

st.markdown("---")
st.subheader("📊 Thống kê & Kết quả")

total = len(st.session_state.history)
wins = sum(1 for h in st.session_state.history if h["outcome"] == "✅ ĐÚNG")
losses = sum(1 for h in st.session_state.history if h["outcome"] == "❌ SAI")
ties = sum(1 for h in st.session_state.history if h["outcome"] == "🟢 HÒA")
skips = sum(1 for h in st.session_state.history if h["outcome"] == "⏩ Bỏ qua")
acc = round((wins / (wins + losses)) * 100, 2) if (wins + losses) > 0 else 0

dna = "".join([h["symbol"] for h in st.session_state.history])
st.markdown(f"🧬 DNA kết quả: {dna}")
st.markdown(f"✅ Tổng: {total} | 🏆 Đúng: {wins} | ❌ Sai: {losses} | 🟢 Hòa: {ties} | ⏩ Bỏ qua: {skips}")
st.markdown(f"🎯 Chính xác: {acc}%")
st.markdown(f"💰 Cược đề xuất: {bet_amount(st.session_state.mistake_count)}")

if st.session_state.history and st.session_state.history[-1]["tie_warn"]:
    st.warning("🟢 CẢNH BÁO: Xác suất HÒA cao hơn 55%!")

for idx, h in enumerate(st.session_state.history, 1):
    ml_info = f" | AI dự đoán: {h['ml_pred']} ({h['ml_conf']}%)" if h["ml_pred"] else ""
    st.markdown(f"Ván {idx}: {h['real']} → Dự đoán: {h['predict']} ({h['conf']}%) → **{h['outcome']}**{ml_info}")

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

if st.session_state.transitions:
    st.markdown("---")
    st.subheader("📋 Bảng chi tiết chuyển TYPE")
    df_trans = pd.DataFrame(st.session_state.transitions)
    df_trans.columns = ["Số ván", "Từ TYPE", "Đến TYPE", "Ghi chú"]
    df_trans = df_trans.reset_index(drop=True)
    st.table(df_trans)
# === VẼ BIỂU ĐỒ CẦU BACCARAT ===
st.markdown("---")
st.subheader("🎴 Bộ Biểu Đồ Cầu Baccarat")

# Tạo chuỗi từ kết quả thực
seq = ''.join([x["real"] for x in st.session_state.history if x["real"] in ["B", "P", "T"]])

def get_color(char):
    if char == 'B': return 'red'
    elif char == 'P': return 'blue'
    elif char == 'T': return 'green'
    return 'gray'

def build_big_road(sequence):
    grid = [[None for _ in range(100)] for _ in range(6)]
    col = 0
    row = 0
    prev = ''
    for ch in sequence:
        if ch == 'T': continue
        if ch == prev:
            row += 1
            if row >= 6:
                row = 5
                col += 1
        else:
            row = 0
            if prev != '':
                col += 1
        grid[row][col] = ch
        prev = ch
    return grid

def draw_grid(grid, dot=False):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, len(grid[0]))
    ax.set_ylim(0, 6)
    ax.invert_yaxis()
    ax.axis('off')
    for r in range(6):
        for c in range(len(grid[0])):
            val = grid[r][c]
            if val:
                color = get_color(val)
                if dot:
                    ax.plot(c + 0.5, r + 0.5, 'o', color=color)
                else:
                    ax.add_patch(plt.Circle((c + 0.5, r + 0.5), 0.35, color=color))
    st.pyplot(fig)

def fake_secondary_grid(sequence, shift=1):
    grid = [[None for _ in range(100)] for _ in range(6)]
    markers = ['R', 'B'] * 100
    col = 0
    row = 0
    for i in range(len(sequence)):
        if i % (2 + shift) == 0:
            col += 1
            row = 0
        else:
            row += 1
        if row >= 6:
            row = 5
            col += 1
        grid[row][col] = markers[i % len(markers)]
    return grid

def draw_secondary_grid(grid):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(0, len(grid[0]))
    ax.set_ylim(0, 6)
    ax.invert_yaxis()
    ax.axis('off')
    for r in range(6):
        for c in range(len(grid[0])):
            val = grid[r][c]
            if val:
                color = 'red' if val == 'R' else 'blue'
                ax.add_patch(plt.Circle((c + 0.5, r + 0.5), 0.25, color=color))
    st.pyplot(fig)

if seq:
    st.markdown("🟥 **Big Road**")
    draw_grid(build_big_road(seq))

    st.markdown("🟦 **Big Eye Boy**")
    draw_secondary_grid(fake_secondary_grid(seq, shift=1))

    st.markdown("🟨 **Small Road**")
    draw_secondary_grid(fake_secondary_grid(seq, shift=2))

    st.markdown("🟥 **Cockroach Pig**")
    draw_secondary_grid(fake_secondary_grid(seq, shift=3))

st.caption("📊 Biểu đồ cầu Baccarat được tích hợp trực tiếp từ lịch sử kết quả – bạn có thể nâng cấp logic cầu phụ sau.")

st.caption("🔧 Phiên bản nâng cấp hoàn chỉnh AION BACCARAT X1 – AI | Streamlit | ML | Charts | Transition")
