# BattleShip_HETIC
## Les fichiers python

Les fichiers python contient le code pour jouer au jeu de la bataille navale.

Le battle_ship.py contient la classe principal pour faire tourner le jeu.
Le fichier classe_de_base.py contient toutes  les class utiles au plateau et au jeu.
Le fichier class_ia contient toutes les classes IA et de l'utilisateur.
Le fichier class_test.py contient toutes les tests unitaires de toutes les classes.


## fichier notebook
Le fichier notebook contient un récapitulif du jeu, ainsi qu'une analyse le jeu des différentes IA et les résultats des matches entre elles.

## Règle de la bataille navale
Ce jeu de société se joue à deux, l’un contre l’autre sur deux grilles où sont placés 5 navires mis en place par les joueurs.

Le but étant de faire couler tous les navires de l’adversaire. C’est à la fois un jeu de réflexion et un jeu de hasard.

## Présentation du projet
Le jeu sera représenté dans le programme par un dictionnaire contenant quatre associations

une association de clé 'plateau' dont la valeur représente l’espace maritime occupé par une flotte de navires
une association de clé 'nbre_cases_occupees' dont la valeur est le nombre de cases occupées par la flotte
une association de clé 'touches' dont la valeur décrit les touchées réalisées par les tirs
et enfin une association de clé 'coups_joues' qui contient l’ensemble des tirs effectués.
La valeur associée à 'plateau' est elle-même un dictionnaire contenant

deux associations de clé 'larg' et 'haut' dont les valeurs sont des nombres entiers donnant la largeur et la hauteur du plateau
et une association de la forme (x,y) : nav pour chaque case de coordonnées (x,y) occupée par un navire, nav étant le nom de ce navire.
La valeur associée à 'touches' est un dictionnaire contenant deux associations

une association de clé 'nb_touches' dont la valeur est le nombre de tirs ayant fait une touche
une association de clé 'etats_navires' dont la valeur est aussi un dictionnaire donnant pour chaque navire le nombre de tirs qu’il peut encore supporter avant de couler.