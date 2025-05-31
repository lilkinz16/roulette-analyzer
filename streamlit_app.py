
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

# Ma trận trực quan nhỏ
st.subheader("🟩 Ma trận màu trực quan")
fig, ax = plt.subplots(figsize=(8, 4))
max_columns = 10
rows = (len(hits) + max_columns - 1) // max_columns
for idx, hit in enumerate(hits):
    row = idx // max_columns
    col = idx % max_columns
    color = "green" if hit == "🟢" else "red" if hit == "🔴" else "lightgray"
    ax.add_patch(plt.Rectangle((col, -row), 1, 1, color=color))
    ax.text(col + 0.5, -row + 0.5, str(numbers[idx]), va="center", ha="center", color="white", fontsize=9)

ax.set_xlim(0, max_columns)
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

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Phân Tích Roulette", layout="centered")

# Nhóm quy ước
group_map = {
    'A': [0, 2, 4, 15, 17, 19, 21, 25, 32, 34],
    'B': [6, 8, 10, 11, 13, 23, 27, 30, 36],
    'C': [1, 5, 9, 14, 16, 20, 24, 31, 33],
    'D': [3, 7, 12, 18, 22, 26, 28, 29, 35],
}
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

# Ma trận trực quan nhỏ
st.subheader("🟩 Ma trận màu trực quan")
fig, ax = plt.subplots(figsize=(8, 4))
max_columns = 10
rows = (len(hits) + max_columns - 1) // max_columns
for idx, hit in enumerate(hits):
    row = idx // max_columns
    col = idx % max_columns
    color = "green" if hit == "🟢" else "red" if hit == "🔴" else "lightgray"
    ax.add_patch(plt.Rectangle((col, -row), 1, 1, color=color))
    ax.text(col + 0.5, -row + 0.5, str(numbers[idx]), va="center", ha="center", color="white", fontsize=9)

ax.set_xlim(0, max_columns)
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


def find_group(num):
    for group, numbers in group_map.items():
        if num in numbers:
            return group
    return "?"

st.title("🎰 Phân Tích Roulette Theo Nhóm A/B/C/D")

results = st.text_input("Nhập dãy số Roulette (phân tách bằng dấu phẩy):", "29, 21, 15, 14, 26, 0, 19")

# Xử lý dữ liệu
numbers = [int(x.strip()) for x in results.split(",") if x.strip().isdigit()]
data = pd.DataFrame({"Số": numbers})
data["Nhóm"] = data["Số"].apply(find_group)
data["Chu kỳ 5 tay"] = (data.index // 5) + 1

# Thống kê
freq = data["Nhóm"].value_counts().sort_index()
latest_group = data["Nhóm"].iloc[-1] if not data.empty else ""
streak = 1
for i in range(len(data) - 2, -1, -1):
    if data["Nhóm"].iloc[i] == latest_group:
        streak += 1
    else:
        break
least_group = freq.idxmin() if not freq.empty else ""
suggested = f"{latest_group} + {least_group}" if latest_group != least_group else latest_group

# Kết quả phân loại
st.subheader("🧾 Kết quả phân loại")
st.dataframe(data)

# Phân tích
st.subheader("📊 Phân tích thống kê")
st.write(f"✅ Nhóm gần nhất: **{latest_group}**")
st.write(f"📌 Độ dài chuỗi liên tiếp: **{streak} lần**")
st.write(f"🎯 Gợi ý nhóm cược: **{suggested}**")

# Biểu đồ
st.subheader("📈 Biểu đồ tần suất nhóm")
fig, ax = plt.subplots()
freq.plot(kind="bar", ax=ax)
plt.xlabel("Nhóm")
plt.ylabel("Số lần xuất hiện")
plt.title("Tần suất xuất hiện của các nhóm")
st.pyplot(fig)

# Tải Excel
st.subheader("📥 Tải kết quả")
from io import BytesIO

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    data.to_excel(writer, index=False)
   
    st.download_button(
        label="📥 Tải xuống kết quả dưới dạng Excel",
        data=buffer.getvalue(),
        file_name="roulette_phan_tich.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

