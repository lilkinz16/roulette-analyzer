import streamlit as st

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

def analyze_baccarat(sequence):
    if len(sequence) < 20:
        return {"error": "Nhập tối thiểu 20 ký tự kết quả."}

    sequence = sequence.upper()
    base = sequence[:10]
    main = sequence[10:]
    groups = group_results(sequence)

    last = main[-1]
    prev = main[-2] if len(main) >= 2 else None
    prediction = "⚠️"
    pattern = "Unknown"
    confidence = 0
    risk = "Normal"

    if prev and last == prev:
        pattern = "Momentum"
        prediction = last
        confidence = 70
    elif prev and ((prev == "P" and last == "B") or (prev == "B" and last == "P")):
        pattern = "Pingpong"
        prediction = "B" if last == "P" else "P"
        confidence = 65
    else:
        pattern = "Trap Zone"
        risk = "Trap"
        confidence = 50

    recommendation = "Avoid"
    if confidence >= 60:
        recommendation = "Play"

    return {
        "developerView": groups,
        "prediction": prediction,
        "confidence": confidence,
        "pattern": pattern,
        "risk": risk,
        "recommendation": recommendation,
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
            st.markdown(f"**🔮 Prediction:** {result['prediction']}")
            st.markdown(f"**🎯 Accuracy:** {result['confidence']}%")
            st.markdown(f"**📍 Risk:** {result['risk']}")
            st.markdown(f"**🧾 Recommendation:** {result['recommendation']}")

if __name__ == "__main__":
    main()
