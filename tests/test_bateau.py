# tests/test_bateau.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from bateau import Bateau, PorteAvions, Croiseur, Torpilleur, SousMarin
from grille1 import Grille

def test_positions_bateau_horizontal_vertical():
    b1 = Bateau(1, 1, longueur=3, vertical=False)
    assert b1.positions == [(1,1),(1,2),(1,3)]

    b2 = Bateau(0, 0, longueur=3, vertical=True)
    assert b2.positions == [(0,0),(1,0),(2,0)]

def test_coule():
    g = Grille(5,5)
    b = Bateau(1,1,3)
    g.place_bateau(b)
    # pas encore coulé
    assert not b.coule(g)
    for pos in b.positions:
        g.tirer(pos)
    assert b.coule(g)

def test_sous_classes_longueurs():
    assert PorteAvions(0,0).longueur == 5
    assert Croiseur(0,0).longueur == 4
    assert Torpilleur(0,0).longueur == 3
    assert SousMarin(0,0).longueur == 2
