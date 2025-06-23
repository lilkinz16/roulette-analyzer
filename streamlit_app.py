import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bảng Cầu Baccarat Mini", layout="centered")
st.title("🎯 Bảng Cầu Baccarat Thủ Công (Chạm Đỏ/Xanh)")

# Tạo hoặc lấy session_state lưu kết quả
if "result_sequence" not in st.session_state:
    st.session_state.result_sequence = []

# Giao diện 2 nút Đỏ/Xanh
col1, col2, col3 = st.columns([1,1,2])
with col1:
    if st.button("🔴 Đặt ĐỎ"):
        st.session_state.result_sequence.append("🟥")
with col2:
    if st.button("🔵 Đặt XANH"):
        st.session_state.result_sequence.append("🟦")
with col3:
    if st.button("♻️ Reset"):
        st.session_state.result_sequence = []

# Hiển thị chuỗi hiện tại
if not st.session_state.result_sequence:
    st.info("👉 Hãy bấm ĐỎ hoặc XANH để bắt đầu tạo cầu Baccarat.")
else:
    st.markdown(f"🧾 **Dãy hiện tại:** {' '.join(st.session_state.result_sequence)}")

    # Vẽ bảng cầu
    symbol_seq = st.session_state.result_sequence
    columns = []
    col = []
    last = None

    for r in symbol_seq:
        if r == last:
            col.append(r)
        else:
            if col:
                columns.append(col)
            col = [r]
            last = r
    if col:
        columns.append(col)

    max_len = max(len(c) for c in columns) if columns else 1
    fig, ax = plt.subplots(figsize=(len(columns), max_len))
    ax.axis('off')

    for x, col in enumerate(columns):
        for y, val in enumerate(col):
            color = "#E53935" if val == '🟥' else "#1E88E5"
            ax.add_patch(plt.Rectangle((x, -y), 1, 1, color=color))
            ax.text(x + 0.5, -y + 0.5, val, va='center', ha='center', fontsize=16, color='white')

    plt.xlim(0, len(columns))
    plt.ylim(-max_len, 1)
    plt.tight_layout()
    st.pyplot(fig)
