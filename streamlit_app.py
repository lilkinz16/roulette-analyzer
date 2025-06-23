import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bảng Cầu Baccarat Thủ Công", layout="centered")
st.title("🎯 Bảng Cầu Baccarat Thủ Công (Chạm Đỏ/Xanh)")

# Khởi tạo session_state nếu chưa có
if "result_sequence" not in st.session_state:
    st.session_state.result_sequence = []

# Giao diện nút bấm
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🔴 Đặt ĐỎ"):
        st.session_state.result_sequence.append("🟥")
with col2:
    if st.button("🔵 Đặt XANH"):
        st.session_state.result_sequence.append("🟦")
with col3:
    if st.button("♻️ Reset"):
        st.session_state.result_sequence = []

# Hiển thị dãy kết quả
if not st.session_state.result_sequence:
    st.info("👉 Bấm vào nút ĐỎ hoặc XANH để tạo bảng cầu Baccarat.")
else:
    st.markdown(f"🧾 **Dãy hiện tại:** {' '.join(st.session_state.result_sequence)}")

    # ==== Xử lý logic bảng cầu ====
    MAX_ROW = 6  # Giới hạn số hàng như Baccarat thật

    grid = {}     # {(x, y): symbol}
    x, y = 0, 0
    last = None

    for symbol in st.session_state.result_sequence:
        if symbol == last:
            if y < MAX_ROW - 1 and (x, y + 1) not in grid:
                y += 1
            else:
                x += 1
                y = 0
        else:
            x += 1
            y = 0
        grid[(x, y)] = symbol
        last = symbol

    # ==== Vẽ bảng ====
    fig, ax = plt.subplots(figsize=(max(x + 2, 6), MAX_ROW))
    ax.axis('off')

    for (x, y), val in grid.items():
        color = "#E53935" if val == '🟥' else "#1E88E5"
        ax.add_patch(plt.Rectangle((x, -y), 1, 1, color=color))
        ax.text(x + 0.5, -y + 0.5, val, va='center', ha='center', fontsize=16, color='white')

    plt.xlim(0, x + 2)
    plt.ylim(-MAX_ROW, 1)
    plt.tight_layout()
    st.pyplot(fig)
