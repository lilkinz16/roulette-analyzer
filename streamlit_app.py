import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Store failed patterns to avoid reuse
FAILED_PATTERNS = set()

# Define Baccarat grid board size
GRID_COLS = 20
GRID_ROWS = 6


def group_results(results):
    groups = []
    if not results:
        return groups

    current = results[0]
    count = 1
    for i in range(1, len(results)):
        if results[i] == current:
            count += 1
        else:
            groups.append(current * count)
            current = results[i]
            count = 1
    groups.append(current * count)
    return groups

def detect_pattern(groups):
    if not groups:
        return "Unknown"

    last = groups[-1]
    if len(last) >= 4:
        return "Dragon"
    elif len(groups) >= 2 and len(groups[-1]) == 2 and len(groups[-2]) == 2:
        return "Two-Cut"
    elif len(groups) >= 3 and groups[-1][0] != groups[-2][0] != groups[-3][0]:
        return "Pingpong"
    return "Unstable"

def analyze_baccarat(sequence):
    if len(sequence) < 20:
        return {"error": "Nhập tối thiểu 20 ký tự kết quả."}

    sequence = sequence.upper()
    base = sequence[:10]
    main = sequence[10:]
    groups = group_results(sequence)
    pattern_type = detect_pattern(groups)

    last = main[-1]
    prev = main[-2] if len(main) >= 2 else None
    prediction = "⚠️"
    pattern = pattern_type
    confidence = 0
    risk = "Normal"
    strong_signal = "Không"

    if pattern in FAILED_PATTERNS:
        risk = "Trap"
        confidence = 40
        recommendation = "Avoid"
    elif pattern == "Dragon":
        prediction = last
        confidence = 75
        strong_signal = "🔥 Có thể vào tiền mạnh (Dragon)"
    elif pattern == "Two-Cut":
        prediction = "B" if last == "P" else "P"
        confidence = 70
        strong_signal = "✅ Ổn định, có thể cân nhắc"
    elif pattern == "Pingpong":
        prediction = "B" if last == "P" else "P"
        confidence = 65
    else:
        risk = "Trap"
        confidence = 50

    recommendation = "Play" if confidence >= 60 else "Avoid"

    if recommendation == "Avoid":
        FAILED_PATTERNS.add(pattern)

    return {
        "developerView": groups,
        "prediction": prediction,
        "confidence": confidence,
        "pattern": pattern,
        "risk": risk,
        "recommendation": recommendation,
        "strong_signal": strong_signal,
        "backtest": list(main[-10:]),
        "full_sequence": list(sequence),
        "predictions": predict_history(main)
    }

def predict_history(main):
    predictions = []
    for i in range(2, len(main)):
        prev, last = main[i-2], main[i-1]
        guess = "B" if last == "P" else "P" if prev != last else last
        predictions.append((main[i], guess))
    return predictions[-10:]

def render_baccarat_grid(results):
    grid = [["" for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    col = 0
    row = 0
    prev = None

    for symbol in results:
        if symbol != prev:
            col += 1
            row = 0
            prev = symbol
        elif row < GRID_ROWS - 1:
            row += 1
        else:
            col += 1
            row = 0
        if col < GRID_COLS:
            grid[row][col] = symbol

    df = pd.DataFrame(grid)
    st.dataframe(df.style.set_properties(**{'text-align': 'center'}).highlight_null(null_color='white'), height=220)

def plot_trend_chart(data):
    colors = ["blue" if x == "B" else "red" if x == "P" else "gray" for x in data]
    fig = go.Figure(data=go.Scatter(
        x=list(range(1, len(data)+1)),
        y=[1]*len(data),
        mode='markers+text',
        marker=dict(size=14, color=colors),
        text=data,
        textposition="top center"
    ))
    fig.update_layout(
        title="Bản đồ xu hướng toàn trận",
        xaxis_title="Hand",
        yaxis_visible=False,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white",
        height=200
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(page_title="SYNAPSE VISION Baccarat", layout="centered")
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("🎴 SYNAPSE VISION Baccarat")

    user_input = st.text_input("Nhập kết quả (ví dụ: BBPBPPPPPBBPBBBBPPP):")

    if st.button("Phân Tích"):
        result = analyze_baccarat(user_input.strip())

        if "error" in result:
            st.error(result["error"])
        else:
            st.subheader("🔬 Phân Tích")
            st.markdown(f"**🧬 Developer View:** [{', '.join(result['developerView'])}]")
            st.markdown(f"**📊 Pattern Detected:** {result['pattern']}")
            st.markdown(f"**🔮 Prediction:** {result['prediction']}")
            st.markdown(f"**🎯 Accuracy:** {result['confidence']}%")
            st.markdown(f"**📍 Risk:** {result['risk']}")
            st.markdown(f"**🧾 Recommendation:** {result['recommendation']}")
            if result['strong_signal'] != "Không":
                st.success(f"🧠 Gợi ý vào tiền: {result['strong_signal']}")

            st.subheader("📈 Backtest (10 ván gần nhất)")
            for idx, (real, pred) in enumerate(result['predictions']):
                ok = real == pred
                st.markdown(f"#{idx+1}: Thật = `{real}` | Dự = `{pred}` → {'✅' if ok else '❌'}")

            st.subheader("🧮 Bảng Baccarat (lưới trực quan)")
            render_baccarat_grid(result['backtest'])

            st.subheader("📊 Bản đồ xu hướng toàn trận")
            plot_trend_chart(result['full_sequence'])

if __name__ == "__main__":
    main()
