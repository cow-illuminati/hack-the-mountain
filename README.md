# AutoCat: Catégorisation vidéo automatique.

## Fonctionnalitées:
Après un long tournage, que ça soit des intrevues, conférences, court métrages ou reportages, un cinéaste se retrouver avec plusieurs gigaoctets de prises sur plusieurs cartes SD et doit les trier manuellement.

AutoCat offre une solution à ce problème, en analysant chaque vidéo afin d'identifier à quelle scène elle appartient et lui donne un nom significatif pour une intervention humaine plus efficace.

## Utilisation: 
Sur Windows, invoquez ``run.bat``
Sur Linux, invoquez ``run.sh``

Entrez l'emplacement des scènes à trier, et lancez le regroupement.
Les médias seront renommés en fonction des scènes

## Statistiques:
Vitesse : 3 minutes par gigaoctet

Taux de classification : 93.7%

Taux de réussite : 98.3%

## Fonctionnement:
AutoCat commence par analyser les vidéos et leurs attribuer une série de poids.

Ensuite, ces poids sont insérés dans un espace latent complexe à 7 dimensions.

Un algorithme de pairage identifie ensuite les distances entre les îlots.

Enfin, les deltas sont utilisés pour trouver les débuts et fin des scènes.

Les fichiers sont ensuite renommés alphabétiquement pour l'identification humaine rapide.
