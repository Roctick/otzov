from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.layers import Layer
import tensorflow.keras.backend as K
from tensorflow.keras.saving import register_keras_serializable
import tensorflow as tf
import cv2
import numpy as np

@register_keras_serializable()
class CTCLayer(Layer):
    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.loss_fn = K.ctc_batch_cost

    def call(self, y_true, y_pred):
        batch_len = tf.shape(y_true)[0]
        input_length = tf.shape(y_pred)[1]
        label_length = tf.shape(y_true)[1]
        input_length_tensor = tf.fill([batch_len, 1], input_length)
        label_length_tensor = tf.fill([batch_len, 1], label_length)
        loss = self.loss_fn(y_true, y_pred, input_length_tensor, label_length_tensor)
        self.add_loss(loss)
        return y_pred

    def compute_output_shape(self, input_shape):
        return input_shape

    def get_config(self):
        config = super().get_config()
        return config

try:
    model_path = "C:/Users/kira/Desktop/code/new_captcha/ocr_captcha_model.keras"
    model = load_model(model_path, custom_objects={"CTCLayer": CTCLayer})
    
    # Создание модели для предсказаний (без CTCLayer)
    inference_model = Model(inputs=model.get_layer("image").input, 
                            outputs=model.get_layer("dense2").output)
    print("Модель успешно загружена")
except Exception as e:
    print(f"Ошибка загрузки модели: {e}")

app = Flask(__name__)

# Словарь символов
char_to_index = {char: idx for idx, char in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")}
index_to_char = {idx: char for char, idx in char_to_index.items()}

# Максимальная длина метки (зависит от задачи)
MAX_LABEL_LENGTH = 10

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (200, 50))  # Изменение размера на (200, 50)
    normalized = resized / 255.0
    reshaped = np.expand_dims(normalized, axis=(0, -1))  # Добавление размерностей
    return reshaped

def decode_predictions(predictions):
    """
    Декодирует предсказания модели в текст.
    """
    decoded_texts = []
    for pred in predictions:
        pred_text = ""
        prev_char = -1
        for idx in np.argmax(pred, axis=-1):  # Берём индекс с максимальной вероятностью
            if idx != prev_char:  # Пропуск повторяющихся символов
                if idx < len(index_to_char):  # Пропуск пустых символов
                    pred_text += index_to_char[idx]
            prev_char = idx
        decoded_texts.append(pred_text)
    return decoded_texts

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"error": "Изображение не было отправлено"}), 400

    file = request.files["image"]
    try:
        # Чтение и обработка изображения
        npimg = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if image is None:
            return jsonify({"error": "Не удалось декодировать изображение"}), 400

        preprocessed_image = preprocess_image(image)

        # Предсказание с использованием модели
        predictions = inference_model.predict(preprocessed_image)

        # Декодирование предсказаний
        decoded_predictions = decode_predictions(predictions)
        return jsonify({"predictions": decoded_predictions})
    except Exception as e:
        return jsonify({"error": f"Ошибка во время предсказания: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
