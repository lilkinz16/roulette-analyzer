import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Phân Tích C?u X? S? - 3 B?ng Có Ch?n K?t Qu?", layout="wide")
st.title("?? Phân Tích C?u X? S? (00-99) - Ch?n S? C?t Hi?n Th? M?i B?ng")

# ===== Nh?p dãy s? =====
results = st.text_input("?? Nh?p dãy s? (cách nhau b?ng kho?ng tr?ng ho?c d?u ph?y):", "00 12 34 56 78 99")
numbers = [int(x) for x in re.findall(r'\d{2}', results)]

# ===== Hàm v? b?ng Baccarat-style =====
def draw_baccarat_board(groups, group_colors, max_columns):
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

# ===== T?o 3 b?ng ngang =====
col1, col2, col3 = st.columns(3)

# ===== PHUONG PHÁP 1 =====
with col1:
    st.subheader("??? Phuong pháp 1")
    num1 = st.radio("S? c?t hi?n th?:", [10, 30, 50, 100], index=1, key="num1")

    group_input_1 = {
        'A': st.text_input("P1 - Nhóm A:", "00,01,02,03,04"),
        'B': st.text_input("P1 - Nhóm B:", "10,11,12"),
        'C': st.text_input("P1 - Nhóm C:", "01, 11, 21, 31, 41, 51, 61, 71, 81, 91"),
        'D': st.text_input("P1 - Nhóm D:", "00, 02, 03, 04, 05, 06, 07, 08, 09, 10,  12, 13, 14, 15, 16, 17, 18, 19, 20, 22,  23, 24, 25, 26, 27, 28, 29, 30, 32, 33,  34, 35, 36, 37, 38, 39, 40, 42, 43, 44,  45, 46, 47, 48, 49, 50, 52, 53, 54, 55,  56, 57, 58, 59, 60, 62, 63, 64, 65, 66,  67, 68, 69, 70, 72, 73, 74, 75, 76, 77,  78, 79, 80, 82, 83, 84, 85, 86, 87, 88,  89, 90, 92, 93, 94, 95, 96, 97, 98, 99"),
    }

    group_map_1 = {g: [int(x) for x in re.findall(r'\d{2}', v)] for g, v in group_input_1.items()}

    def find_group_1(n):
        for g, vals in group_map_1.items():
            if n in vals:
                return g
        return "?"

    groups_1 = [find_group_1(n) for n in numbers]
    group_colors_1 = {'A': "#F44336", 'B': "#2196F3", 'C': "#4CAF50", 'D': "#FF9800", '?': "#9E9E9E"}
    draw_baccarat_board(groups_1, group_colors_1, num1)

# ===== PHUONG PHÁP 2 =====
with col2:
    st.subheader("??? Phuong pháp 2")
    num2 = st.radio("S? c?t hi?n th?:", [10, 30, 50, 100], index=1, key="num2")

    group_input_2 = {
        'A': st.text_input("P2 - Nhóm A:", "05,15,25"),
        'B': st.text_input("P2 - Nhóm B:", "35,45,55"),
        'C': st.text_input("P2 - Nhóm C:", "00, 11, 22, 33, 44, 55, 66, 77, 88, 99"),
        'D': st.text_input("P2 - Nhóm D:", "01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 12, 13, 14, 15, 16, 17, 18, 19,  20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39,  40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 56, 57, 58, 59,  60, 61, 62, 63, 64, 65, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 78, 79,  80, 81, 82, 83, 84, 85, 86, 87, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98"),
    }

    group_map_2 = {g: [int(x) for x in re.findall(r'\d{2}', v)] for g, v in group_input_2.items()}

    def find_group_2(n):
        for g, vals in group_map_2.items():
            if n in vals:
                return g
        return "?"

    groups_2 = [find_group_2(n) for n in numbers]
    group_colors_2 = {'A': "#795548", 'B': "#03A9F4", 'C': "#8BC34A", 'D': "#FFC107", '?': "#BDBDBD"}
    draw_baccarat_board(groups_2, group_colors_2, num2)

# ===== PHUONG PHÁP 3 =====
with col3:
    st.subheader("?? Phuong pháp 3")
    num3 = st.radio("S? c?t hi?n th?:", [10, 30, 50, 100], index=1, key="num3")

    group_input_3 = {
        'A': st.text_input("P3 - Nhóm A:", "01,11,21,31"),
        'B': st.text_input("P3 - Nhóm B:", "41,51"),
        'C': st.text_input("P3 - Nhóm C:", "61,71"),
        'D': st.text_input("P3 - Nhóm D:", "81,91"),
    }

    group_map_3 = {g: [int(x) for x in re.findall(r'\d{2}', v)] for g, v in group_input_3.items()}

    def find_group_3(n):
        for g, vals in group_map_3.items():
            if n in vals:
                return g
        return "?"

    groups_3 = [find_group_3(n) for n in numbers]
    group_colors_3 = {'A': "#E91E63", 'B': "#00BCD4", 'C': "#CDDC39", 'D': "#FF5722", '?': "#BDBDBD"}
    draw_baccarat_board(groups_3, group_colors_3, num3)

# ===== Tạo 3 bảng ngang tiếp theo =====
col4, col5, col6 = st.columns(3)

# ===== PHƯƠNG PHÁP 4 =====
with col4:
    st.subheader("🔢 Phương pháp 4")
    num4 = st.radio("Số cột hiển thị:", [10, 30, 50, 100], index=1, key="num4")

    group_input_4 = {
        'A': st.text_input("P4 - Nhóm A:", "09,19,29"),
        'B': st.text_input("P4 - Nhóm B:", "39,49,59"),
        'C': st.text_input("P4 - Nhóm C:", "69,79"),
        'D': st.text_input("P4 - Nhóm D:", "00,01,02,03,04,05,06,07,08,10,11,12,13,14,15,16,17,18,20,21,22,23,24,25,26,27,28,30,31,32,33,34,35,36,37,38,40,41,42,43,44,45,46,47,48,50,51,52,53,54,55,56,57,58,60,61,62,63,64,65,66,67,68,70,71,72,73,74,75,76,77,78,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99"),
    }

    group_map_4 = {g: [int(x) for x in re.findall(r'\d{2}', v)] for g, v in group_input_4.items()}

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
    st.subheader("🧮 Phương pháp 5")
    num5 = st.radio("Số cột hiển thị:", [10, 30, 50, 100], index=1, key="num5")

    group_input_5 = {
        'A': st.text_input("P5 - Nhóm A:", "00,11,22,33,44"),
        'B': st.text_input("P5 - Nhóm B:", "55,66,77"),
        'C': st.text_input("P5 - Nhóm C:", "88,99"),
        'D': st.text_input("P5 - Nhóm D:", "01,02,03,04,05,06,07,08,09,10,12,13,14,15,16,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,34,35,36,37,38,39,40,41,42,43,45,46,47,48,49,50,51,52,53,54,56,57,58,59,60,61,62,63,64,65,67,68,69,70,71,72,73,74,75,76,78,79,80,81,82,83,84,85,86,87,89,90,91,92,93,94,95,96,97,98"),
    }

    group_map_5 = {g: [int(x) for x in re.findall(r'\d{2}', v)] for g, v in group_input_5.items()}

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
    st.subheader("🎲 Phương pháp 6")
    num6 = st.radio("Số cột hiển thị:", [10, 30, 50, 100], index=1, key="num6")

    group_input_6 = {
        'A': st.text_input("P6 - Nhóm A:", "00,02,04,06,08"),
        'B': st.text_input("P6 - Nhóm B:", "01,03,05,07,09"),
        'C': st.text_input("P6 - Nhóm C:", "10,20,30,40,50"),
        'D': st.text_input("P6 - Nhóm D:", "11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,47,48,49,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99"),
    }

    group_map_6 = {g: [int(x) for x in re.findall(r'\d{2}', v)] for g, v in group_input_6.items()}

    def find_group_6(n):
        for g, vals in group_map_6.items():
            if n in vals:
                return g
        return "?"

    groups_6 = [find_group_6(n) for n in numbers]
    group_colors_6 = {'A': "#E91E63", 'B': "#2196F3", 'C': "#4CAF50", 'D': "#9E9E9E", '?': "#BDBDBD"}
    draw_baccarat_board(groups_6, group_colors_6, num6)
