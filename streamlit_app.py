import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Phân Tích Roulette - 3 Bảng Ngang", layout="wide")
st.title("🎯 Phân Tích Cầu Roulette Theo 3 Phương Pháp Song Song")

# ===== Nhập dãy số =====
results = st.text_input("🎲 Nhập dãy số Roulette (phân cách bằng dấu cách hoặc phẩy):", "0 16 17 18 19 21 22 1 2 3")
numbers = [int(x) for x in re.findall(r'\d+', results)]

# ===== Số cột tối đa hiển thị cho mỗi bảng =====
max_columns_to_show = 30

# ===== Cấu hình 3 nhóm =====
col1, col2, col3 = st.columns(3)

# ==== Hàm vẽ bảng Baccarat-style ====
def draw_baccarat_board(groups, group_colors, title):
    # Tách cột cầu
    columns = []
    col_temp = []
    last = None
    for g in groups:
        if g == last:
            col_temp.append(g)
        else:
            if col_temp:
                columns.append(col_temp)
            col_temp = [g]
            last = g
    if col_temp:
        columns.append(col_temp)

    # Giới hạn số cột
    columns = columns[-max_columns_to_show:]

    max_len = max(len(c) for c in columns) if columns else 1
    fig, ax = plt.subplots(figsize=(max(len(columns), 10), 6))
    ax.axis('off')

    for x, col in enumerate(columns):
        for y, val in enumerate(col):
            color = group_colors.get(val, "#9E9E9E")
            ax.add_patch(plt.Rectangle((x, -y), 1, 1, color=color))
            ax.text(x + 0.5, -y + 0.5, val, ha='center', va='center', color='white', fontsize=14)

    plt.xlim(0, len(columns))
    plt.ylim(-max_len, 1)
    plt.tight_layout()
    st.pyplot(fig)

# ===== PHƯƠNG PHÁP 1 =====
with col1:
    st.subheader("🅰️ Phương pháp 1")

    group_input_1 = {
        'A': st.text_input("P1 - Nhóm A:", "0, 17"),
        'B': st.text_input("P1 - Nhóm B:", "16, 18"),
        'C': st.text_input("P1 - Nhóm C:", "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,19,20"),
        'D': st.text_input("P1 - Nhóm D:", "21-36"),
    }

    group_map_1 = {
        g: [int(x) for x in re.findall(r'\d+', v)]
        for g, v in group_input_1.items()
    }

    def find_group_1(n):
        for g, vals in group_map_1.items():
            if n in vals:
                return g
        return "?"

    groups_1 = [find_group_1(n) for n in numbers]

    group_colors_1 = {'A': "#F44336", 'B': "#2196F3", 'C': "#4CAF50", 'D': "#FF9800", '?': "#9E9E9E"}
    draw_baccarat_board(groups_1, group_colors_1, "Phương pháp 1")

# ===== PHƯƠNG PHÁP 2 =====
with col2:
    st.subheader("🅱️ Phương pháp 2")

    group_input_2 = {
        'A': st.text_input("P2 - Nhóm A:", "1, 3, 5, 7, 9"),
        'B': st.text_input("P2 - Nhóm B:", "2, 4, 6, 8, 10"),
        'C': st.text_input("P2 - Nhóm C:", "11,13,15,17,19"),
        'D': st.text_input("P2 - Nhóm D:", "0,12,14,16,18,20"),
    }

    group_map_2 = {
        g: [int(x) for x in re.findall(r'\d+', v)]
        for g, v in group_input_2.items()
    }

    def find_group_2(n):
        for g, vals in group_map_2.items():
            if n in vals:
                return g
        return "?"

    groups_2 = [find_group_2(n) for n in numbers]

    group_colors_2 = {'A': "#795548", 'B': "#03A9F4", 'C': "#8BC34A", 'D': "#FFC107", '?': "#BDBDBD"}
    draw_baccarat_board(groups_2, group_colors_2, "Phương pháp 2")

# ===== PHƯƠNG PHÁP 3 =====
with col3:
    st.subheader("🆎 Phương pháp 3")

    group_input_3 = {
        'A': st.text_input("P3 - Nhóm A:", "0, 2, 4, 6, 8, 10, 12"),
        'B': st.text_input("P3 - Nhóm B:", "1, 3, 5, 7, 9, 11, 13"),
        'C': st.text_input("P3 - Nhóm C:", "14,15,16,17,18,19,20"),
        'D': st.text_input("P3 - Nhóm D:", "21-36"),
    }

    group_map_3 = {
        g: [int(x) for x in re.findall(r'\d+', v)]
        for g, v in group_input_3.items()
    }

    def find_group_3(n):
        for g, vals in group_map_3.items():
            if n in vals:
                return g
        return "?"

    groups_3 = [find_group_3(n) for n in numbers]

    group_colors_3 = {'A': "#E91E63", 'B': "#00BCD4", 'C': "#CDDC39", 'D': "#FF5722", '?': "#BDBDBD"}
    draw_baccarat_board(groups_3, group_colors_3, "Phương pháp 3")
