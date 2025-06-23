import streamlit as st
import matplotlib.pyplot as plt

# === Hàm xử lý vẽ bảng cầu ===
def draw_big_road(results, title, colors, columns=30):
    grid = []
    x = y = 0
    last = None

    for r in results:
        if r == last:
            y += 1
        else:
            y = 0
            x += 1
        last = r
        while len(grid) <= x:
            grid.append([])
        while len(grid[x]) <= y:
            grid[x].append("")
        grid[x][y] = r

    fig, ax = plt.subplots(figsize=(columns, 6))
    ax.axis("off")

    for i, col in enumerate(grid[:columns]):
        for j, val in enumerate(col):
            color = colors.get(val, "#cccccc")
            ax.add_patch(plt.Rectangle((i, -j), 1, 1, color=color))
            ax.text(i + 0.5, -j + 0.5, val, va='center', ha='center', fontsize=12, color="white")

    st.markdown(f"### 📌 {title}")
    st.pyplot(fig)


# === Hàm cho từng phương pháp ===
def run_strategy(name):
    st.markdown(f"## 🔠 Phương pháp {name}")

    # Số cột
    cols = st.radio(f"Số cột hiển thị:", [10, 30, 50, 100], index=1, key=f"cols_{name}")

    # Nhóm A/B/C/D
    group_A = st.text_input(f"P{name} - Nhóm A:", "0,1,2", key=f"A_{name}")
    group_B = st.text_input(f"P{name} - Nhóm B:", "3,4,5", key=f"B_{name}")
    group_C = st.text_input(f"P{name} - Nhóm C:", "6,7,8", key=f"C_{name}")
    group_D = st.text_input(f"P{name} - Nhóm D:", "9,10,11,12", key=f"D_{name}")

    group_map = {}
    for g, text in zip("ABCD", [group_A, group_B, group_C, group_D]):
        for val in text.split(","):
            val = val.strip()
            if val.isdigit():
                group_map[int(val)] = g

    # Kết quả
    if "results_" + name not in st.session_state:
        st.session_state["results_" + name] = []

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🟥 Đặt ĐỎ", key=f"red_{name}"):
            st.session_state["results_" + name].append("Đ")
    with col2:
        if st.button("🟦 Đặt XANH", key=f"blue_{name}"):
            st.session_state["results_" + name].append("X")
    with col3:
        if st.button("♻️ Reset", key=f"reset_{name}"):
            st.session_state["results_" + name] = []

    # Vẽ bảng
    symbols = st.session_state["results_" + name]
    labels = []
    for i, s in enumerate(symbols):
        color_group = group_map.get(i % 37, "?")
        labels.append(color_group)

    draw_big_road(labels, f"Big Road – Phương pháp {name}", {
        "A": "#E74C3C",  # đỏ
        "B": "#3498DB",  # xanh
        "C": "#F39C12",  # cam
        "D": "#27AE60",  # xanh lá
    }, columns=cols)


# === Giao diện chính ===
st.set_page_config(page_title="Bảng Cầu Baccarat – 3 Phương Pháp", layout="wide")
st.title("🎯 Bảng Cầu Baccarat theo 3 Phương Pháp + Gợi ý nhóm")

col1, col2, col3 = st.columns(3)
with col1:
    run_strategy("1")
with col2:
    run_strategy("2")
with col3:
    run_strategy("3")
