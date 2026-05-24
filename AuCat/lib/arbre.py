import pickle
import dist

# Identifie les îles
def iles(latent):
    
    lastval = sorted(latent.items())[0][1]

    print("Génération d'îles...")

    isles = []
    
    sous_isle = []

    # Ordre de nom, pour le test
    for key, value in sorted(latent.items()):
        
        sous_isle.append(key)

        if (not cluster(value, lastval)):
            print ("====================")
            isles.append(sous_isle)
            sous_isle = []

        print(key + " -> " + str(dist.dist(value,lastval, 0)) + " | " + str(dist.dist(value,lastval, 1)) + "   :   " + str(value))
        lastval = value
       
    return isles


def cluster(vA, vB):
    if (dist.dist(vA,vB, 0) > 1 or dist.dist(vA,vB, 1) > .1 ):
        return False
    else:
        return True


print(iles({}))
