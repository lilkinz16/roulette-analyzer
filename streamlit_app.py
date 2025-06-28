import streamlit as st
import json
import os

DATA_FILE = "baccarat_data.json"

# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Thống kê cơ bản
def analyze_sequence(seq):
    b_count = seq.count("B")
    p_count = seq.count("P")
    total = len(seq)

    def max_streak(char):
        streak, max_s = 0, 0
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

# UI
st.title("🎴 Baccarat Cầu Tracker")

data = load_data()

menu = st.sidebar.selectbox("Chọn chức năng", ["Nhập cầu mới", "Tra cứu cầu cũ"])

if menu == "Nhập cầu mới":
    name = st.text_input("🔖 Đặt tên chuỗi cầu (VD: VIP 19h)")
    seq_input = st.text_area("🎲 Nhập cầu (B hoặc P, viết liền hoặc cách nhau)", height=100)

    if st.button("📥 Lưu cầu"):
        sequence = seq_input.replace(" ", "").upper()
        if set(sequence).issubset({"B", "P"}) and len(sequence) > 0:
            data[name] = sequence
            save_data(data)
            st.success(f"Đã lưu chuỗi '{name}'!")
        else:
            st.error("Chỉ nhập ký tự B và P, không có ký tự lạ!")

elif menu == "Tra cứu cầu cũ":
    if not data:
        st.warning("Chưa có dữ liệu nào được lưu.")
    else:
        name = st.selectbox("🗂 Chọn tên chuỗi cầu", list(data.keys()))
        st.code(data[name])
        stats = analyze_sequence(data[name])
        st.subheader("📊 Phân tích:")
        for k, v in stats.items():
            st.write(f"- {k}: {v}")
