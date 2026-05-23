import pickle
import dist

# Identifie les îles
def iles(latent):
    
    # Cosin ou euler?
    saveur = 0

    # Temporairement
    with open('_last.dump', 'rb') as file:
        latent = pickle.load(file)
   
    lastval = sorted(latent.items())[0][1]

    # Ordre de nom, pour le test
    for key, value in sorted(latent.items()):
        
        if (not cluster(value, lastval)):
            print ("====================")

        print(key + " -> " + str(dist.dist(value,lastval, 0)) + " | " + str(dist.dist(value,lastval, 1)) + "   :   " + str(value))
        lastval=value


def cluster(vA, vB):
    if (dist.dist(vA,vB, 0) > 1 or dist.dist(vA,vB, 1) > .1 ):
        return False
    else:
        return True


iles({})
