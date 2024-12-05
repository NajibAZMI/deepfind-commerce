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
    if 'image' not in request.files:
        return redirect(url_for('index'))

    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        # Sauvegarder le fichier téléchargé
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Prétraitement de l'image pour le modèle
        image = load_img(filepath, target_size=(224, 224))
        image_array = img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array = preprocess_input(image_array)

        # Prédiction des catégories de l'image
        predictions = model.predict(image_array)
        decoded_predictions = decode_predictions(predictions, top=3)[0]  # Top 3 catégories
        category = None
        similar_images = []

        # Vérification des catégories disponibles
        for pred in decoded_predictions:
            possible_category = pred[1]
            similar_images_folder = os.path.join('static/images', possible_category)

            if os.path.exists(similar_images_folder):
                category = possible_category
                similar_images = os.listdir(similar_images_folder)
                break

        # Si aucune correspondance trouvée
        if not category:
            category = decoded_predictions[0][1]  # Catégorie la plus probable
            similar_images = []  # Aucun dossier correspondant

        return render_template('results.html', uploaded_image=filename, category=category, similar_images=similar_images)

# Démarrer l'application
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
