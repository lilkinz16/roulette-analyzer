import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Phân Tích Roulette - 3 Phuong Pháp", layout="wide")
st.title("?? Phân Tích C?u Roulette Theo 3 Phuong Pháp Riêng Bi?t")

# ===== NH?P D? LI?U CHUNG =====
results = st.text_input("?? Nh?p dãy s? Roulette (cách nhau b?i d?u cách ho?c ph?y):", "0 16 17 18 19")
numbers = [int(x) for x in re.findall(r'\d+', results)]

col1, col2 = st.columns(2)

# ===== PHUONG PHÁP 1 =====
with col1:
    st.subheader("??? Phuong pháp 1: Thi?t l?p nhóm riêng")

    group_input_1 = {
        'A': st.text_input("Phuong pháp 1 - Nhóm A:", "0, 17"),
        'B': st.text_input("Phuong pháp 1 - Nhóm B:", "16, 18"),
        'C': st.text_input("Phuong pháp 1 - Nhóm C:", "1-15, 19, 20"),
        'D': st.text_input("Phuong pháp 1 - Nhóm D:", "21-36"),
    }

    group_map_1 = {
        group: [int(x.strip()) for x in re.findall(r'\d+', val)]
        for group, val in group_input_1.items()
    }

    def find_group_1(num):
        for group, values in group_map_1.items():
            if num in values:
                return group
        return "?"

    groups_1 = [find_group_1(n) for n in numbers]

    st.markdown("#### ?? B?ng C?u Baccarat-style (Phuong pháp 1)")

    group_colors_1 = {'A': "#F44336", 'B': "#2196F3", 'C': "#4CAF50", 'D': "#FF9800", '?': "#9E9E9E"}

    columns1 = []
    col_temp1 = []
    last1 = None
    for g in groups_1:
        if g == last1:
            col_temp1.append(g)
        else:
            if col_temp1:
                columns1.append(col_temp1)
            col_temp1 = [g]
            last1 = g
    if col_temp1:
        columns1.append(col_temp1)

    max_len1 = max(len(c) for c in columns1) if columns1 else 1
    fig1, ax1 = plt.subplots(figsize=(len(columns1), max_len1))
    ax1.axis('off')
    for x, col in enumerate(columns1):
        for y, val in enumerate(col):
            ax1.add_patch(plt.Rectangle((x, -y), 1, 1, color=group_colors_1.get(val, "#9E9E9E")))
            ax1.text(x + 0.5, -y + 0.5, val, ha='center', va='center', color='white', fontsize=16)
    plt.xlim(0, len(columns1))
    plt.ylim(-max_len1, 1)
    plt.tight_layout()
    st.pyplot(fig1)

# ===== PHUONG PHÁP 2 =====
with col2:
    st.subheader("??? Phuong pháp 2: Nhóm khác")

    group_input_2 = {
        'A': st.text_input("Phuong pháp 2 - Nhóm A:", "1, 3, 5, 7, 9"),
        'B': st.text_input("Phuong pháp 2 - Nhóm B:", "2, 4, 6, 8, 10"),
        'C': st.text_input("Phuong pháp 2 - Nhóm C:", "11, 13, 15, 17, 19"),
        'D': st.text_input("Phuong pháp 2 - Nhóm D:", "0, 12, 14, 16, 18, 20"),
    }

    group_map_2 = {
        group: [int(x.strip()) for x in re.findall(r'\d+', val)]
        for group, val in group_input_2.items()
    }

    def find_group_2(num):
        for group, values in group_map_2.items():
            if num in values:
                return group
        return "?"

    groups_2 = [find_group_2(n) for n in numbers]

    st.markdown("#### ?? B?ng C?u Baccarat-style (Phuong pháp 2)")

    group_colors_2 = {'A': "#795548", 'B': "#03A9F4", 'C': "#8BC34A", 'D': "#FFC107", '?': "#BDBDBD"}

    columns2 = []
    col_temp2 = []
    last2 = None
    for g in groups_2:
        if g == last2:
            col_temp2.append(g)
        else:
            if col_temp2:
                columns2.append(col_temp2)
            col_temp2 = [g]
            last2 = g
    if col_temp2:
        columns2.append(col_temp2)

    max_len2 = max(len(c) for c in columns2) if columns2 else 1
    fig2, ax2 = plt.subplots(figsize=(len(columns2), max_len2))
    ax2.axis('off')
    for x, col in enumerate(columns2):
        for y, val in enumerate(col):
            ax2.add_patch(plt.Rectangle((x, -y), 1, 1, color=group_colors_2.get(val, "#9E9E9E")))
            ax2.text(x + 0.5, -y + 0.5, val, ha='center', va='center', color='white', fontsize=16)
    plt.xlim(0, len(columns2))
    plt.ylim(-max_len2, 1)
    plt.tight_layout()
    st.pyplot(fig2)

# ===== PHUONG PHÁP 3 (Du?i cùng) =====
st.subheader("?? Phuong pháp 3: M?t nhóm khác n?a")

group_input_3 = {
    'A': st.text_input("Phuong pháp 3 - Nhóm A:", "0, 2, 4, 6, 8, 10, 12"),
    'B': st.text_input("Phuong pháp 3 - Nhóm B:", "1, 3, 5, 7, 9, 11, 13"),
    'C': st.text_input("Phuong pháp 3 - Nhóm C:", "14, 15, 16, 17, 18, 19, 20"),
    'D': st.text_input("Phuong pháp 3 - Nhóm D:", "21-36"),
}

group_map_3 = {
    group: [int(x.strip()) for x in re.findall(r'\d+', val)]
    for group, val in group_input_3.items()
}

def find_group_3(num):
    for group, values in group_map_3.items():
        if num in values:
            return group
    return "?"

groups_3 = [find_group_3(n) for n in numbers]

st.markdown("#### ?? B?ng C?u Baccarat-style (Phuong pháp 3)")

group_colors_3 = {'A': "#E91E63", 'B': "#00BCD4", 'C': "#CDDC39", 'D': "#FF5722", '?': "#BDBDBD"}

columns3 = []
col_temp3 = []
last3 = None
for g in groups_3:
    if g == last3:
        col_temp3.append(g)
    else:
        if col_temp3:
            columns3.append(col_temp3)
        col_temp3 = [g]
        last3 = g
if col_temp3:
    columns3.append(col_temp3)

max_len3 = max(len(c) for c in columns3) if columns3 else 1
fig3, ax3 = plt.subplots(figsize=(len(columns3), max_len3))
ax3.axis('off')
for x, col in enumerate(columns3):
    for y, val in enumerate(col):
        ax3.add_patch(plt.Rectangle((x, -y), 1, 1, color=group_colors_3.get(val, "#9E9E9E")))
        ax3.text(x + 0.5, -y + 0.5, val, ha='center', va='center', color='white', fontsize=16)
plt.xlim(0, len(columns3))
plt.ylim(-max_len3, 1)
plt.tight_layout()
st.pyplot(fig3)
