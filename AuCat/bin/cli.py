
import lib.arbre as arbre
import lib.mkdict as mkdict
import lib.recat as recat
from pathlib import Path

def aucat(path):
    ledict = mkdict.parse_vid(path)
    isles = arbre.isles(ledict)
    recat.recat(isles)
    Path("_last.dump").unlink()

aucat("/home/cow/Downloads/test")
                
            
 
