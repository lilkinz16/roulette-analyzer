import streamlit as st
import matplotlib.pyplot as plt

# Cấu hình giao diện
st.set_page_config(page_title="Bảng Cầu Baccarat 4 loại", layout="wide")
st.title("🎯 Bảng Cầu Baccarat: Big Road, Big Eye Boy, Small Road, Cockroach Pig")

# Khởi tạo kết quả người dùng chọn
if "result_sequence" not in st.session_state:
    st.session_state.result_sequence = []

# Giao diện nút bấm
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

# Không làm gì nếu chuỗi rỗng
if not st.session_state.result_sequence:
    st.info("👉 Bấm ĐỎ hoặc XANH để bắt đầu tạo bảng cầu.")
    st.stop()

# ==== 1. Xây Big Road ====
MAX_ROW = 6
grid = {}
x, y = 0, 0
last = None

for symbol in st.session_state.result_sequence:
    if symbol == last:
        if y < MAX_ROW - 1 and (x, y + 1) not in grid:
            y += 1
        else:
            x += 1
            y = 0
    else:
        x += 1
        y = 0
    grid[(x, y)] = symbol
    last = symbol

# Lấy chiều cao cột
col_heights = {}
for (cx, cy) in grid:
    col_heights[cx] = max(col_heights.get(cx, 0), cy + 1)

# ==== 2. Tính các bảng phụ (logic giống thật) ====
def gen_big_eye(col_heights):
    big_eye = {}
    for col in range(2, max(col_heights.keys()) + 1):
        same = col_heights.get(col - 1, 0) == col_heights.get(col - 2, 0)
        color = "🔵" if same else "🔴"
        big_eye[(col - 1, 0)] = color
    return big_eye

def gen_small_road(col_heights):
    small = {}
    for col in range(3, max(col_heights.keys()) + 1):
        same = col_heights.get(col - 2, 0) == col_heights.get(col - 3, 0)
        color = "🔵" if same else "🔴"
        small[(col - 2, 0)] = color
    return small

def gen_cockroach(col_heights):
    cock = {}
    for col in range(4, max(col_heights.keys()) + 1):
        same = col_heights.get(col - 2, 0) == col_heights.get(col - 4, 0)
        color = "🔵" if same else "🔴"
        cock[(col - 2, 0)] = color
    return cock

# Các bảng cầu
grids = {
    "Big Road": grid,
    "Big Eye Boy": gen_big_eye(col_heights),
    "Small Road": gen_small_road(col_heights),
    "Cockroach Pig": gen_cockroach(col_heights)
}

# ==== 3. Vẽ 4 bảng ====
cols = st.columns(4)
colors_map = {"🟥": "#E53935", "🟦": "#1E88E5", "🔴": "#E53935", "🔵": "#1E88E5"}

for idx, (name, g) in enumerate(grids.items()):
    with cols[idx]:
        st.markdown(f"### {name}")
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.axis("off")
        for (x, y), val in g.items():
            color = colors_map.get(val, "#999999")
            ax.add_patch(plt.Rectangle((x, -y), 1, 1, color=color))
            ax.text(x + 0.5, -y + 0.5, val, ha="center", va="center", fontsize=16, color="white")
        max_x = max((x for x, _ in g), default=1) + 1
        ax.set_xlim(0, max_x)
        ax.set_ylim(-6, 1)
        st.pyplot(fig)
