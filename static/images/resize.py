import cv2
import os

# Répertoire contenant les images
root_dir = "static/images/"  # Remplacez par votre répertoire racine

# Taille cible
target_size = (260, 170)

# Parcourir tous les fichiers et dossiers dans le répertoire racine
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)

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
                print(f"Erreur avec le fichier {file_path}: {e}")
        else:
            print(f"Fichier ignoré (pas une image) : {file_path}")
