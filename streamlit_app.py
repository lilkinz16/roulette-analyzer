
import streamlit as st
import random

st.set_page_config(page_title="🎰 Roulette Offline Simulator", layout="centered")

st.title("🎰 Roulette Offline Simulator – 34/37 Chiến Lược Gãy")

# --- Cấu hình ---
total_rounds = st.slider("🎯 Số ván cần mô phỏng", 1000, 100000, 10000, step=1000)

st.markdown("### 🧩 Chọn chiến lược:")
strategy = st.radio("Chiến lược", ["1. Bao 34 số mỗi ván", 
                                    "2. Chỉ đánh sau khi gãy", 
                                    "3. Đánh ngược 3 số (ăn 35x)"])

st.markdown("---")

# Cài đặt các nhóm số
all_numbers = list(range(37))
bao_34 = [x for x in range(1, 35)]  # ví dụ bao số 1–34
not_covered = [x for x in all_numbers if x not in bao_34]

# Thống kê
wins = 0
losses = 0
entries = 0
gaye_sau_thua = 0
gaye_lien_tiep = 0
total_profit = 0

# Quay roulette và mô phỏng
prev_result = None
for _ in range(total_rounds):
    spin = random.choice(all_numbers)

    if strategy == "1. Bao 34 số mỗi ván":
        entries += 1
        if spin in bao_34:
            wins += 1
            total_profit += 1
        else:
            losses += 1
            total_profit -= 1

    elif strategy == "2. Chỉ đánh sau khi gãy":
        if prev_result is not None and prev_result not in bao_34:
            entries += 1
            if spin in bao_34:
                wins += 1
                total_profit += 1
            else:
                losses += 1
                total_profit -= 1
        prev_result = spin

    elif strategy == "3. Đánh ngược 3 số (ăn 35x)":
        if prev_result is not None and prev_result not in bao_34:
            entries += 1
            if spin in not_covered:
                wins += 1
                total_profit += 33  # lời 33 (ăn 35 - mất 2)
            else:
                losses += 1
                total_profit -= 3  # cược 3 số = 3u
        prev_result = spin

# Kết quả
st.markdown("## 📊 Kết quả mô phỏng")
st.write(f"🔁 Số lần vào tiền: {entries}")
st.write(f"✅ Thắng: {wins}")
st.write(f"❌ Thua: {losses}")
win_rate = wins / entries * 100 if entries else 0
st.write(f"📈 Tỷ lệ thắng: {win_rate:.2f}%")
st.write(f"💰 Lợi nhuận: {total_profit} đơn vị")
