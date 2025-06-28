import streamlit as st
import json
import os
import random

DATA_FILE = "baccarat_data.json"

# ----- DỮ LIỆU BAN ĐẦU (1000 cầu mẫu) -----
def generate_sequences(n=1000, length=20):
    data = {}
    for i in range(1, n + 1):
        name = f"Cau_{i:04d}"
        sequence = ''.join(random.choices(['B', 'P'], k=length))
        data[name] = sequence
    return data

# ----- ĐỌC / GHI FILE -----
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        # Tạo dữ liệu ban đầu nếu chưa có file
        data = generate_sequences()
        save_data(data)
        return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ----- THỐNG KÊ -----
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

# ----- GIAO DIỆN -----
st.title("🎴 Baccarat Cầu Tracker (1000 cầu + thêm + xoá)")

data = load_data()

menu = st.sidebar.selectbox("Chọn chức năng", ["Tra cứu cầu", "Nhập cầu mới", "Xoá cầu"])

# ----- NHẬP CẦU -----
if menu == "Nhập cầu mới":
    st.subheader("📥 Nhập & lưu cầu mới")
    name = st.text_input("🔖 Tên chuỗi cầu (ví dụ: VIP_19h)")
    seq_input = st.text_area("🎲 Nhập cầu (B/P, cách nhau hoặc viết liền)", height=100)

    if st.button("💾 Lưu"):
        sequence = seq_input.replace(" ", "").upper()
        if set(sequence).issubset({"B", "P"}) and len(sequence) > 0:
            data[name] = sequence
            save_data(data)
            st.success(f"✅ Đã lưu chuỗi '{name}'!")
        else:
            st.error("❌ Chỉ nhập ký tự B và P, không có ký tự lạ!")

# ----- TRA CỨU -----
elif menu == "Tra cứu cầu":
    st.subheader("🔍 Tra cứu & phân tích")
    search_key = st.text_input("Nhập tên cầu cần tìm (VD: Cau_0010 hoặc VIP...)")
    filtered = [k for k in data if search_key.lower() in k.lower()]

    if filtered:
        name = st.selectbox("🗂 Danh sách khớp:", filtered)
        st.code(data[name])
        stats = analyze_sequence(data[name])
        st.subheader("📊 Phân tích:")
        for k, v in stats.items():
            st.write(f"- {k}: {v}")
    else:
        st.info("⛔ Không tìm thấy kết quả phù hợp.")

# ----- XOÁ CẦU -----
elif menu == "Xoá cầu":
    st.subheader("🗑 Xoá chuỗi cầu đã lưu")
    if not data:
        st.warning("⚠️ Không có dữ liệu để xoá.")
    else:
        del_key = st.selectbox("🗂 Chọn tên chuỗi cầu để xoá", list(data.keys()))
        if st.button("❌ Xoá chuỗi này"):
            del data[del_key]
            save_data(data)
            st.success(f"✅ Đã xoá '{del_key}' khỏi hệ thống!")
