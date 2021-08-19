from enum import Enum


class action(Enum):
    HIDE = 0
    NOTHING = 1
    TOUCHE = 2
    COULER = 3


class dir(Enum):
    HORI = 0
    VERTI = 1


class Ship:
    def __init__(self, lengh):
        if 1 < lengh < 6:
            self.lenght = lengh
            self.life = lengh
        else:
            raise ValueError
        self.couler = False

    def touche(self):
        self.life -= 1
        if self.life == 0:
            self.couler = True
            return action.COULER
        else:
            return action.TOUCHE

    def is_couler(self):
        return self.couler

    def reset_ship(self):
        self.couler = False
        self.life = self.lenght


class Cell:

    def __init__(self):
        self.jouer = False
        self.ship_cell = None

    def change_view(self):
        self.jouer = True
        if self.ship_cell is None:
            return action.NOTHING
        else:
            return self.ship_cell.touche()

    def add_ship(self, ship):
        self.ship_cell = ship

    def is_ship_couler(self):
        if self.ship_cell is not None:
            return self.ship_cell.is_couler()
        else:
            return False

    def is_ship(self):
        return self.ship_cell is not None

    def reset_cell(self):
        self.jouer = False
        self.add_ship(None)

    def is_hide(self):
        return not self.jouer


class MapSea:
    def __init__(self, size):
        self.size = size
        self.map_cell = [[Cell() for _ in range(self.size)] for _ in
                         range(self.size)]

    def place_ship(self, ship, x, y, direct):
        if direct is dir.HORI:
            for i in range(y, ship.lenght + y):
                self.map_cell[x][i].add_ship(ship)
        else:
            for i in range(x, ship.lenght + x):
                self.map_cell[i][y].add_ship(ship)
        return None

    def peut_placer(self, ship, x, y, direct):
        if direct is dir.HORI:
            if (y + ship.lenght) > self.size:
                return False
            elif x > self.size:
                return False
            else:
                for i in range(y, y + ship.lenght):
                    if self.map_cell[x][i].is_ship():
                        return False
                return True
        else:
            if (x + ship.lenght) > self.size:
                return False
            elif 0 > y > self.size:
                return False
            else:
                for i in range(x, x + ship.lenght):
                    if self.map_cell[i][y].is_ship():
                        return False
                return True

    def see_cell(self, x, y):
        return self.map_cell[x][y].change_view()

    def is_hide_cell(self, x, y):
        """docstring."""
        return self.map_cell[x][y].is_hide()

    def is_ship_couler(self, x, y):
        if self.map_cell[x][y].is_ship():
            return self.map_cell[x][y].ship_cell.is_couler()
        else:
            return True

    def reset_map(self):
        for ligne in self.map_cell:
            for cell_m in ligne:
                cell_m.reset_cell()
