import unittest
import random
from class_de_base import Cell
from class_de_base import dir
from class_de_base import action
from class_de_base import Ship
from class_de_base import MapSea
from class_ia import IaDumb
from class_ia import IaHunter
from class_ia import IaHunterUltime
from class_ia import Pile
from battle_ship import BattleShip


class test_ship(unittest.TestCase):

    def setUp(self):
        self.ship_test = Ship(2)

    def test_init_ship_except_lenght(self):
        self.assertEqual(2, self.ship_test.lenght)
        self.assertEqual(2, self.ship_test.life)
        self.assertFalse(self.ship_test.couler)

    def test_touche(self):
        self.assertEqual(2, self.ship_test.life)
        self.assertEqual(action.TOUCHE, self.ship_test.touche())
        self.assertEqual(1, self.ship_test.life)
        self.assertEqual(2, self.ship_test.lenght)
        self.assertFalse(self.ship_test.couler)
        self.assertEqual(action.COULER, self.ship_test.touche())
        self.assertEqual(0, self.ship_test.life)
        self.assertTrue(self.ship_test.couler)

    def test_is_couler(self):
        self.assertFalse(self.ship_test.is_couler())
        self.ship_test.touche()
        self.ship_test.touche()
        self.assertTrue(self.ship_test.is_couler())

    def test_reset_ship(self):
        self.ship_test.touche()
        self.ship_test.touche()
        self.assertEqual(0, self.ship_test.life)
        self.assertTrue(self.ship_test.couler)
        self.ship_test.reset_ship()
        self.assertEqual(2, self.ship_test.life)
        self.assertFalse(self.ship_test.couler)


class test_Cell(unittest.TestCase):

    def setUp(self):
        self.ship_test = Ship(2)
        self.cell_test = Cell()

    def test_init(self):
        self.assertFalse(self.cell_test.jouer)
        self.assertIsNone(self.cell_test.ship_cell)

    def test_change_view(self):
        self.assertEqual(self.cell_test.change_view(), action.NOTHING)
        self.assertTrue(self.cell_test.jouer)

    def test_add_ship(self):
        self.cell_test.add_ship(self.ship_test)
        self.assertIsInstance(self.cell_test.ship_cell, Ship)

    def test_is_ship(self):
        self.cell_test.add_ship(self.ship_test)
        self.assertTrue(self.cell_test.is_ship())

    def test_is_hide(self):
        self.assertTrue(self.cell_test.is_hide())
        self.cell_test.change_view()
        self.assertFalse(self.cell_test.is_hide())


class test_map_sea(unittest.TestCase):

    def setUp(self):
        self.map_sea_test = MapSea(5)
        self.cell_test = Cell()

    def test_map_init(self):
        self.assertEqual(self.map_sea_test.size,
                         len(self.map_sea_test.map_cell))
        self.assertEqual(self.map_sea_test.size,
                         len(self.map_sea_test.map_cell[1]))
        for ligne in self.map_sea_test.map_cell:
            for member in ligne:
                self.assertIsInstance(member, Cell)

    def test_place_ship(self):
        ship1 = Ship(5)
        self.map_sea_test.place_ship(ship1, 0, 0, dir.HORI)
        for i in range(5):
            self.assertTrue(self.map_sea_test.map_cell[0][i].is_ship())
            self.assertTrue(self.map_sea_test.map_cell[0][i].ship_cell.lenght)
        ship2 = Ship(2)
        self.map_sea_test.place_ship(ship2, 1, 1, dir.VERTI)
        for i in range(2):
            self.assertTrue(self.map_sea_test.map_cell[i + 1][1].is_ship())
            self.assertTrue(self.map_sea_test.map_cell[i + 1][1].ship_cell.lenght)
        nb_cell_with_ship = 0
        for ligne in self.map_sea_test.map_cell:
            for cell_m in ligne:
                if cell_m.is_ship():
                    nb_cell_with_ship += 1
        self.assertEqual(7, nb_cell_with_ship)

    def test_peut_placer(self):
        ship1 = Ship(5)
        # test quand il y a rien sur la map
        for i in range(self.map_sea_test.size):
            self.assertTrue(self.map_sea_test.peut_placer(ship1, i, 0,
                                                          dir.HORI))

        for i in range(self.map_sea_test.size):
            self.assertTrue(self.map_sea_test.peut_placer(ship1, 0, i,
                                                          dir.VERTI))

        for i in range(self.map_sea_test.size):
            for j in range(1, self.map_sea_test.size):
                self.assertFalse(self.map_sea_test.peut_placer(ship1, i, j,
                                                               dir.HORI))

        for i in range(1, self.map_sea_test.size):
            for j in range(self.map_sea_test.size):
                self.assertFalse(self.map_sea_test.peut_placer(ship1, i, j,
                                                               dir.VERTI))

        self.map_sea_test.place_ship(ship1, 2, 0, dir.HORI)
        ship2 = Ship(3)
        # test quand il y a un bateau sur la map
        for i in range(self.map_sea_test.size):
            for j in range(self.map_sea_test.size):
                self.assertFalse(self.map_sea_test.peut_placer(ship2, i, j,
                                                               dir.VERTI))

        for i in range(self.map_sea_test.size):
            self.assertFalse(self.map_sea_test.peut_placer(ship2, 0, i,
                                                           dir.VERTI))

        for i in range(3, self.map_sea_test.size):
            self.assertTrue(self.map_sea_test.peut_placer(ship2, i, 0,
                                                          dir.HORI))

    def test_see_cell(self):
        ship2 = Ship(2)
        self.map_sea_test.place_ship(ship2, 1, 0, dir.HORI)
        self.assertEqual(action.NOTHING, self.map_sea_test.see_cell(0, 0))
        self.assertEqual(action.TOUCHE, self.map_sea_test.see_cell(1, 0))
        self.assertEqual(action.COULER, self.map_sea_test.see_cell(1, 1))

    def test_reset_map(self):
        ship1 = Ship(5)
        ship2 = Ship(2)
        self.map_sea_test.place_ship(ship1, 0, 0, dir.HORI)
        self.map_sea_test.place_ship(ship2, 1, 0, dir.VERTI)
        nb_cell_with_ship = 0
        for ligne in self.map_sea_test.map_cell:
            for cell_m in ligne:
                if cell_m.is_ship():
                    nb_cell_with_ship += 1
        self.assertEqual(7, nb_cell_with_ship)
        for ligne in self.map_sea_test.map_cell:
            ligne[0].change_view()
        self.map_sea_test.reset_map()
        nb_cell_with_ship = 0
        for ligne in self.map_sea_test.map_cell:
            for cell_m in ligne:
                if cell_m.is_ship():
                    nb_cell_with_ship += 1
        self.assertEqual(0, nb_cell_with_ship)
        for ligne in self.map_sea_test.map_cell:
            self.assertTrue(ligne[0].is_hide())


class test_BattleShip(unittest.TestCase):
    def setUp(self):
        self.bs_test = BattleShip()

    def test_init_BattleShip(self):
        self.assertIsInstance(self.bs_test.map_sea, MapSea)
        self.assertEqual(5, self.bs_test.nb_ship_rest)
        self.bs_test.play_user('alone')

    def test_is_finish(self):
        self.assertFalse(self.bs_test.is_finish())

    def test_generate_grille(self):
        for ligne in self.bs_test.map_sea.map_cell:
            for cell_m in ligne:
                self.assertFalse(cell_m.is_ship())
        self.bs_test.generate_grille(self.bs_test.list_ship, self.bs_test.map_sea)
        nb_cell_with_ship = 0
        for ligne in self.bs_test.map_sea.map_cell:
            for cell_m in ligne:
                if cell_m.is_ship():
                    nb_cell_with_ship += 1
        self.assertEqual(17, nb_cell_with_ship)


class test_iaDumb(unittest.TestCase):
    def setUp(self):
        self.test_map = MapSea(5)
        self.ia_test = IaDumb(5, self.test_map)

    def test_init_ia_dumb(self):
        self.assertListEqual(self.ia_test.coup_jouer, [])
        self.assertFalse(self.ia_test.track)
        self.assertEqual(self.ia_test.size_map, self.test_map.size)

    def test_choice_coup_ia_dumb(self):
        for _ in range(10):
            random.randint(0, 9)
        self.assertTrue(self.ia_test)

    def test_play_one_tour(self):
        pass


class test_IaHunter(unittest.TestCase):
    def setUp(self):
        self.test_map = MapSea(10)
        self.ia_test = IaHunter(10, self.test_map)

    def test_init_ia_hunter(self):
        self.assertIsInstance(self.ia_test.pile_coup, Pile)
        self.assertListEqual(self.ia_test.coup_jouer, [])
        self.assertFalse(self.ia_test.track)
        self.assertEqual(self.ia_test.size_map, self.test_map.size)
        self.assertEqual(100, len(self.ia_test.coup_possible))

    def test_croix_hunt(self):
        self.assertListEqual([(0, 1), (2, 1), (1, 2), (1, 0)],
                             self.ia_test.croix_hunt(1, 1))
        self.assertListEqual([(1, 0), (0, 1)], self.ia_test.croix_hunt(0, 0))
        self.assertListEqual([(1, 1), (0, 2), (0, 0)],
                             self.ia_test.croix_hunt(0, 1))
        self.assertListEqual([(1, 9), (0, 8)], self.ia_test.croix_hunt(0, 9))
        self.assertListEqual([(0, 9), (2, 9), (1, 8)],
                             self.ia_test.croix_hunt(1, 9))
        self.assertListEqual([(8, 9), (9, 8)], self.ia_test.croix_hunt(9, 9))
        self.assertListEqual([(8, 1), (9, 2), (9, 0)],
                             self.ia_test.croix_hunt(9, 1))
        self.assertListEqual([(8, 0), (9, 1)], self.ia_test.croix_hunt(9, 0))
        self.assertListEqual([(0, 0), (2, 0), (1, 1)],
                             self.ia_test.croix_hunt(1, 0))
        self.test_map.see_cell(0, 1)
        self.test_map.see_cell(1, 1)
        self.test_map.see_cell(8, 1)
        self.test_map.see_cell(2, 9)
        self.assertListEqual([(2, 1), (1, 2), (1, 0)],
                             self.ia_test.croix_hunt(1, 1))
        self.assertListEqual([(1, 0)], self.ia_test.croix_hunt(0, 0))
        self.assertListEqual([(0, 2), (0, 0)], self.ia_test.croix_hunt(0, 1))
        self.assertListEqual([(1, 9), (0, 8)], self.ia_test.croix_hunt(0, 9))
        self.assertListEqual([(0, 9), (1, 8)], self.ia_test.croix_hunt(1, 9))
        self.assertListEqual([(8, 9), (9, 8)], self.ia_test.croix_hunt(9, 9))
        self.assertListEqual([(9, 2), (9, 0)], self.ia_test.croix_hunt(9, 1))
        self.assertListEqual([(8, 0), (9, 1)], self.ia_test.croix_hunt(9, 0))
        self.assertListEqual([(0, 0), (2, 0)], self.ia_test.croix_hunt(1, 0))
        # test avec des case entre les adjacant
        ship3 = Ship(3)
        self.test_map.place_ship(ship3, 5, 5, dir.HORI)
        self.test_map.see_cell(5, 6)
        self.assertListEqual([(4, 5), (6, 5), (5, 7), (5, 4)],
                             self.ia_test.croix_hunt(5, 5))
        self.assertListEqual([(4, 7), (6, 7), (5, 8), (5, 5)],
                             self.ia_test.croix_hunt(5, 7))
        self.assertListEqual([(3, 6), (6, 6), (4, 7), (4, 5)],
                             self.ia_test.croix_hunt(4, 6))
        self.assertListEqual([(4, 6), (7, 6), (6, 7), (6, 5)],
                             self.ia_test.croix_hunt(6, 6))

    def test_next_coup(self):
        self.ia_test.origine_point = (2, 2)
        self.assertTupleEqual((0, 2), self.ia_test.next_coup(1, 2))
        self.assertTupleEqual((4, 2), self.ia_test.next_coup(3, 2))
        self.assertTupleEqual((2, 4), self.ia_test.next_coup(2, 3))
        self.assertTupleEqual((2, 0), self.ia_test.next_coup(2, 1))
        self.ia_test.origine_point = (1, 1)
        self.assertIs(None, self.ia_test.next_coup(0, 1))
        self.assertTupleEqual((3, 1), self.ia_test.next_coup(2, 1))
        self.assertIs(None, self.ia_test.next_coup(1, 0))
        self.assertTupleEqual((1, 3), self.ia_test.next_coup(1, 2))
        self.ia_test.origine_point = (8, 8)
        self.assertTupleEqual((6, 8), self.ia_test.next_coup(7, 8))
        self.assertIs(None, self.ia_test.next_coup(9, 8))
        self.assertTupleEqual((8, 6), self.ia_test.next_coup(8, 7))
        self.assertIs(None, self.ia_test.next_coup(8, 9))
        self.ia_test.origine_point = (2, 2)
        self.ia_test.grille.see_cell(0, 2)
        self.ia_test.grille.see_cell(4, 2)
        self.ia_test.grille.see_cell(2, 0)
        self.ia_test.grille.see_cell(2, 4)
        self.assertIs(None, self.ia_test.next_coup(1, 2))
        self.assertIs(None, self.ia_test.next_coup(3, 2))
        self.assertIs(None, self.ia_test.next_coup(2, 1))
        self.assertIs(None, self.ia_test.next_coup(2, 3))

    def test_choice_coup(self):
        random.seed(a=0)
        self.ia_test.choice_coup()
        self.assertEqual(99, len(self.ia_test.coup_possible))
        self.assertEqual(1, len(self.ia_test.coup_jouer))
        self.ia_test.track = True
        self.ia_test.origine_point = (5, 5)
        self.ia_test.pile_coup.stack += self.ia_test.croix_hunt(5, 5)
        coup = self.ia_test.choice_coup()
        self.assertEqual(3, len(self.ia_test.pile_coup.stack))
        self.assertEqual(98, len(self.ia_test.coup_possible))
        self.assertNotIn(coup, self.ia_test.coup_possible)
        self.assertIn(coup, self.ia_test.coup_jouer)

    def test_play_one_tour_iaHunter(self):
        random.seed(a=0)
        self.ia_test.reset_coup_possible()
        ship1 = Ship(2)
        self.test_map.place_ship(ship1, 8, 0, dir.HORI)
        ship2 = Ship(3)
        self.test_map.place_ship(ship2, 1, 0, dir.HORI)
        ship3 = Ship(3)
        self.test_map.place_ship(ship3, 7, 4, dir.VERTI)
        ship4 = Ship(3)
        self.test_map.place_ship(ship4, 6, 5, dir.VERTI)
        ship5 = Ship(4)
        self.test_map.place_ship(ship5, 1, 9, dir.VERTI)
        self.assertEqual(action.NOTHING, self.ia_test.play_one_tour())
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.COULER, self.ia_test.play_one_tour())
        # premier bateau
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.COULER, self.ia_test.play_one_tour())
        # test bateau juste poser l'un contre l'autre
        self.assertEqual(action.NOTHING, self.ia_test.play_one_tour())
        # premier touche
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.NOTHING, self.ia_test.play_one_tour())
        # correspond au 11eme coup
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.NOTHING, self.ia_test.play_one_tour())
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.COULER, self.ia_test.play_one_tour())
        self.assertEqual(action.NOTHING, self.ia_test.play_one_tour())
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.COULER, self.ia_test.play_one_tour())

    def test_play_one_tour_iaHunter_hard(self):
        random.seed(a=0)
        self.ia_test.reset_coup_possible()
        ship1 = Ship(2)
        self.test_map.place_ship(ship1, 8, 0, dir.HORI)
        ship2 = Ship(3)
        self.test_map.place_ship(ship2, 1, 0, dir.HORI)
        ship3 = Ship(3)
        self.test_map.place_ship(ship3, 7, 4, dir.VERTI)
        ship4 = Ship(3)
        self.test_map.place_ship(ship4, 6, 5, dir.VERTI)
        ship5 = Ship(4)
        self.test_map.place_ship(ship5, 1, 9, dir.VERTI)
        self.assertEqual(action.NOTHING, self.ia_test.play_one_tour())
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.COULER, self.ia_test.play_one_tour())
        # premier bateau
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.COULER, self.ia_test.play_one_tour())
        # test bateau juste poser l'un contre l'autre
        self.assertEqual(action.NOTHING, self.ia_test.play_one_tour())
        # premier touche
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.NOTHING, self.ia_test.play_one_tour())
        # correspond au 11eme coup
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.NOTHING, self.ia_test.play_one_tour())
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.COULER, self.ia_test.play_one_tour())
        self.assertEqual(action.NOTHING, self.ia_test.play_one_tour())
        self.assertEqual(action.TOUCHE, self.ia_test.play_one_tour())
        self.assertEqual(action.COULER, self.ia_test.play_one_tour())


class test_IaHunterUltime(unittest.TestCase):
    def setUp(self):
        self.test_map = MapSea(10)
        self.ia_test = IaHunterUltime(10, self.test_map)

    def test_init_ia_ultimate(self):
        pass

    def test_choice_coup_ulitimate(self):
        random.seed(a=0)
        self.ia_test.choice_coup()
        self.assertEqual(49, len(self.ia_test.coup_possible))
        self.assertEqual(1, len(self.ia_test.coup_jouer))
        self.ia_test.track = True
        self.ia_test.origine_point = (5, 5)
        self.ia_test.pile_coup.stack += self.ia_test.croix_hunt(5, 5)
        # coup = self.ia_test.choice_coup()
        # self.assertEqual(3, len(self.ia_test.pile_coup.stack))
        # self.assertEqual(98, len(self.ia_test.coup_possible))
        # self.assertNotIn(coup, self.ia_test.coup_possible)
        # self.assertIn(coup, self.ia_test.coup_jouer)

    def test_play_one_tour_ultimate(self):
        self.assertEqual(action.NOTHING, self.ia_test.play_one_tour())


if __name__ == '__main__':
    unittest.main()
