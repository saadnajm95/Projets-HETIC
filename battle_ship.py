import time
import random
from enum import Enum
from class_de_base import MapSea
from class_de_base import Ship
from class_de_base import action
from class_de_base import dir
from class_ia import User
from class_ia import IaHunter
from class_ia import IaHunterUltime
from class_ia import IaDumb
from IPython.display import clear_output


class player(Enum):
    USER = 6
    DUMB = 7
    HUNTER = 8
    ULTIMATE = 9


class BattleShip:

    def __init__(self):
        self.map_sea = MapSea(10)
        self.map_sea2 = MapSea(10)
        self.nb_ship_rest = 5
        self.nb_ship_rest2 = 5
        self.list_ship = [Ship(i) for i in range(5, 1, -1)]
        self.list_ship.insert(2, Ship(3))
        self.list_ship2 = [Ship(i) for i in range(5, 1, -1)]
        self.list_ship2.insert(2, Ship(3))
        self.player1 = None
        self.player2 = None

    def party_init(self):
        for sh in self.list_ship:
            sh.reset_ship()
        self.map_sea.reset_map()
        self.nb_ship_rest = 5
        self.generate_grille(self.list_ship, self.map_sea)

    def party_init2(self):
        for sh in self.list_ship2:
            sh.reset_ship()
        self.map_sea2.reset_map()
        self.nb_ship_rest2 = 5
        self.generate_grille(self.list_ship2, self.map_sea2)

    def is_finish(self):
        return self.nb_ship_rest == 0 or self.nb_ship_rest2 == 0

    def generate_grille(self, liste_ship, sea):
        for sh in liste_ship:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            direct = dir.VERTI if 1 == random.randint(1, 2) else dir.HORI
            while(not sea.peut_placer(sh, x, y, direct)):
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                direct = dir.VERTI if 1 == random.randint(1, 2) else dir.HORI
            sea.place_ship(sh, x, y, direct)
        return

    def find_player(self, joueur, grille):
        if joueur is player.USER:
            return User(grille)
        elif joueur is player.DUMB:
            return IaDumb(10, grille)
        elif joueur is player.HUNTER:
            return IaHunter(10, grille)
        else:
            return IaHunterUltime(10, grille)

    def play_nb_game(self, joueur, nb_game):
        """
        docstring
        """
        self.player1 = self.find_player(joueur, self.map_sea)
        self.party_init()
        nb_coup = 0
        for _ in range(nb_game):
            while(not self.is_finish()):
                if self.player1.play_one_tour() == action.COULER:
                    self.nb_ship_rest -= 1
                nb_coup += 1
            self.party_init()
            self.player1.grille = self.map_sea
            self.player1.reset_coup_possible()
        return nb_coup

    def play_one_game(self, joueur, verbose=False, graph=False):
        self.player1 = self.find_player(joueur, self.map_sea)
        self.party_init()
        while(not self.is_finish()):
            if graph:
                clear()
                print_map_cache(self.map_sea)
                print('\n')
            if verbose:
                time.sleep(1)
            if self.player1.play_one_tour() == action.COULER:
                self.nb_ship_rest -= 1
        return (joueur, len(self.player1.coup_jouer))

    def play_one_versus(self, joueur1, joueur2, verbose=False, graph=False):
        self.player1 = self.find_player(joueur1, self.map_sea)
        self.player2 = self.find_player(joueur2, self.map_sea2)
        self.party_init()
        self.party_init2()
        while(not self.is_finish()):
            if graph:
                clear()
                print("tableau de l'adversaire")
                print_map_cache(self.map_sea)
                print("votre tableau")
                print_map_not_cache(self.map_sea2)
            if self.player1.play_one_tour() == action.COULER:
                self.nb_ship_rest -= 1
            if self.player2.play_one_tour() == action.COULER:
                self.nb_ship_rest2 -= 1
        if self.nb_ship_rest == 0:
            us = joueur1
            nb_coup = len(self.player1.coup_jouer)
        else:
            us = joueur2
            nb_coup = len(self.player2.coup_jouer)
        if verbose:
            print(f"le joueur {us} a gagné avec {nb_coup} coup")
        self.nb_ship_rest2 = 5
        return (us, nb_coup)

    def play_user(self, mode):
        if mode == 'alone':
            back = self.play_one_game(player.USER, graph=True)
            print(f"vous avez trouvé en {back[1]}")
            return
        elif mode == 'facile':
            back = self.play_one_versus(player.USER, player.DUMB, graph=True)
            if back[0] == player.DUMB:
                print(f"Vous avez perdu contre l'IA facile après {back[1]}"
                      " coups")
            else:
                print(f"Vous avez perdu contre l'IA facile après {back[1]}"
                      " coups")
                return
        elif mode == 'moyen':
            back = self.play_one_versus(player.USER, player.HUNTER, graph=True)
            if back[0] == player.HUNTER:
                print(f"Vous avez perdu contre l'IA moyen après {back[1]}"
                      " coups")
            else:
                print(f"Vous avez perdu contre l'IA moyen après {back[1]}"
                      " coups")
                return
        elif mode == 'difficile':
            back = self.play_one_versus(player.USER, player.ULTIMATE,
                                        graph=True)
            if back[0] == player.ULTIMATE:
                print(f"Vous avez perdu contre l'IA difficile après {back[1]}"
                      " coups")
            else:
                print(f"Vous avez perdu contre l'IA difficile après {back[1]}"
                      " coups")
                return
        else:
            print(f"le mode ({mode} n\'est pas correct, veillez choisi parmi"
                  " ces propositions:\n -alone\n-facile\n-moyen\n-difficile\n)")
            return None

    def play_versus_nb_party(self, joueur1, joueur2, nb_party):
        self.player1 = self.find_player(joueur1, self.map_sea)
        self.player2 = self.find_player(joueur2, self.map_sea2)
        self.party_init()
        self.party_init2()
        liste_victoire = []
        for _ in range(nb_party):
            while(not self.is_finish()):
                if self.player1.play_one_tour() == action.COULER:
                    self.nb_ship_rest -= 1
                if self.player2.play_one_tour() == action.COULER:
                    self.nb_ship_rest2 -= 1
            if self.nb_ship_rest == 0:
                liste_victoire.append(1)
            else:
                liste_victoire.append(0)
            self.party_init()
            self.party_init2()
            self.player1.grille = self.map_sea
            self.player2.grille = self.map_sea2
            self.player1.reset_coup_possible()
            self.player2.reset_coup_possible()
        return liste_victoire


def print_map_cache(mapse):
    print("  " + "   A   B   C   D   E   F   G   H   I   J")
    for index, ligne in enumerate(mapse.map_cell):
        print("   " + " _"*20)
        colonnes = [str(conv_cell_int_cache(element)) for element in ligne]
        colonne_converti = " | ".join(colonnes)
        colonne_converti = f"| {colonne_converti} |"
        if index + 1 > 9:
            print(f"{index+1} {colonne_converti}")
        else:
            print(f"{index+1}  {colonne_converti}")


def print_map_not_cache(mapse):
    print("  " + "   A   B   C   D   E   F   G   H   I   J")
    for index, ligne in enumerate(mapse.map_cell):
        print("   " + " _"*20)
        colonnes = [str(conv_cell_int_not_cache(element)) for element in ligne]
        colonne_converti = " | ".join(colonnes)
        colonne_converti = f"| {colonne_converti} |"
        if index + 1 > 9:
            print(f"{index+1} {colonne_converti}")
        else:
            print(f"{index+1}  {colonne_converti}")


def conv_cell_int_not_cache(cell_m):
    if cell_m.is_ship():
        if cell_m.ship_cell.is_couler():
            return "♦"
        elif cell_m.is_hide():
            return str(cell_m.ship_cell.lenght)
        else:
            return "♢"
    else:
        if cell_m.is_hide():
            return " "
        else:
            return "o"


def conv_cell_int_cache(cell_m):
    if cell_m.is_hide():
        return " "
    else:
        if cell_m.is_ship():
            if cell_m.ship_cell.is_couler():
                return "♦"
            else:
                return "♢"

        else:
            return "o"


def clear():
    clear_output(wait=True)
