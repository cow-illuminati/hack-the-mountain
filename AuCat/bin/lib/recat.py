from pathlib import Path
import os
import random


# Trouve N noms au hasard
def pull_random_names(fichier, n):
    with open(fichier, 'r') as f:
        lines = f.readlines()
    return sorted(random.sample(lines, n))
    
def recat(clusters):

    noms = pull_random_names(Path("src/noms"), len(clusters))
    index = 0
    for isle in clusters:
        for element in isle:
            p = Path(element)
            p.rename(p.with_name(f"{noms[index].strip()}_{p.stem}{p.suffix}"))
        index += 1

