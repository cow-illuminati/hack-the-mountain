
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
        
        if (dist.dist(value,lastval, 0) > 1.5 or dist.dist(value,lastval, 1) > .1 ):
            print ("====================")

        print(key + " -> " + str(dist.dist(value,lastval, 0)) + " | " + str(dist.dist(value,lastval, 1)) + "   :   " + str(value))
        lastval=value


iles({})
