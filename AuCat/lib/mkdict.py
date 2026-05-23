
#Passe les fichiers un-par-un aux poids, et crée une Dict avec

import poids.couleur.combined as poids
import numpy as np
import poids.metadata.fps as fps
import poids.metadata.res as res
import os
import pickle


# Retourne le vecteur pour une vidéo
def cat_vid(path, sample=10):
    vect = []
    
    hue, hue_c, val, sat = poids.hue_centre_valeur_sat(path, sample)
   
    vect.append(val/100-1.28 - .5)

    vect.append(sat/75-1.7+.5)

    # Les hues doivent êtres considérés sur un cercle! 
    vect.append(np.exp(hue/256*2*np.pi*1j)*0.75)
    vect.append(np.exp(hue_c/256*2*np.pi*1j)*2.5)
    

    vect.append(fps.fps(path)/30-30)
    vect.append(res.res(path) - 1)

    return vect

# Calcule chaque vidéo et assemble un dict
def parse_vid(path, samples=15):

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
            print(clip.name + (" " * 16), end="")
            cedict[os.path.abspath(clip)] = cat_vid(os.path.abspath(clip),samples)

        index += 1

    print("\n\nTerminé..!")
    
    for key, value in cedict.items():
        print(f"{key}: {value}")

    # Dumps to file for debugging
    with open('_last.dump', 'wb') as file:
        pickle.dump(cedict, file)

    return cedict
