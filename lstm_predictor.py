
# 🔬 Giả lập mô hình LSTM cho dự đoán nhóm tiếp theo
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Chuyển nhóm thành số
def encode_groups(groups):
    le = LabelEncoder()
    encoded = le.fit_transform(groups)
    return encoded, le

# Xây model LSTM đơn giản
def build_lstm_model(input_shape, output_dim):
    model = Sequential()
    model.add(LSTM(32, input_shape=input_shape))
    model.add(Dense(output_dim, activation='softmax'))
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def train_and_predict_lstm(groups):
    if len(groups) < 10:
        return "Không đủ dữ liệu"

    seq_length = 3
    encoded, le = encode_groups(groups)
    X = []
    y = []
    for i in range(len(encoded) - seq_length):
        X.append(encoded[i:i + seq_length])
        y.append(encoded[i + seq_length])
    X = np.array(X)
    y = np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    model = build_lstm_model((seq_length, 1), len(set(encoded)))
    model.fit(X, y, epochs=20, verbose=0)

    last_seq = encoded[-seq_length:].reshape((1, seq_length, 1))
    pred = model.predict(last_seq, verbose=0)
    pred_class = np.argmax(pred)
    return le.inverse_transform([pred_class])[0]
