from flask import Flask, request, jsonify
from keras.applications import VGG16
from keras.applications.vgg16 import preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Charger le modèle pré-entraîné
model = VGG16(weights="imagenet")

# Produits de démonstration
PRODUCTS = [
    {"name": "Camera Sony", "category": "camera", "image": "static/images/télécharger.jpg", "price": 500},
    {"name": "Camera Canon", "category": "camera", "image": "static/images/camera2.jpg", "price": 600},
    {"name": "Smartphone Samsung", "category": "smartphone", "image": "static/images/smartphone1.jpg", "price": 300},
    {"name": "Smartphone iPhone", "category": "smartphone", "image": "static/images/smartphone2.jpg", "price": 1000},
    {"name": "Télévision LG", "category": "tv", "image": "static/images/tv1.jpg", "price": 800},
]

# Endpoint pour classifier une image
@app.route("/classify", methods=["POST"])
def classify_image():
    file = request.files["image"]
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Sauvegarde temporaire
    file_path = os.path.join("static", "uploads", file.filename)
    file.save(file_path)

    # Prétraitement de l'image
    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Classification
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=1)
    category = decoded_predictions[0][0][1]  # Catégorie la plus probable

    # Recherche de produits similaires
    similar_products = [p for p in PRODUCTS if category in p["category"]]

    return jsonify({"products": similar_products})

if __name__ == "__main__":
    os.makedirs("static/uploads", exist_ok=True)
    app.run(debug=True)
