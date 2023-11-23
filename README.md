## Coding Week 2023-2024 - Billard Interactif Techniquement Exploitable

## Description :clipboard:
Simulation et affichage d'une billard interactif :8ball:

## Membres :man_office_worker:
- Montoya Samuel
- Delavaud Paul-Emile
- Faynot Guillaume
- Noël-Bertin Paul
- Talbaut Gatien

## Bibliothèques :books:

Installation des bibliothèques:
```bash
pip install -r requirements.txt
```
## Lancement de la simulation :chart_with_upwards_trend:
Après avoir installé les bibliothèques requises, taper dans un terminal la commande suivante:
```bash
launch_billard.py 
```
## Soutenance :loudspeaker:
Le support de présentation pour la présentation est accessible [ici](WorkingDocs/presentation.pdf) :point_left:
## Détails du projet :construction:
### Analyse et Conception du produit
Le travail préalable servant à établir les objectifs de notre projet est amorcé par :
- une étude du lanquage omniprésent ou [ubiquitous language](WorkingDocs/ubiquitous%20language.md) dans le but de déterminer un vocabulaire commun
- une analyse des besoins d'un utilisateur en imagninant des scénarios d'utilisation et [user stories](WorkingDocs/user%20story.md)

### Analyse du problème et des principales fonctionnalités MVP :
- Permettre à l’utilisateur d'interagir avec le billard et régler un tir : choix de la direction et de la puissance du coup
- Permettre la simulation et la visualisation du coup (en 2D vue du dessus) en fonction des paramètres renseignés par l’utilisateur : déplacements, rebonds, collisions
- Afficher la simulation sous la forme d’une animation à l’aide du module matplotlib

### Fonctionnalités supplémentaires :
ATTENTION A RELIRE SVP
- Permettre le choix du point d’impact sur la boule frappée avec la queue (affichage de la boule vue depuis la queue sur un 2ème affichage)
- Appliquer les conséquences des différents effets causés par ce choix (rotation de la boule, etc.) à la simulation (effets : rétro, coulé, etc.)
- Modéliser des frottements (résistance au roulement et au glissement)
Intégrer la possibilité de jouer une partie de billard français/américain/anglais
- Ajouter des trous à la table de billard 

### Détails des fonctionnalités : 
#### Objectif 1 : MVP
- **:white_check_mark: Sprint 1 : mise en place du modèle du billard**
    - :heavy_check_mark: Fonctionnalité 1 : représentation d’une table de billard et d’une boule
    - :heavy_check_mark: Fonctionnalité 2 : affichage du billard et d’une boule avec `matplotlib`
- **:white_check_mark: [Sprint 2](WorkingDocs/gif/sprint2-rebond.gif) : mise en place du mouvement libre au sein du billard**
    - :heavy_check_mark: Fonctionnalité 3 : simulation du mouvement d’une boule initié par un coup frappé avec la queue
    - :heavy_check_mark: Fonctionnalité 4 : modélisation les interactions entre la boule et le bord de la table de billard (rebonds)
    - :heavy_check_mark: Fonctionnalité 5 : Mise à jour de la position des boules en fonction de la vitesse
- **:white_check_mark: [Sprint 3](WorkingDocs/gif/sprint3-colision.gif) : mise en place des interactions entre les boules**
    - :heavy_check_mark: Fonctionnalité 6 : modélisation du choc entre les boules
    - :heavy_check_mark: Fonctionnalité 7 : modélisation des frottements avec le tapis
- **:white_check_mark: Sprint 4 : Paramétrer la simulation depuis une ligne de commande**
    - :heavy_check_mark: Fonctionnalité 8 : utilisation du module argparse
    - :heavy_check_mark: Fonctionnalité 9 : écriture d’un programme principal
    - :heavy_check_mark: Fonctionnalité 10 : lancement d’un coup
#### Objectif 2 : un jeu complet
- **:white_check_mark: Sprint 6 : Utilisation d’un GUI**
    - :heavy_check_mark: Fonctionnalité 11 : mise en place d'une interface graphique pour lancer un coup "in-game"
    - :heavy_check_mark: Fonctionnalité 12 : gestion d'une partie de billard
#### Objectif 3 : Un billard avec `pymunk`
- **:white_check_mark: [Sprint 5](WorkingDocs/gif/objectif3-pymunk.gif) : Représentation du billard avec `pymunk`**
    - :heavy_check_mark: Fonctionnalité 13 : création d'un billard fonctionnel avec `pymunk`
    - :heavy_check_mark: Fonctionnalité 14 : prise en compte de la rotation de la boule    
