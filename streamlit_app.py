import streamlit as st
import json
import os
import random

DATA_FILE = "baccarat_data.json"

# ------------------------ DỮ LIỆU BAN ĐẦU ------------------------
def generate_sequences(n=1000, length=20):
    data = {}
    for i in range(1, n + 1):
        name = f"Cau_{i:04d}"
        sequence = ''.join(random.choices(['B', 'P'], k=length))
        data[name] = sequence
    return data

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        data = generate_sequences()
        save_data(data)
        return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ------------------------ PHÂN TÍCH ------------------------
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

# ------------------------ GIAO DIỆN ------------------------
st.set_page_config(page_title="Baccarat Cầu Tracker", layout="centered")
st.title("🎴 Baccarat Cầu Tracker (Full: tạo + lưu + xoá + tra cứu chuỗi)")

data = load_data()

menu = st.sidebar.selectbox("📂 Chọn chức năng", ["Nhập cầu mới", "Tra cứu cầu", "Xoá cầu"])

# ----- NHẬP -----
if menu == "Nhập cầu mới":
    st.subheader("📥 N
