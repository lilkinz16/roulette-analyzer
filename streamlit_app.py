import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Baccarat Cầu 4 Loại", layout="wide")
st.title("🎯 Bảng Cầu Baccarat: Big Road, Big Eye Boy, Small Road, Cockroach Pig")

# Session state
if "result_sequence" not in st.session_state:
    st.session_state.result_sequence = []

# Nút bấm
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

if not st.session_state.result_sequence:
    st.info("👉 Bấm để bắt đầu đặt tay")
    st.stop()

# ==== 1. Tạo Big Road ====
MAX_ROW = 6
big_grid = {}
x, y = 0, 0
last = None

for symbol in st.session_state.result_sequence:
    if symbol == last:
        if (x, y + 1) not in big_grid and y + 1 < MAX_ROW:
            y += 1
        else:
            x += 1
            while (x, 0) in big_grid:
                x += 1
            y = 0
    else:
        x += 1
        while (x, 0) in big_grid:
            x += 1
        y = 0
    big_grid[(x, y)] = symbol
    last = symbol

# ==== 2. Hàm logic cầu phụ ====
def get_color_by_shape(x, y, ref_x1, ref_x2, grid):
    a = (ref_x1, y) in grid
    b = (ref_x2, y) in grid
    if a and b:
        return "🔵"
    elif a or b:
        return "🔴"
    else:
        return None

def get_shape_sequence(start_col, offset1, offset2, grid):
    result = []
    max_col = max(i[0] for i in grid)
    for x in range(start_col, max_col + 1):
        color = get_color_by_shape(x, 0, x - offset1, x - offset2, grid)
        if color:
            result.append(color)
    return result

def build_vertical_grid(symbol_list):
    grid = {}
    x, y = 0, 0
    last = None
    for symbol in symbol_list:
        if symbol == last:
            if (x, y + 1) not in grid and y + 1 < MAX_ROW:
                y += 1
            else:
                x += 1
                y = 0
        else:
            x += 1
            y = 0
        grid[(x, y)] = symbol
        last = symbol
    return grid

# ==== 3. Tạo các bảng phụ ====
big_eye_seq = get_shape_sequence(2, 1, 2, big_grid)
small_seq = get_shape_sequence(3, 2, 3, big_grid)
cock_seq = get_shape_sequence(4, 2, 4, big_grid)

big_eye = build_vertical_grid(big_eye_seq)
small_road = build_vertical_grid(small_seq)
cockroach = build_vertical_grid(cock_seq)

# ==== 4. Vẽ bảng ====
colors_map = {"🟥": "#E53935", "🟦": "#1E88E5", "🔴": "#E53935", "🔵": "#1E88E5"}
grids = {
    "Big Road": big_grid,
    "Big Eye Boy": big_eye,
    "Small Road": small_road,
    "Cockroach Pig": cockroach
}

cols = st.columns(4)

for idx, (name, g) in enumerate(grids.items()):
    with cols[idx]:
        st.markdown(f"### {name}")
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.axis("off")
        for (gx, gy), val in g.items():
            color = colors_map.get(val, "#999999")
            ax.add_patch(plt.Rectangle((gx, -gy), 1, 1, color=color))
            ax.text(gx + 0.5, -gy + 0.5, val, ha="center", va="center", fontsize=16, color="white")
        max_x = max((gx for gx, _ in g), default=1) + 1
        ax.set_xlim(0, max_x)
        ax.set_ylim(-MAX_ROW, 1)
        st.pyplot(fig)
