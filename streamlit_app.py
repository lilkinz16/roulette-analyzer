import streamlit as st

st.set_page_config(page_title="AION BACCARAT X1", layout="centered")

st.title("🎯 AION BACCARAT X1 – Dự đoán Baccarat bằng AI")

# Nhập chuỗi kết quả
user_input = st.text_input("🔢 Nhập chuỗi kết quả gần nhất (ví dụ: BPPBT)", max_chars=100).upper()

def parse_streaks(sequence):
    streaks = []
    current = ''
    for ch in sequence:
        if ch == 'T':
            continue  # Bỏ qua Tie
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
        return "TYPE_1"  # Balanced Pairing
    elif len(last_two[0]) >= 2 and len(last_two[1]) == 1:
        return "TYPE_2"  # Cutpoint-1
    return None

def suggest_next_move(pattern_type):
    if pattern_type == "TYPE_1":
        return ("B", 70, "Phát hiện mẫu cặp cân bằng (BP)")
    elif pattern_type == "TYPE_2":
        return ("P", 75, "Chu kỳ Cutpoint-1 PPB đang diễn ra")
    else:
        return (None, 50, "⏩ Bỏ qua – Không đủ tự tin để dự đoán")

# Khi người dùng đã nhập chuỗi
if user_input:
    st.markdown("### 📊 Phân tích:")
    streaks = parse_streaks(user_input)
    pattern_type = detect_pattern_type(streaks)
    next_move, confidence, reason = suggest_next_move(pattern_type)

    st.markdown(f"🧬 **Kết quả trước:** `{user_input}`")
    st.markdown(f"🧩 **Mẫu phát hiện:** `{pattern_type or 'Không xác định'}`")

    if confidence >= 65 and next_move:
        icon = "🔴" if next_move == "B" else "🔵"
        st.success(f"🔍 **Dự đoán tiếp theo:** {icon} `{next_move}` – {confidence}%")
        st.markdown(f"🔮 **Lý do:** {reason}")
    else:
        st.warning("⏩ Bỏ qua – Độ tự tin dưới 65%")

else:
    st.info("⏳ Vui lòng nhập chuỗi kết quả để bắt đầu dự đoán.")

st.markdown("---")
st.caption("🤖 Phiên bản đơn giản hóa từ AI AION BACCARAT X1 – dành cho thử nghiệm chiến lược đọc cầu")
