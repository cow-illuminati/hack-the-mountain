
# Accepte un fichier et retourne le metadata du fps / slow-motion
import cv2

def fps(path):

    video = cv2.VideoCapture(path)

    fps = video.get(cv2.CAP_PROP_FPS)

    video.release()

    return fps
