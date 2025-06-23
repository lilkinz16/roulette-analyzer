import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Cầu Roulette dạng Baccarat", layout="centered")
st.title("🎯 Bảng Cầu Roulette theo kiểu Baccarat")

# Ánh xạ nhóm
group_map = {
    'A': [0, 1, 6, 9, 18, 21, 28, 31, 36],
    'B': [2, 3, 5, 8, 17, 20, 29, 32, 24, 27],
    'C': [4, 7, 10, 13, 16, 19, 30, 33],
    'D': [12, 15, 11, 14, 22, 25, 28, 34, 35],
}

def find_group(num):
    for group, numbers in group_map.items():
        if num in numbers:
            return group
    return "?"

# Nhập chuỗi số
input_str = st.text_input("📥 Nhập dãy số Roulette (cách nhau bởi dấu cách hoặc dấu phẩy):", "22 19 15 33 19 6 2 5 9 28")

# Chọn nhóm màu đỏ và xanh
col1, col2 = st.columns(2)
with col1:
    red_group = st.selectbox("🔴 Chọn nhóm làm ĐỎ (Player)", ["A", "B", "C", "D"], index=0)
with col2:
    blue_group = st.selectbox("🔵 Chọn nhóm làm XANH (Banker)", ["A", "B", "C", "D"], index=1)

# Xử lý dãy số
numbers = [int(x) for x in re.findall(r'\d+', input_str)]
groups = [find_group(n) for n in numbers]

# Ánh xạ màu theo chọn
def map_color_symbol(group):
    if group == red_group:
        return "🟥"
    elif group == blue_group:
        return "🟦"
    else:
        return None

symbol_seq = list(filter(None, [map_color_symbol(g) for g in groups]))

# Vẽ cầu Baccarat
if len(symbol_seq) < 1:
    st.warning("Không có số nào thuộc nhóm đã chọn!")
else:
    st.subheader("🧮 Bảng Cầu Baccarat")

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

    # Hiển thị bảng số và nhóm
    df = pd.DataFrame({
        "Tay": list(range(1, len(numbers)+1)),
        "Số": numbers,
        "Nhóm": groups,
        "Biểu tượng": [map_color_symbol(g) if map_color_symbol(g) else "❌" for g in groups]
    })
    st.subheader("📋 Bảng Thống kê")
    st.dataframe(df)
