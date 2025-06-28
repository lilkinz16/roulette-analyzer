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
    st.subheader("📥 Nhập & lưu cầu mới")
    name = st.text_input("🔖 Tên chuỗi cầu (VD: VIP_19h)")
    seq_input = st.text_area("🎲 Nhập chuỗi tay (B/P, cách hoặc liền nhau)", height=100)

    if st.button("💾 Lưu"):
        sequence = seq_input.replace(" ", "").upper()
        if set(sequence).issubset({"B", "P"}) and len(sequence) > 0:
            data[name] = sequence
            save_data(data)
            st.success(f"✅ Đã lưu chuỗi '{name}'!")
        else:
            st.error("❌ Chỉ được dùng ký tự B và P.")

# ----- TRA CỨU -----
elif menu == "Tra cứu cầu":
    st.subheader("🔍 Tìm cầu theo chuỗi tay")
    search_seq = st.text_input("🧩 Nhập chuỗi tay cần tra (tối thiểu 2 ký tự):")

    matched = []
    seq = search_seq.replace(" ", "").upper()

    if len(seq) >= 2 and set(seq).issubset({"B", "P"}):
        for k, v in data.items():
            if v.startswith(seq):
                matched.append((k, v))

        if matched:
            st.success(f"🔎 Có {len(matched)} cầu có phần đầu giống: {seq}")
            selected = st.selectbox("📌 Chọn cầu để phân tích", [m[0] for m in matched])
            st.code(data[selected])
            stats = analyze_sequence(data[selected])
            st.subheader("📊 Phân tích:")
            for k, v in stats.items():
                st.write(f"- {k}: {v}")
        else:
            st.warning("❌ Không tìm thấy chuỗi nào khớp phần đầu.")
    elif seq and not set(seq).issubset({"B", "P"}):
        st.error("❌ Chỉ được nhập B và P.")
    else:
        st.info("ℹ️ Nhập ít nhất 2 ký tự để bắt đầu tìm.")

# ----- XOÁ -----
elif menu == "Xoá cầu":
    st.subheader("🗑 Xoá chuỗi cầu đã lưu")
    if not data:
        st.warning("⚠️ Không có cầu để xoá.")
    else:
        del_key = st.selectbox("🗂 Chọn cầu để xoá", list(data.keys()))
        if st.button("❌ Xoá cầu này"):
            del data[del_key]
            save_data(data)
            st.success(f"✅ Đã xoá '{del_key}'!")
