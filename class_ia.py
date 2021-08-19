import random
import sys
from class_de_base import action


class Pile():
    def __init__(self):
        self.stack = []

    def empile(self, x):
        self.stack.append(x)
        return None

    def depile(self):
        try:
            return self.stack.pop()
        except:
            return None

    def resett(self):
        self.stack = []


class User():

    def __init__(self, grille):
        self.grille = grille
        self.coup_jouer = []
        self.table_coor = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,
                           'G': 6, 'H': 7, 'I': 8, 'J': 9}

    def choice_coup(self):
        bad_input = True
        while(bad_input):
            coor_str = input("entrer les coordonnées sous la forme 'x y'\n")
            if coor_str == 'exit':
                sys.exit(0)
            try:
                coor = coor_str.split(' ')
                if coor[0].isalpha():
                    x, y = int(coor[1]) - 1, self.table_coor[coor[0]]
                    if self.grille.is_hide_cell(x, y):
                        bad_input = False
                    else:
                        print(f"la cellule  {(x, y)} que vous cibler est déjà"
                              " visible")
                else:
                    x, y = int(coor[0]) - 1, self.table_coor[coor[1]]
                    if self.grille.is_hide_cell(x, y):
                        bad_input = False
                    else:
                        print(f"la cellule  {(x, y)} que vous cibler est déjà"
                              " visible")
            except:
                continue
        self.coup_jouer.append((x, y))
        return ((x, y))

    def play_one_tour(self):
        x, y = self.choice_coup()
        return self.grille.see_cell(x, y)


class IA:

    def __init__(self, size, grille):
        self.pile_coup = Pile()
        self.coup_jouer = []
        self.track = False
        self.size_map = size
        self.grille = grille
        self.origine_point = ()

    def search_coup_hori(self, point, operateur):
        x, y = point
        if operateur < 0 and y == 0:
            return None
        elif operateur > 0 and y == 9:
            return None
        else:
            if (self.grille.is_hide_cell(x, y + operateur)):
                return (x, y + operateur)
            else:
                if self.grille.map_cell[x][y + operateur].is_ship():
                    if not self.grille.map_cell[x][y + operateur].is_ship_couler():
                        return self.search_coup_hori((x, y + operateur),
                                                     operateur)
                return None

    def search_coup_verti(self, point_adjacant, operateur):
        x, y = point_adjacant
        if operateur < 0 and x == 0:
            return None
        elif operateur > 0 and x == 9:
            return None
        else:
            if (self.grille.is_hide_cell(x + operateur, y)):
                return (x + operateur, y)
            else:
                if self.grille.map_cell[x + operateur][y].is_ship():
                    if not self.grille.map_cell[x + operateur][y].is_ship_couler():
                        return self.search_coup_verti((x + operateur, y),
                                                      operateur)
                return None

    def next_coup(self, x, y):
        if self.origine_point[0] < x:
            return self.search_coup_verti((x, y), 1)
        elif self.origine_point[0] > x:
            return self.search_coup_verti((x, y), -1)
        elif self.origine_point[1] > y:
            return self.search_coup_hori((x, y), -1)
        else:
            return self.search_coup_hori((x, y), 1)

    def croix_hunt(self, x, y):
        list_coor = []
        coup = self.search_coup_verti((x, y), -1)
        if coup is not None:
            list_coor.append(coup)
        coup = self.search_coup_verti((x, y), 1)
        if coup is not None:
            list_coor.append(coup)
        coup = self.search_coup_hori((x, y), 1)
        if coup is not None:
            list_coor.append(coup)
        coup = self.search_coup_hori((x, y), -1)
        if coup is not None:
            list_coor.append(coup)
        return list_coor

    def is_all_point_is_couler(self):
        for x in self.coup_jouer:
            if not self.grille.is_ship_couler(x[0], x[1]):
                self.origine_point = x
                return False
        return True


def print_map_not_cache(mapse):
    ligne_affiche = []
    for ligne in mapse.map_cell:
        ligne_affiche = [conv_cell_int_not_cache(i) for i in ligne]
        print(ligne_affiche)


def conv_cell_int_not_cache(cell_m):
    if cell_m.is_ship():
        if cell_m.ship_cell.is_couler():
            return 4
        elif not cell_m.is_hide():
            return 3
        else:
            return 2
    else:
        if cell_m.is_hide():
            return 0
        else:
            return 1


class IaHunter(IA):

    def __init__(self, size_map, grille):
        super().__init__(size_map, grille)
        self.coup_possible = [(i, j) for j in range(size_map) for i in
                              range(size_map)]
        random.shuffle(self.coup_possible)

    def choice_coup(self):
        if self.track:
            # print(f"pile de coup {self.pile_coup.stack}")
            coup = self.pile_coup.depile()
            # print(f"{coup}")
            if coup is None:
                print_map_not_cache(self.grille)
                print(f'{self.coup_jouer}')
            try:
                self.coup_possible.remove(coup)
            except ValueError:
                pass
        else:
            coup = self.coup_possible.pop(0)
        self.coup_jouer.append(coup)
        return coup

    def reset_coup_possible(self):
        self.coup_possible = [(i, j) for j in range(self.size_map) for i in
                              range(self.size_map)]
        random.shuffle(self.coup_possible)
        self.track = False
        self.coup_jouer = []

    def play_one_tour(self):
        coup = self.choice_coup()
        react = self.grille.see_cell(coup[0], coup[1])
        if self.track:
            if react == action.COULER:
                self.origine_point = None
                if self.is_all_point_is_couler():
                    self.track = False
                    self.pile_coup.resett()
                else:
                    self.pile_coup.stack += self.croix_hunt(self.origine_point[0],
                                                            self.origine_point[1])
            elif react == action.TOUCHE:
                coor = self.next_coup(coup[0], coup[1])
                # print(f'next coup {coor}')
                if coor is not None:
                    self.pile_coup.empile(coor)
        else:
            if react == action.TOUCHE:
                self.track = True
                self.origine_point = coup
                self.pile_coup.stack += self.croix_hunt(coup[0], coup[1])
        return react


def combi_pair(member):
    return (member[0] + member[1]) & 1 == 0


class IaHunterUltime(IA):

    def __init__(self, size_map, grille):
        super().__init__(size_map, grille)
        self.coup_possible = [(i, j) for j in range(size_map) for i in
                              range(size_map)]
        self.coup_possible = list(filter(combi_pair, self.coup_possible))
        random.shuffle(self.coup_possible)

    def choice_coup(self):
        if self.track:
            coup = self.pile_coup.depile()
            if coup is None:
                print_map_not_cache(self.grille)
                print(f'{self.coup_jouer}')
            if (coup[0] + coup[1]) % 2 == 0:
                try:
                    self.coup_possible.remove(coup)
                except ValueError:
                    pass
        else:
            coup = self.coup_possible.pop(0)
        self.coup_jouer.append(coup)
        return coup

    def play_one_tour(self):
        coup = self.choice_coup()
        react = self.grille.see_cell(coup[0], coup[1])
        if self.track:
            if react == action.COULER:
                self.origine_point = None
                if self.is_all_point_is_couler():
                    self.track = False
                    self.pile_coup.resett()
                else:
                    self.pile_coup.stack += self.croix_hunt(self.origine_point[0],
                                                            self.origine_point[1])

            elif react == action.TOUCHE:
                coor = self.next_coup(coup[0], coup[1])
                # print(f'next coup {coor}')
                if coor is not None:
                    self.pile_coup.empile(coor)
        else:
            if react == action.TOUCHE:
                self.track = True
                self.origine_point = coup
                self.pile_coup.stack += self.croix_hunt(coup[0], coup[1])
        return react

    def reset_coup_possible(self):
        self.coup_possible = [(i, j) for j in range(self.size_map) for i in
                              range(self.size_map)]
        self.coup_possible = list(filter(combi_pair, self.coup_possible))
        self.track = False
        self.coup_jouer = []


class IaDumb(IA):

    def __init__(self, size_map, grille):
        super().__init__(size_map, grille)
        self.coup_possible = [(i, j) for j in range(size_map) for i in
                              range(size_map)]
        random.shuffle(self.coup_possible)

    def choice_coup(self):
        coup = self.coup_possible.pop(0)
        self.coup_jouer.append(coup)
        return coup

    def play_one_tour(self):
        coup = self.choice_coup()
        react = self.grille.see_cell(coup[0], coup[1])
        return react

    def reset_coup_possible(self):
        self.coup_possible = [(i, j) for j in range(self.size_map) for i in
                              range(self.size_map)]
        random.shuffle(self.coup_possible)
        self.coup_jouer = []
