
import cv2
import numpy as np


## Décoder la vidéo prends 15+ secondes, donc on combine tout ici


# Accepte un fichier et retourne le hue
def hue_centre_valeur(path, samples=10):

    # Charge la vidéo
    video = cv2.VideoCapture(path, cv2.CAP_FFMPEG, [
         cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY
     ])

    video.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)

    # On veut n images, trouvons la longeur 
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    n = int(length/samples)

    # Préparation
    images = []
    index = 0

    # Extraction
    while True:
        
        if not video.grab():
            break

        if index % n == 0:
            ret, frame = video.retrieve()

            if not ret:
                break
    
            images.append(frame)

        index += 1

    
    hues_moy = []
    hues_c_moy = []
    vals_moy = []
 
    # Crop

    height, width, _ = images[0].shape
    ymin = int(height / 3)
    ymax = int(2 * height / 3)
    xmin = int(width / 3)
    xmax = int(2 * width / 3)

   
    for image in images:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        hsv_c = hsv[ymin:ymax, xmin:xmax]


        hues = hsv[:, :, 0]
        hues_moy.append(np.mean(hues))

        hues_c = hsv_c[:, :, 0]
        hues_c_moy.append(np.mean(hues_c))

        vals = hsv[:, :, 2]
        vals_moy.append(np.mean(vals))


    hue_moy = 0
    val_moy = 0
    hue_c_moy = 0
    for hue in hues_moy:
        hue_moy += hue / len(hues_moy)

    for hue_c in hues_c_moy:
        hue_c_moy += hue_c / len(hues_c_moy)
        
    for val in vals_moy:
        val_moy += val / len(vals_moy)
    
    video.release()
    
    return hue_moy, hue_c_moy, val_moy
        
    
