
import cv2
import numpy as np


# Accepte un fichier et retourne le hue
def hue_centre(path, samples=10):
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

    hues_moy = []
    
    for image in images:
        height, width, _ = image.shape

        # Crop
        ymin = int(height / 3)
        ymax = int(2 * height / 3)

        xmin = int(width / 3)
        xmax = int(2 * width / 3)
        image = image[ymin:ymax, xmin:xmax]


        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hues = hsv[:, :, 0]
        hues_moy.append(np.mean(hues))

    hue_moy = 0
    for hue in hues_moy:
        hue_moy += hue / len(hues_moy)

    return hue_moy
        
    
