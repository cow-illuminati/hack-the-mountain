import pickle
import lib.dist.dist as dist
from pathlib import Path

# Identifie les îles
def isles(latent):

    if (Path("_last.dump").exists()):
        with open('_last.dump', 'rb') as file:
            latent = pickle.load(file)

    lastval = sorted(latent.items())[0][1]

    print("Génération d'îles...")

    isles = []
    
    sous_isle = []

    # Ordre de nom, pour le test
    for key, value in sorted(latent.items()):

        if (not cluster(value, lastval)):
            print ("====================")
            isles.append(sous_isle)
            sous_isle = []

        sous_isle.append(key)
        print(key + " -> " + str(dist.dist(value,lastval, 0)) + " | " + str(dist.dist(value,lastval, 1)) + "   :   " + str(value))
        lastval = value
    isles.append(sous_isle)

    print("\nIsles:\n")
    print(isles) 
    return isles


def cluster(vA, vB):
    if (dist.dist(vA,vB, 0) > 1 or dist.dist(vA,vB, 1) > .1 ):
        return False
    else:
        return True


