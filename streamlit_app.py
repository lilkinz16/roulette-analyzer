import streamlit as st
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Phân Tích Baccarat - 3 Bảng Cầu", layout="wide")
st.title("🎯 Phân Tích Cầu Baccarat - Nhập BPB, cấu hình nhóm, 3 bảng độc lập")

# === Nhập kết quả kiểu BPBPPB ===
results_input = st.text_input("🎲 Nhập chuỗi kết quả (B = Đỏ, P = Xanh):", "BPBPPBBP")
symbol_map = {'B': 0, 'P': 1}
numbers = [symbol_map.get(char.upper(), -1) for char in results_input if char.upper() in symbol_map]

# === Hàm vẽ Big Road ===
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

# === Hàm xử lý từng phương pháp ===
def handle_strategy(col, name, default_group_map, group_colors, key_prefix):
    with col:
        st.subheader(f"🧠 Phương pháp {name}")
        num = st.radio("Số cột hiển thị:", [10, 30, 50, 100], index=1, key=f"{key_prefix}_num")

        group_input = {
            'A': st.text_input(f"P{name} - Nhóm A:", default_group_map['A'], key=f"{key_prefix}_A"),
            'B': st.text_input(f"P{name} - Nhóm B:", default_group_map['B'], key=f"{key_prefix}_B"),
            'C': st.text_input(f"P{name} - Nhóm C:", default_group_map['C'], key=f"{key_prefix}_C"),
            'D': st.text_input(f"P{name} - Nhóm D:", default_group_map['D'], key=f"{key_prefix}_D"),
        }

        group_map = {g: [int(x) for x in re.findall(r'\d+', v)] for g, v in group_input.items()}

        def find_group(n):
            for g, vals in group_map.items():
                if n in vals:
                    return g
            return "?"

        groups = [find_group(n) for n in numbers]
        draw_baccarat_board(groups, group_colors, num)

# === Bố cục 3 bảng ===
col1, col2, col3 = st.columns(3)

# PHƯƠNG PHÁP 1
handle_strategy(
    col1,
    name="1",
    default_group_map={
        'A': "0,1,2",
        'B': "3,4,5",
        'C': "6,7,8",
        'D': "9,10,11"
    },
    group_colors={'A': "#F44336", 'B': "#2196F3", 'C': "#4CAF50", 'D': "#FF9800", '?': "#9E9E9E"},
    key_prefix="pp1"
)

# PHƯƠNG PHÁP 2
handle_strategy(
    col2,
    name="2",
    default_group_map={
        'A': "0,2,4,6",
        'B': "1,3,5",
        'C': "7,8,9",
        'D': "10,11,12"
    },
    group_colors={'A': "#795548", 'B': "#03A9F4", 'C': "#8BC34A", 'D': "#FFC107", '?': "#BDBDBD"},
    key_prefix="pp2"
)

# PHƯƠNG PHÁP 3
handle_strategy(
    col3,
    name="3",
    default_group_map={
        'A': "0, 19, 20, 21",
        'B': "1,10",
        'C': "14,11",
        'D': "2,3,4,5,6,7,8,9,11,12"
    },
    group_colors={'A': "#E91E63", 'B': "#00BCD4", 'C': "#CDDC39", 'D': "#FF5722", '?': "#BDBDBD"},
    key_prefix="pp3"
)
