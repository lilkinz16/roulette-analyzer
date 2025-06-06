import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Phân Tích Roulette - Cầu Nhóm", layout="wide")
st.title("🎯 Phân Tích Cầu Roulette Theo 2 Phương Pháp")

# ===== Nhập nhóm động (cho phương pháp 1) =====
st.subheader("✏️ Thiết lập nhóm số Roulette (Phương pháp 1)")

group_input = {
    'A': st.text_input("Nhóm A:", "0, 17"),
    'B': st.text_input("Nhóm B:", "16, 18"),
    'C': st.text_input("Nhóm C:", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 19, 20"),
    'D': st.text_input("Nhóm D:", "21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36"),
}

# Parse input thành dict group_map
group_map = {
    group: [int(x.strip()) for x in re.findall(r'\d+', val)]
    for group, val in group_input.items()
}

# ===== Hàm xác định nhóm =====
def find_group(num):
    for group, numbers in group_map.items():
        if num in numbers:
            return group
    return "?"

# ===== Nhập kết quả roulette =====
results = st.text_input("🎲 Nhập dãy số Roulette (cách nhau bởi dấu cách hoặc phẩy):", "0 16 17 18 19")
numbers = [int(x) for x in re.findall(r'\d+', results)]
groups = [find_group(n) for n in numbers]

# ===== Bảng kết quả nhóm =====
data = pd.DataFrame({
    "Tay": list(range(1, len(numbers) + 1)),
    "Số": numbers,
    "Nhóm": groups
})

st.subheader("📋 Kết quả nhóm")
st.dataframe(data, use_container_width=True)

# ===== Chia giao diện 2 cột =====
col1, col2 = st.columns(2)

# ===== CỘT 1: Theo nhóm người dùng nhập =====
with col1:
    st.subheader("📊 Phương pháp 1: Theo nhóm nhập")

    # Màu theo nhóm
    group_colors = {
        'A': "#F44336",
        'B': "#2196F3",
        'C': "#4CAF50",
        'D': "#FF9800",
        '?': "#9E9E9E"
    }

    columns = []
    col = []
    last = None

    for group in groups:
        if group == last:
            col.append(group)
        else:
            if col:
                columns.append(col)
            col = [group]
            last = group
    if col:
        columns.append(col)

    max_len = max(len(c) for c in columns) if columns else 1
    fig1, ax1 = plt.subplots(figsize=(len(columns), max_len))
    ax1.axis('off')

    for x, col in enumerate(columns):
        for y, val in enumerate(col):
            color = group_colors.get(val, "#9E9E9E")
            ax1.add_patch(plt.Rectangle((x, -y), 1, 1, color=color))
            ax1.text(x + 0.5, -y + 0.5, val, va='center', ha='center', fontsize=16, color='white')

    plt.xlim(0, len(columns))
    plt.ylim(-max_len, 1)
    plt.tight_layout()
    st.pyplot(fig1)

# ===== CỘT 2: Theo Chẵn / Lẻ =====
with col2:
    st.subheader("📊 Phương pháp 2: Chẵn / Lẻ")

    even_odd = ['Chẵn' if n % 2 == 0 else 'Lẻ' for n in numbers]

    columns2 = []
    col2 = []
    last2 = None

    for val in even_odd:
        if val == last2:
            col2.append(val)
        else:
            if col2:
                columns2.append(col2)
            col2 = [val]
            last2 = val
    if col2:
        columns2.append(col2)

    max_len2 = max(len(c) for c in columns2) if columns2 else 1
    fig2, ax2 = plt.subplots(figsize=(len(columns2), max_len2))
    ax2.axis('off')

    color_map2 = {'Chẵn': "#3F51B5", 'Lẻ': "#E91E63"}

    for x, col in enumerate(columns2):
        for y, val in enumerate(col):
            color = color_map2.get(val, "#9E9E9E")
            ax2.add_patch(plt.Rectangle((x, -y), 1, 1, color=color))
            ax2.text(x + 0.5, -y + 0.5, val, va='center', ha='center', fontsize=16, color='white')

    plt.xlim(0, len(columns2))
    plt.ylim(-max_len2, 1)
    plt.tight_layout()
    st.pyplot(fig2)
