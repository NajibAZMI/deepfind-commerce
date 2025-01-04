import cv2
import os

# Répertoire contenant les images
image_dir = "static/images/Windsor_tie"
 # Remplacez par votre répertoire

# Taille cible
target_size = (260, 150)

# Parcourir toutes les images dans le répertoire
for filename in os.listdir(image_dir):
    file_path = os.path.join(image_dir, filename)
    
    # Vérifier si le fichier est une image
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        try:
            # Charger l'image
            img = cv2.imread(file_path)

            # Vérifier si l'image est chargée correctement
            if img is None:
                print(f"Impossible de charger l'image : {file_path}")
                continue

            # Redimensionner l'image
            resized_img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)

            # Écraser l'image originale avec l'image redimensionnée
            cv2.imwrite(file_path, resized_img)
            print(f"Image redimensionnée : {file_path}")
        except Exception as e:
            print(f"Erreur avec le fichier {filename}: {e}")
    else:
        print(f"Fichier ignoré (pas une image) : {filename}")
