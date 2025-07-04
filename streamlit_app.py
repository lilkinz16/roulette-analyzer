import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

st.set_page_config(page_title="AION BACCARAT X1", layout="centered")
st.title("🎯 AION BACCARAT X1 – AI Dự đoán Baccarat toàn diện")

# === Session State ===
if "history" not in st.session_state:
    st.session_state.history = []
if "fire_mode" not in st.session_state:
    st.session_state.fire_mode = False
if "mistake_count" not in st.session_state:
    st.session_state.mistake_count = 0
if "model" not in st.session_state:
    st.session_state.model = RandomForestClassifier()
    st.session_state.encoder = LabelEncoder()
    st.session_state.X_train = []
    st.session_state.y_train = []
if "transitions" not in st.session_state:
    st.session_state.transitions = []
if "last_pattern" not in st.session_state:
    st.session_state.last_pattern = None

# === FIRE MODE ===
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🚀 Bật chế độ BẮN"):
        st.session_state.fire_mode = True
    if st.button("🛑 Tắt chế độ BẮN"):
        st.session_state.fire_mode = False
with col2:
    status = "ĐANG BẬT 🔥" if st.session_state.fire_mode else "ĐANG TẮT ❌"
    st.markdown(f"**Chế độ bắn:** `{status}`")

# === Pattern Detection Logic ===
def detect_pattern(streaks):
    if len(streaks) < 2:
        return None
    a, b = streaks[-2:]
    la, lb = len(a), len(b)
    if la == lb:
        return "TYPE_1"
    if la >= 2 and lb == 1:
        return "TYPE_2"
    if la >= 3 and lb == 2:
        return "TYPE_3"
    if la >= 4 and lb == 3:
        return "TYPE_4"
    if la >= 5 and lb == 4:
        return "TYPE_5"
    if la >= 6 and lb == 5:
        return "TYPE_6"
    return None

def parse_streaks(seq):
    streaks = []
    current = ""
    for ch in seq:
        if ch == "T": continue
        if current == "" or current[0] == ch:
            current += ch
        else:
            streaks.append(current)
            current = ch
    if current: streaks.append(current)
    return streaks

def detect_transition(prev_pattern, current_pattern, current_round):
    if not current_pattern:
        return None
    if prev_pattern == "TYPE_1" and current_pattern == "TYPE_2":
        msg = "🔁 TYPE_1 → TYPE_2 (bắt đầu chu kỳ PPB)"
    elif prev_pattern and prev_pattern.startswith("TYPE_1") and current_pattern == "TYPE_1":
        msg = "↘️ TYPE_1 đang rút ngắn (co mẫu)"
    elif prev_pattern != current_pattern:
        msg = f"🔄 {prev_pattern or 'None'} → {current_pattern}"
    else:
        return None

    st.session_state.transitions.append({
        "round": current_round,
        "from": prev_pattern or "None",
        "to": current_pattern,
        "note": msg
    })
    return msg

def tie_probability(seq):
    tie_count = seq.count("T")
    if len(seq) == 0:
        return 0
    return round((tie_count / len(seq)) * 100, 2)

def bet_amount(n):
    base = 20
    return base * (2 ** n) if n < 4 else "STOP"

def update_model():
    if len(st.session_state.X_train) >= 10:
        X = st.session_state.encoder.fit_transform(st.session_state.X_train).reshape(-1, 1)
        y = np.array(st.session_state.y_train)
        st.session_state.model.fit(X, y)

def predict_ml(sequence):
    if len(sequence) < 5:
        return None, 0
    seq5 = sequence[-5:]
    if seq5 not in st.session_state.encoder.classes_:
        return None, 0
    val = st.session_state.encoder.transform([seq5])[0]
    prob = st.session_state.model.predict_proba([[val]])[0]
    labels = st.session_state.model.classes_
    best_idx = np.argmax(prob)
    return labels[best_idx], round(prob[best_idx] * 100, 2)
