
# Accepte un fichier et retourne le metadata de la résoltion / ratio
import cv2

def res(path):

    video = cv2.VideoCapture(path)

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    video.release()

    if (width < height):
        width = -width

    return width/height
