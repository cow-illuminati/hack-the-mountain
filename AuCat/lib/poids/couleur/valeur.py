
import cv2
import numpy as np


# Accepte un fichier et retourne le hue
def valeur(path, samples=10):
    # Charge la vidéo
    video = cv2.VideoCapture(path)

    # On veut n images, trouvons la longeur 
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    n = int(length/samples)

    # Préparation
    images = []
    index = 0

    # Extraction
    while True:
        
        ret, frame = video.read()

        if not ret:
            break
    
        if index % n == 0:
            images.append(frame)

        index += 1

    vals_moy = []
    
    for image in images:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        vals = hsv[:, :, 2]
        vals_moy.append(np.mean(vals))

    val_moy = 0
    for val in vals_moy:
        val_moy += val / len(vals_moy)

    return val_moy
        
    
