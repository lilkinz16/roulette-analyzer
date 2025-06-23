# Xác định nhóm để vẽ cầu Baccarat
# Bạn có thể thay đổi tùy theo chiến thuật (ví dụ: A vs B, hoặc A+C vs B+D,...)
def map_baccarat_symbol(group):
    if group == "A":
        return "🟥"  # Player
    elif group == "B":
        return "🟦"  # Banker
    else:
        return None  # Không vẽ

# Tạo dãy kết quả cho cầu
baccarat_seq = list(filter(None, [map_baccarat_symbol(g) for g in groups]))

# Vẽ cầu Baccarat-style
st.subheader("🧮 Cầu Baccarat theo nhóm A (🟥) và B (🟦)")

columns = []
col = []
last = None

for r in baccarat_seq:
    if r == last:
        col.append(r)
    else:
        if col:
            columns.append(col)
        col = [r]
        last = r
if col:
    columns.append(col)

max_len = max(len(c) for c in columns) if columns else 1
fig, ax = plt.subplots(figsize=(len(columns), max_len))
ax.axis('off')

for x, col in enumerate(columns):
    for y, val in enumerate(col):
        color = "#4CAF50" if val == '🟥' else "#2196F3"
        ax.add_patch(plt.Rectangle((x, -y), 1, 1, color=color))
        ax.text(x + 0.5, -y + 0.5, val, va='center', ha='center', fontsize=16, color='white')

plt.xlim(0, len(columns))
plt.ylim(-max_len, 1)
plt.tight_layout()
st.pyplot(fig)
