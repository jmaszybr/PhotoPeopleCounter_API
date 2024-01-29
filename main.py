# Importowanie niezbędnych bibliotek
from flask import Flask, request
from flask_restful import Resource, Api
import cv2
import numpy as np
import io
import base64
import requests
from flask_cors import CORS

# Inicjalizacja aplikacji Flask, API i CORS
app = Flask(__name__)
api = Api(app)
CORS(app)


def detect_faces(image):
    # Funkcja do wykrywania twarzy na obrazie
    # Konwersja obrazu na skalę szarości
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Inicjalizacja klasyfikatora twarzy
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Wykrywanie twarzy na obrazie
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Rysowanie prostokątów wokół wykrytych twarzy
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # Zwracanie obrazu z zaznaczonymi twarzami i liczby wykrytych twarzy
    return image, len(faces)


def encode_image(image):
    # Funkcja do kodowania obrazu do formatu base64
    _, buffer = cv2.imencode('.jpg', image)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    return encoded_image


class ImageUploadAnalyzer(Resource):
    # Klasa do analizy obrazów przesłanych przez użytkownika
    def post(self):
        # Sprawdzanie, czy plik został przesłany
        if 'file' not in request.files:
            return {'error': 'Brak pliku do analizy'}, 400

        # Przetwarzanie przesłanego pliku
        file = request.files['file']
        in_memory_file = io.BytesIO()
        file.save(in_memory_file)
        data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)

        # Wykrywanie twarzy na obrazie i kodowanie obrazu
        processed_image, face_count = detect_faces(image.copy())
        original_encoded = encode_image(image)
        processed_encoded = encode_image(processed_image)

        # Zwracanie wyników
        return {
            'original_image': original_encoded,
            'processed_image': processed_encoded,
            'face_count': face_count
        }


class ImageURLAnalyzer(Resource):
    # Klasa do analizy obrazów z URL
    def post(self):
        # Sprawdzanie, czy URL obrazu został przesłany
        if 'image_url' not in request.form:
            return {'error': 'Brak URL obrazu do analizy'}, 400

        # Pobieranie obrazu z URL
        image_url = request.form['image_url']
        response = requests.get(image_url)
        if response.status_code != 200:
            return {'error': 'Nie można pobrać obrazu z podanego URL'}, 400

        # Przetwarzanie pobranego obrazu
        in_memory_file = io.BytesIO(response.content)
        data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)

        # Wykrywanie twarzy na obrazie i kodowanie obrazu
        processed_image, face_count = detect_faces(image.copy())
        original_encoded = encode_image(image)
        processed_encoded = encode_image(processed_image)

        # Zwracanie wyników
        return {
            'original_image': original_encoded,
            'processed_image': processed_encoded,
            'face_count': face_count
        }


class TestImageAnalyzer(Resource):
    # Klasa do analizy obrazu testowego
    def get(self):
        # Ścieżka do obrazu na serwerze
        image_path = 'images/test.png'

        # Wczytanie obrazu
        image = cv2.imread(image_path)

        # Analiza obrazu i wykrywanie twarzy
        processed_image, face_count = detect_faces(image.copy())
        original_encoded = encode_image(image)
        processed_encoded = encode_image(processed_image)

        # Zwracanie wyników
        return {
            'original_image': original_encoded,
            'processed_image': processed_encoded,
            'face_count': face_count
        }


# Dodawanie zasobów do API
api.add_resource(ImageUploadAnalyzer, '/analyze_upload')
api.add_resource(ImageURLAnalyzer, '/analyze_url')
api.add_resource(TestImageAnalyzer, '/analyze_test')

# Definiowanie głównej trasy


@app.route('/')
def home():
    return "Witaj. Przetestuj API uruchamiając załączony w repozytorium plik index.html"


# Uruchamianie aplikacji
if __name__ == '__main__':
    app.run(debug=True)
