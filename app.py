from flask import Flask, request, jsonify
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Charger le modèle pré-entraîné
model = ResNet50(weights='imagenet')

@app.route('/')
def index():
    return "Backend is running. Access the frontend at index.html."
@app.route('/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        print("Aucune image reçue")
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['image']
    print(f"Fichier reçu : {file.filename}")  # Log pour vérifier le fichier
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)
    
    # Charger et prétraiter l'image
    try:
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        print("Image prétraitée avec succès")
    except Exception as e:
        print(f"Erreur lors du prétraitement de l'image : {e}")
        return jsonify({"error": "Error processing image"}), 500

    # Effectuer la prédiction
    try:
        
        preds = model.predict(img_array)
        print(f"Prédictions brutes : {preds}")
        decoded_preds = decode_predictions(preds, top=5)[0]
        products = [f"{pred[1]} ({pred[2]*100:.2f}%)" for pred in decoded_preds]
        print(f"Produits prédits : {products}")
    except Exception as e:
        print(f"Erreur lors de la prédiction : {e}")
        return jsonify({"error": "Error during prediction"}), 500

    # Supprimer le fichier après utilisation
    os.remove(filepath)

    return jsonify({"products": products})


if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
