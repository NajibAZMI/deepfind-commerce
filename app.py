from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import numpy as np
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Initialisation de l'application Flask
app = Flask(__name__)

# Dossier pour stocker les images téléchargées
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Chargement du modèle pré-entraîné
model = MobileNet(weights='imagenet')

# Route principale
@app.route('/')
def index():
    return render_template('index.html')

# Route pour gérer le téléchargement d'image
@app.route('/upload', methods=['POST'])
def upload():
    search_query = request.form.get('search', '')  # Récupère la requête de recherche (si présente)

    if 'image' in request.files:
        file = request.files['image']
        if file.filename == '':
            return redirect(url_for('index'))

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Prétraitement de l'image pour le modèle
        image = load_img(filepath, target_size=(224, 224))
        image_array = img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array = preprocess_input(image_array)

        # Prédiction de la catégorie de l'image
        predictions = model.predict(image_array)
        decoded_predictions = decode_predictions(predictions, top=1)[0]
        category = decoded_predictions[0][1]  # Nom de la catégorie prédite

        # Récupération des images similaires
        similar_images_folder = os.path.join('static/images', category)
        if os.path.exists(similar_images_folder):
            similar_images = os.listdir(similar_images_folder)
        else:
            similar_images = []

        # Filtrer les images en fonction de la recherche
        if search_query:
            similar_images = [img for img in similar_images if search_query.lower() in img.lower()]

        return render_template('index.html', uploaded_image=filename, category=category, similar_images=similar_images, search_query=search_query)

    return redirect(url_for('index'))

# Démarrer l'application
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
