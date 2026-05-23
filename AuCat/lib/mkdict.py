
#Passe les fichiers un-par-un aux poids, et crée une Dict avec
#TODO

import poids.couleur.combined as poids
import numpy as np
import os

# Retourne le vecteur pour une vidéo
def cat_vid(path, sample=10):
    vect = []
    
    hue, hue_c, val = poids.hue_centre_valeur(path, sample)

    vect.append(val)

    # Les hues doivent êtres considérés sur un cercle! 
    vect.append(np.exp(hue/256*2*np.pi*1j))
    vect.append(np.exp(hue_c/256*2*np.pi*1j))

    return vect

# Calcule chaque vidéo et assemble un dict
def parse_vid(path, samples=10):

    cedict = {}
    
    index = 0
    nb = len(os.listdir(path))

    print("Lecture de " + path + "...")
    print(str(nb) + " fichiers trouvés...")

    # Pour chaque vidéo
    for clip in os.scandir(path):
        # Progrès
        print("\r" + str(int(index/nb * 100)) + "% : ", end="")

        # C'est un clip (et non .. ou .)
        if clip.is_file():
            print(clip.name + (" " * 10), end="")
            cedict[os.path.abspath(clip)] = cat_vid(os.path.abspath(clip),samples)

        index += 1

    print("\n\nTerminé..!")
    
    for key, value in cedict.items():
        print(f"{key}: {value}")
    
    return cedict
