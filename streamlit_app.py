import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Phân Tích Roulette", layout="centered")


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
excel_file = data.to_excel(index=False, engine='openpyxl')
st.download_button("Tải xuống kết quả dưới dạng Excel", data=excel_file, file_name="roulette_phan_tich.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    'D': [3, 7, 12, 18, 22, 26, 28, 29, 35],
}

def find_group(num):
    for group, numbers in group_map.items():
        if num in numbers:
            return group
    return "?"

st.title("🎰 Phân Tích Roulette Theo Nhóm A/B/C/D")

results = st.text_input("Nhập dãy số Roulette (phân tách bằng dấu phẩy):", "29, 21, 15, 14, 26")
numbers = [int(x.strip()) for x in results.split(",") if x.strip().isdigit()]
data = pd.DataFrame({"Số": numbers})
data["Nhóm"] = data["Số"].apply(find_group)

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

st.subheader("🧾 Kết quả phân loại")
st.dataframe(data)

st.subheader("📊 Phân tích thống kê")
st.write(f"✅ Nhóm gần nhất: **{latest_group}**")
st.write(f"📌 Độ dài chuỗi liên tiếp: **{streak} lần**")
st.write(f"🎯 Gợi ý nhóm cược: **{suggested}**")

st.subheader("📈 Biểu đồ tần suất nhóm")
fig, ax = plt.subplots()
freq.plot(kind="bar", ax=ax)
st.pyplot(fig)
