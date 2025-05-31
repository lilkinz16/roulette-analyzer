
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Phân Tích Roulette", layout="centered")

group_map = {
    'A': [0, 2, 4, 15, 17, 19, 21, 25, 32, 34],
    'B': [6, 8, 10, 11, 13, 23, 27, 30, 36],
    'C': [1, 5, 9, 14, 16, 20, 24, 31, 33],
    'D': [3, 7, 12, 18, 22, 26, 28, 29, 35],
}

def find_group(num):
    for group, numbers in group_map.items():
        if num in numbers:
            return group
    return "?"

st.title("🎰 Phân Tích Roulette Theo Nhóm A/B/C/D")

results = st.text_input("Nhập dãy số Roulette (phân tách bằng dấu phẩy):", "29, 21, 15, 14, 26, 0, 19, 1, 4, 12, 6")

# Xử lý dữ liệu
numbers = [int(x.strip()) for x in results.split(",") if x.strip().isdigit()]
data = pd.DataFrame({"Số": numbers})
data["Nhóm"] = data["Số"].apply(find_group)
data["Chu kỳ 5 tay"] = (data.index // 5) + 1

# Gợi ý cược cho từng dòng
suggestions = []
hits = []
for i in range(len(data)):
    if i == 0:
        suggestions.append("—")
        hits.append("⚪")
    else:
        prev_group = data.loc[i - 1, "Nhóm"]
        freq = data.loc[:i - 1, "Nhóm"].value_counts()
        least_group = freq.idxmin() if not freq.empty else ""
        suggestion = f"{prev_group} + {least_group}" if prev_group != least_group else prev_group
        suggestions.append(suggestion)
        current = data.loc[i, "Nhóm"]
        hit = "🟢" if current in suggestion else "🔴"
        hits.append(hit)

data["Gợi ý trước"] = suggestions
data["Kết quả"] = hits

import matplotlib.pyplot as plt

# Hiển thị ma trận màu trực quan như ảnh mẫu
st.subheader("🟩 Ma trận màu nhỏ gọn")

fig, ax = plt.subplots(figsize=(8, 4))
cols = 10
rows = (len(data) + cols - 1) // cols

for idx, row in data.iterrows():
    color = "green" if row["Kết quả"] == "🟢" else "red" if row["Kết quả"] == "🔴" else "gray"
    r = idx // cols
    c = idx % cols
    ax.add_patch(plt.Rectangle((c, -r), 1, 1, color=color))
    ax.text(c + 0.5, -r + 0.5, str(row["Số"]), va="center", ha="center", color="white", fontsize=10, weight="bold")

ax.set_xlim(0, cols)
ax.set_ylim(-rows, 0)
ax.axis("off")
st.pyplot(fig)


# Bảng chi tiết
st.subheader("📋 Bảng chi tiết kết quả")
st.dataframe(data)

# Tải Excel
st.subheader("📥 Tải kết quả")
buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    data.to_excel(writer, index=False)
st.download_button(
    label="📥 Tải xuống kết quả dưới dạng Excel",
    data=buffer.getvalue(),
    file_name="roulette_phan_tich.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
