import streamlit as st
import json
import os

DATA_FILE = "baccarat_data.json"

# Load dữ liệu
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Phân tích chuỗi
def analyze_sequence(seq):
    b_count = seq.count("B")
    p_count = seq.count("P")
    total = len(seq)

    def max_streak(char):
        streak = max_s = 0
        for c in seq:
            if c == char:
                streak += 1
                max_s = max(max_s, streak)
            else:
                streak = 0
        return max_s

    return {
        "Tổng ván": total,
        "Banker (%)": round(100 * b_count / total, 2),
        "Player (%)": round(100 * p_count / total, 2),
        "Chuỗi dài nhất B": max_streak("B"),
        "Chuỗi dài nhất P": max_streak("P"),
    }

# Giao diện
st.title("🎴 Baccarat Cầu Tracker (1000 cầu)")

data = load_data()

st.sidebar.markdown("## 📂 Chức năng")
menu = st.sidebar.selectbox("Chọn", ["Tra cứu cầu"])

if menu == "Tra cứu cầu":
    if not data:
        st.warning("⚠️ Chưa có dữ liệu.")
    else:
        search_key = st.text_input("🔍 Nhập tên cầu cần tìm (ví dụ: Cau_0050)")
        filtered_keys = [k for k in data.keys() if search_key.lower() in k.lower()]

        if filtered_keys:
            name = st.selectbox("🗂 Kết quả khớp", filtered_keys)
            st.code(data[name])
            stats = analyze_sequence(data[name])
            st.subheader("📊 Phân tích:")
            for k, v in stats.items():
                st.write(f"- {k}: {v}")
        else:
            st.info("❕ Không tìm thấy tên cầu.")
