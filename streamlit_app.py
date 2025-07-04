import streamlit as st

# Store failed patterns to avoid reuse
FAILED_PATTERNS = set()


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

    if pattern in FAILED_PATTERNS:
        risk = "Trap"
        confidence = 40
        recommendation = "Avoid"
    elif pattern == "Dragon":
        prediction = last
        confidence = 75
    elif pattern == "Two-Cut":
        prediction = "B" if last == "P" else "P"
        confidence = 70
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
        "backtest": list(main[-10:])
    }

def main():
    st.set_page_config(page_title="SYNAPSE VISION Baccarat", layout="centered")
    st.title("SYNAPSE VISION Baccarat")

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

            st.subheader("📈 Backtest (10 ván gần nhất)")
            cols = st.columns(len(result['backtest']))
            for i, (col, outcome) in enumerate(zip(cols, result['backtest'])):
                col.metric(label=f"#{i+1}", value=outcome)

if __name__ == "__main__":
    main()
