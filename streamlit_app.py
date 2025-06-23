import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Baccarat Cầu Chuẩn", layout="wide")
st.title("🎯 Bảng Cầu Baccarat: Big Road, Big Eye Boy, Small Road, Cockroach Pig")

# === Session State ===
if "result_sequence" not in st.session_state:
    st.session_state.result_sequence = []

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
    st.info("👉 Bấm ĐỎ hoặc XANH để bắt đầu.")
    st.stop()

# === Build Big Road ===
MAX_ROW = 6
grid = {}
x, y = 0, 0
last = None

for symbol in st.session_state.result_sequence:
    if symbol == last:
        if (x, y + 1) not in grid and y + 1 < MAX_ROW:
            y += 1
        else:
            x += 1
            while (x, 0) in grid:
                x += 1
            y = 0
    else:
        x += 1
        while (x, 0) in grid:
            x += 1
        y = 0
    grid[(x, y)] = symbol
    last = symbol

# === Build helper logic for 3 derived roads ===
def get_color_by_shape(x, y, ref_x1, ref_x2, grid):
    a = (ref_x1, y) in grid
    b = (ref_x2, y) in grid
    if a and b:
        return "🔵"
    elif a or b:
        return "🔴"
    else:
        return None

def build_pattern_road(start_col, offset1, offset2):
    res = {}
    max_col = max(i[0] for i in grid)
    for x in range(start_col, max_col + 1):
        color = get_color_by_shape(x, 0, x - offset1, x - offset2, grid)
        if color:
            res[(x - offset1, 0)] = color
    return res

big_eye = build_pattern_road(2, 1, 2)
small_road = build_pattern_road(3, 2, 3)
cockroach = build_pattern_road(4, 2, 4)

grids = {
    "Big Road": grid,
    "Big Eye Boy": big_eye,
    "Small Road": small_road,
    "Cockroach Pig": cockroach
}

# === Vẽ 4 bảng ===
colors_map = {"🟥": "#E53935", "🟦": "#1E88E5", "🔴": "#E53935", "🔵": "#1E88E5"}
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
