
#Passe les fichiers un-par-un aux poids, et crée une Dict avec
#TODO

import poids.couleur.hue as hue
import poids.couleur.hue_centre as hue_centre
import poids.couleur.valeur as valeur
import numpy as np

# Retourne le vecteur pour une vidéo
def cat_vid(path, sample=10):
    vect = []
    
    vect.append(valeur.valeur(path, sample))

    # Les hues doivent êtres considérés sur un cercle! 
    vect.append(np.exp((hue.hue(path, sample)/256)*2*np.pi*1j))
    vect.append(np.exp((hue_centre.hue_centre(path,sample)/256)*2*np.pi*1j))

    return vect

# Calcule chaque vidéo et assemble un dict
def parse_vid(path):
    pass

