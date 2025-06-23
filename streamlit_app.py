import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Baccarat - Big Road & Chu kỳ", layout="wide")
st.title("🎯 Bảng Cầu Baccarat + Gợi ý theo Chu Kỳ")

# Session
if "result_sequence" not in st.session_state:
    st.session_state.result_sequence = []

# Nhập chu kỳ (VD: 1 2 1)
cycle_input = st.text_input("🔢 Nhập chu kỳ (VD: 1 2 1):", "1 1")
try:
    pattern = [int(x) for x in cycle_input.strip().split()]
except:
    pattern = [1, 1]

# Giao diện nút
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

# Nếu chưa có tay nào
if not st.session_state.result_sequence:
    st.info("👉 Nhấn Đỏ hoặc Xanh để bắt đầu")
    st.stop()

# === Vẽ Big Road ===
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

# === GỢI Ý TAY TIẾP THEO DỰA TRÊN CHU KỲ ===
seq = st.session_state.result_sequence
cycle_index = 0
pointer = 0
colors = [seq[0]]  # bắt đầu theo màu đầu tiên

for step in pattern:
    for _ in range(step):
        if pointer >= len(seq):
            break
        pointer += 1
    if pointer >= len(seq):
        break
    # đổi màu
    next_color = "🟦" if colors[-1] == "🟥" else "🟥"
    colors.append(next_color)

# Gợi ý tay kế tiếp
if pointer == len(seq):
    next_suggest = colors[-1]
    st.success(f"🔮 **Gợi ý tay tiếp theo theo chu kỳ `{cycle_input}` là: `{next_suggest}`**")

# === VẼ CẦU ===
st.subheader("🧱 Big Road")
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("off")
for (gx, gy), val in grid.items():
    color = "#E53935" if val == '🟥' else "#1E88E5"
    ax.add_patch(plt.Rectangle((gx, -gy), 1, 1, color=color))
    ax.text(gx + 0.5, -gy + 0.5, val, ha="center", va="center", fontsize=16, color="white")
max_x = max((gx for gx, _ in grid), default=1) + 1
ax.set_xlim(0, max_x)
ax.set_ylim(-MAX_ROW, 1)
st.pyplot(fig)
