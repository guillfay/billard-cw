## Coding Week 2023-2024 - Billard Interactif Techniquement Exploitable

## Description
Simulation et affichage d'une billard interactif

## Membres
- Montoya Samuel
- Delavaud Paul-Emile
- Faynot Guillaume
- Noël-Bertin Paul
- Talbaut Gatien

## Libraries

Installation des bibliothèques:
```bash
pip install -r requirements.txt
```

## Détails du projet
### Analyse du problème et des principales fonctionnalités MVP :
- Permettre à l’utilisateur d'interagir avec le billard et régler un tir : choix de la direction et de la puissance du coup
- Permettre la simulation et la visualisation du coup (en 2D vue du dessus) en fonction des paramètres renseignés par l’utilisateur
- Afficher la simulation sous la forme d’une animation à l’aide du module matplotlib
- Permettre d’afficher les différents paramètres connus lors de la simulation

### Fonctionnalités supplémentaires :
- Ajouter d’autres boules et gérer les chocs entre ces dernières (chocs élastiques ou non)
- Permettre le choix du point d’impact sur la boule frappée avec la queue (affichage de la boule vue depuis la queue sur un 2ème affichage)
- Appliquer les conséquences des différents effets causés par ce choix (rotation de la boule, etc.) à la simulation (effets : rétro, coulé, etc.)
- Intégrer la possibilité de jouer une partie de billard français / compter des points (pas le plus important, sort un peu du côté simulation mais est une fonctionnalité sympa et pas trop dure à implémenter)
- Ajouter des trous à la table de billard (pour pouvoir simuler des coups de billard anglais ou américain)
- Intégrer la possibilité de jouer une partie de billard anglais/américain

### Détails des fonctionnalités : 
#### Objectif 1 : MVP
- **:white_check_mark: Sprint 1 : mise en place du modèle du billard**
    - :heavy_check_mark: Fonctionnalité 1 : représentation d’une table de billard et d’une boule
    - :heavy_check_mark: Fonctionnalité 2 : affichage du billard et d’une boule avec `matplotlib`
- **:white_check_mark: Sprint 2 : mise en place du mouvement libre au sein du billard**
    - :heavy_check_mark: Fonctionnalité 3 : simulation du mouvement d’une boule initié par un coup frappé avec la queue
    - :heavy_check_mark: Fonctionnalité 4 : modélisation les interactions entre la boule et le bord de la table de billard (rebonds)
    - :heavy_check_mark: Fonctionnalité 5 : Mise à jour de la position des boules en fonction de la vitesse
- **:white_check_mark: Sprint 3 : mise en place des interactions entre les boules**
    - :heavy_check_mark: Fonctionnalité 6 : modélisation du choc entre les boules
    - :heavy_check_mark: Fonctionnalité 7 : modélisation des frottements avec le tapis
- **:white_check_mark: Sprint 4 : Paramétrer la simulation depuis une ligne de commande**
    - :heavy_check_mark: Fonctionnalité 8 : utilisation du module argparse
    - :heavy_check_mark: Fonctionnalité 9 : écriture d’un programme principal
    - :heavy_check_mark: Fonctionnalité 10 : lancement d’un coup
#### Objectif 2 : Un billard avec `pymunk`
- **:white_check_mark: Sprint 5 : Représentation du billard avec `pymunk`**
    - :heavy_check_mark: Fonctionnalité 11 : Création d'un billard fonctionnel avec `pymunk`
    - :heavy_check_mark: Fonctionnalité 12 : prise en compte de la rotation de la boule    
#### Objectif 3 : un jeu complet
- **:white_check_mark: Sprint 6 : Utilisation d’un GUI**
    - :heavy_check_mark: Fonctionnalité 13 : mise en place d'une interface graphique pour lancer un coup "in-game"
    - :heavy_check_mark: Fonctionnalité 14 : gestion d'une partie de billard