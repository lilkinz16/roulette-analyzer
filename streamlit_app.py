import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Phân Tích Roulette - 3 Bảng Có Chọn Kết Quả", layout="wide")
st.title("🎯 Phân Tích Cầu Roulette - Chọn Số Cột Hiển Thị Mỗi Bảng")

# ===== Nhập dãy số =====
results = st.text_input("🎲 Nhập dãy số Roulette:", "0 16 17 18 19 21 22 1 2 3")
numbers = [int(x) for x in re.findall(r'\d+', results)]

# ===== Hàm vẽ bảng Baccarat-style =====
def draw_baccarat_board(groups, group_colors, max_columns):
    # Tách chuỗi thành cột
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

    # Lấy n cột gần nhất
    columns = columns[-max_columns:]

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

# ===== 3 cột bảng ngang =====
col1, col2, col3 = st.columns(3)

# ===== PHƯƠNG PHÁP 1 =====
with col1:
    st.subheader("🅰️ Phương pháp 1")

    num1 = st.radio("Số cột hiển thị:", [10, 30, 50, 100], index=1, key="num1")

    group_input_1 = {
        'A': st.text_input("P1 - Nhóm A:", "0,1,2,3"),
        'B': st.text_input("P1 - Nhóm B:", "18"),
        'C': st.text_input("P1 - Nhóm C:", "0"),
        'D': st.text_input("P1 - Nhóm D:", "4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36"),
    }

    group_map_1 = {g: [int(x) for x in re.findall(r'\d+', v)] for g, v in group_input_1.items()}

    def find_group_1(n):
        for g, vals in group_map_1.items():
            if n in vals:
                return g
        return "?"

    groups_1 = [find_group_1(n) for n in numbers]

    group_colors_1 = {'A': "#F44336", 'B': "#2196F3", 'C': "#4CAF50", 'D': "#FF9800", '?': "#9E9E9E"}
    draw_baccarat_board(groups_1, group_colors_1, num1)

# ===== PHƯƠNG PHÁP 2 =====
with col2:
    st.subheader("🅱️ Phương pháp 2")

    num2 = st.radio("Số cột hiển thị:", [10, 30, 50, 100], index=1, key="num2")

    group_input_2 = {
        'A': st.text_input("P2 - Nhóm A:", "4, 5, 6, 0,"),
        'B': st.text_input("P2 - Nhóm B:", "2"),
        'C': st.text_input("P2 - Nhóm C:", "11"),
        'D': st.text_input("P2 - Nhóm D:", "1,2,3,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36"),
    }

    group_map_2 = {g: [int(x) for x in re.findall(r'\d+', v)] for g, v in group_input_2.items()}

    def find_group_2(n):
        for g, vals in group_map_2.items():
            if n in vals:
                return g
        return "?"

    groups_2 = [find_group_2(n) for n in numbers]

    group_colors_2 = {'A': "#795548", 'B': "#03A9F4", 'C': "#8BC34A", 'D': "#FFC107", '?': "#BDBDBD"}
    draw_baccarat_board(groups_2, group_colors_2, num2)

# ===== PHƯƠNG PHÁP 3 =====
with col3:
    st.subheader("🆎 Phương pháp 3")

    num3 = st.radio("Số cột hiển thị:", [10, 30, 50, 100], index=1, key="num3")

    group_input_3 = {
        'A': st.text_input("P3 - Nhóm A:", "0,7,8,9"),
        'B': st.text_input("P3 - Nhóm B:", "10"),
        'C': st.text_input("P3 - Nhóm C:", "11"),
        'D': st.text_input("P3 - Nhóm D:", "1,2,3,4,5,6,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36"),
    }

    group_map_3 = {g: [int(x) for x in re.findall(r'\d+', v)] for g, v in group_input_3.items()}

    def find_group_3(n):
        for g, vals in group_map_3.items():
            if n in vals:
                return g
        return "?"

    groups_3 = [find_group_3(n) for n in numbers]

    group_colors_3 = {'A': "#E91E63", 'B': "#00BCD4", 'C': "#CDDC39", 'D': "#FF5722", '?': "#BDBDBD"}
    draw_baccarat_board(groups_3, group_colors_3, num3)

# ===== 3 cột bảng ngang tiếp theo =====
col4, col5, col6 = st.columns(3)

# ===== PHƯƠNG PHÁP 4 =====
with col4:
    st.subheader("🆔 Phương pháp 4")

    num4 = st.radio("Số cột hiển thị:", [10, 30, 50, 100], index=1, key="num4")

    group_input_4 = {
        'A': st.text_input("P4 - Nhóm A:", "0,10,11,12"),
        'B': st.text_input("P4 - Nhóm B:", "2"),
        'C': st.text_input("P4 - Nhóm C:", "11"),
        'D': st.text_input("P4 - Nhóm D:", "1,2,3,4,5,6,7,8,9,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36"),
    }

    group_map_4 = {g: [int(x) for x in re.findall(r'\d+', v)] for g, v in group_input_4.items()}

    def find_group_4(n):
        for g, vals in group_map_4.items():
            if n in vals:
                return g
        return "?"

    groups_4 = [find_group_4(n) for n in numbers]

    group_colors_4 = {'A': "#9C27B0", 'B': "#3F51B5", 'C': "#009688", 'D': "#FF5722", '?': "#BDBDBD"}
    draw_baccarat_board(groups_4, group_colors_4, num4)

# ===== PHƯƠNG PHÁP 5 =====
with col5:
    st.subheader("🅾️ Phương pháp 5")

    num5 = st.radio("Số cột hiển thị:", [10, 30, 50, 100], index=1, key="num5")

    group_input_5 = {
        'A': st.text_input("P5 - Nhóm A:", "0,13,14,15"),
        'B': st.text_input("P5 - Nhóm B:", "3"),
        'C': st.text_input("P5 - Nhóm C:", "9"),
        'D': st.text_input("P5 - Nhóm D:", "1,2,3,4,5,6,7,8,9,10,11,12,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36"),
    }

    group_map_5 = {g: [int(x) for x in re.findall(r'\d+', v)] for g, v in group_input_5.items()}

    def find_group_5(n):
        for g, vals in group_map_5.items():
            if n in vals:
                return g
        return "?"

    groups_5 = [find_group_5(n) for n in numbers]

    group_colors_5 = {'A': "#673AB7", 'B': "#00BCD4", 'C': "#CDDC39", 'D': "#FF9800", '?': "#9E9E9E"}
    draw_baccarat_board(groups_5, group_colors_5, num5)

# ===== PHƯƠNG PHÁP 6 =====
with col6:
    st.subheader("🆓 Phương pháp 6")

    num6 = st.radio("Số cột hiển thị:", [10, 30, 50, 100], index=1, key="num6")

    group_input_6 = {
        'A': st.text_input("P6 - Nhóm A:", "0,16,17,18"),
        'B': st.text_input("P6 - Nhóm B:", "5"),
        'C': st.text_input("P6 - Nhóm C:", "9"),
        'D': st.text_input("P6 - Nhóm D:", "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36"),
    }

    group_map_6 = {g: [int(x) for x in re.findall(r'\d+', v)] for g, v in group_input_6.items()}

    def find_group_6(n):
        for g, vals in group_map_6.items():
            if n in vals:
                return g
        return "?"

    groups_6 = [find_group_6(n) for n in numbers]

    group_colors_6 = {'A': "#E91E63", 'B': "#2196F3", 'C': "#4CAF50", 'D': "#9E9E9E", '?': "#BDBDBD"}
    draw_baccarat_board(groups_6, group_colors_6, num6)

