import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# tests/test_grille.py
import pytest
from grille1 import Grille, ErreurPlacement

class DummyBateau:
    def __init__(self, positions):
        self.positions = list(positions)

    def coule(self, grille):
        # un bateau est coulé si toutes ses positions sont marquées 'x' sur la grille
        for pos in self.positions:
            if grille[pos] != grille.TOUCHE:
                return False
        return True

def test_creation_grille():
    g = Grille(3, 4)
    assert g.lignes == 3
    assert g.colonnes == 4
    # toutes les cases sont vides
    for r in range(3):
        for c in range(4):
            assert g[(r, c)] == Grille.VIDE

def test_place_bateau_and_positions():
    g = Grille(4, 4)
    b = DummyBateau([(1,1), (1,2), (1,3)])
    g.place_bateau(b)
    pos = g.positions_d_un_bateau(b)
    assert pos == [(1,1),(1,2),(1,3)]

def test_chevauchement():
    g = Grille(4, 4)
    b1 = DummyBateau([(0,0),(0,1)])
    b2 = DummyBateau([(0,1),(0,2)])
    g.place_bateau(b1)
    with pytest.raises(ErreurPlacement):
        g.place_bateau(b2)

def test_debordement():
    g = Grille(2, 2)
    b = DummyBateau([(1,1),(1,2)])  # (1,2) hors grille
    with pytest.raises(ErreurPlacement):
        g.place_bateau(b)

def test_tir_miss_and_hit_and_sunk():
    g = Grille(3,3)
    b = DummyBateau([(0,0),(0,1)])
    g.place_bateau(b)

    # miss
    res, boat = g.tirer((2,2))
    assert res == "miss" and boat is None
    # hit
    res, boat = g.tirer((0,0))
    assert res == "hit" and boat is b
    # hit again different cell -> still hit
    res, boat = g.tirer((0,1))
    assert res == "sunk" and boat is b
    # repeat
    res, boat = g.tirer((0,1))
    assert res == "repeat"

