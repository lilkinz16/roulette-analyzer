import streamlit as st

st.set_page_config(page_title="AION BACCARAT X1", layout="centered")
st.title("🎯 AION BACCARAT X1 – Dự đoán Baccarat AI")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []
if "predictions" not in st.session_state:
    st.session_state.predictions = []
if "fire_mode" not in st.session_state:
    st.session_state.fire_mode = False
if "mistake_count" not in st.session_state:
    st.session_state.mistake_count = 0

# Cài đặt chế độ "bắn"
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🚀 Bật chế độ BẮN"):
        st.session_state.fire_mode = True
    if st.button("🛑 Tắt chế độ BẮN"):
        st.session_state.fire_mode = False
with col2:
    fire_status = "ĐANG BẬT 🔥" if st.session_state.fire_mode else "ĐANG TẮT ❌"
    st.markdown(f"**Chế độ bắn:** `{fire_status}`")

# Hàm xử lý dữ liệu
def parse_streaks(sequence):
    streaks = []
    current = ''
    for ch in sequence:
        if ch == 'T':
            continue
        if current == '' or current[0] == ch:
            current += ch
        else:
            streaks.append(current)
            current = ch
    if current:
        streaks.append(current)
    return streaks

def detect_pattern_type(streaks):
    if len(streaks) < 2:
        return None
    last_two = streaks[-2:]
    if len(last_two[0]) == len(last_two[1]):
        return "TYPE_1"
    elif len(last_two[0]) >= 2 and len(last_two[1]) == 1:
        return "TYPE_2"
    return None

def suggest_next_move(pattern_type):
    if pattern_type == "TYPE_1":
        return ("B", 70, "Phát hiện mẫu cặp cân bằng (BP)")
    elif pattern_type == "TYPE_2":
        return ("P", 75, "Chu kỳ Cutpoint-1 PPB đang diễn ra")
    else:
        return (None, 50, "⏩ Bỏ qua – Không đủ tự tin để dự đoán")

def get_bet_amount(mistake_count):
    base = 20
    return base * (2 ** mistake_count) if mistake_count < 4 else "DỪNG LẠI"

# Giao diện nhập liệu
with st.form("predict_form"):
    input_result = st.text_input("🔢 Nhập kết quả thật của ván gần nhất (B / P / T)", max_chars=1).upper()
    submitted = st.form_submit_button("📥 Gửi và dự đoán ván kế")

if submitted and input_result in ["B", "P", "T"]:
    # Lấy chuỗi kết quả
    sequence = ''.join([x["real"] for x in st.session_state.history])
    streaks = parse_streaks(sequence)
    pattern_type = detect_pattern_type(streaks)
    move, confidence, reason = suggest_next_move(pattern_type)

    # Xác định có nên dự đoán không
    if st.session_state.fire_mode and confidence < 85:
        prediction = None
        outcome = "⏩ Bỏ qua"
        symbol = "⏩"
    elif confidence >= 65:
        prediction = move
        if input_result == prediction:
            outcome = "✅ ĐÚNG"
            symbol = "⚪"
            st.session_state.mistake_count = 0
        elif input_result == "T":
            outcome = "🟢 HÒA"
            symbol = "🟢"
        else:
            outcome = "❌ SAI"
            symbol = "🟠"
            st.session_state.mistake_count += 1
    else:
        prediction = None
        outcome = "⏩ Bỏ qua"
        symbol = "⏩"

    # Ghi vào lịch sử
    st.session_state.history.append({
        "real": input_result,
        "predict": prediction,
        "conf": confidence,
        "outcome": outcome,
        "symbol": symbol
    })

    # Tự động reset nếu sai quá 4 lần
    if st.session_state.mistake_count >= 4:
        st.warning("❌ Đã sai liên tiếp 4 lần – dừng cược và tổng kết!")
        st.session_state.fire_mode = False
        st.session_state.mistake_count = 0

# Thống kê
total = len(st.session_state.history)
win = sum(1 for i in st.session_state.history if i["outcome"] == "✅ ĐÚNG")
lose = sum(1 for i in st.session_state.history if i["outcome"] == "❌ SAI")
tie = sum(1 for i in st.session_state.history if i["outcome"] == "🟢 HÒA")
skip = sum(1 for i in st.session_state.history if i["outcome"] == "⏩ Bỏ qua")
accuracy = round((win / (win + lose)) * 100, 2) if (win + lose) > 0 else 0

# Hiển thị kết quả
st.markdown("---")
st.markdown("## 📊 Kết quả phân tích")

dna = "".join([h["symbol"] for h in st.session_state.history])
st.markdown(f"🧬 **DNA kết quả:** `{dna}`")

for idx, h in enumerate(st.session_state.history, 1):
    predict_text = f"{h['predict']} ({h['conf']}%)" if h["predict"] else "⏩ Bỏ qua"
    st.markdown(f"Ván {idx}: Dự đoán: `{predict_text}` – Kết quả: `{h['real']}` → **{h['outcome']}**")

st.markdown("---")
st.markdown(f"✅ **Tổng ván:** {total} | 🏆 Đúng: {win} | ❌ Sai: {lose} | 🟢 Hòa: {tie} | ⏩ Bỏ qua: {skip}")
st.markdown(f"🎯 **Tỷ lệ chính xác:** `{accuracy}%`")
st.markdown(f"💰 **Tiền cược đề xuất:** `{get_bet_amount(st.session_state.mistake_count)}₫`")

st.caption("🧠 AION BACCARAT X1 – Phiên bản demo trên Streamlit. Bạn có thể phát triển thêm AI, vẽ biểu đồ, hoặc tải dữ liệu.")
