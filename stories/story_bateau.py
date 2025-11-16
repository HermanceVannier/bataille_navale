# stories/story_bateau.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from bateau import PorteAvions, Croiseur, Torpilleur, SousMarin
from grille1 import Grille

def main():
    g = Grille(8, 10)
    bateaux = [
        PorteAvions(0, 0),
        Croiseur(2, 3, vertical=True),
        Torpilleur(5, 5),
        SousMarin(7, 7)
    ]

    for b in bateaux:
        g.place_bateau(b)

    print("Grille initiale :")
    print(g)
    print()

    # simulation de tirs
    for (r, c) in [(0,0),(0,1),(0,2),(0,3),(0,4),(5,1),(5,2),(5,3)]:
        res, boat = g.tirer((r,c))
        if boat:
            print(f"Tir en {(r,c)} -> {res.upper()} sur {boat}")
        else:
            print(f"Tir en {(r,c)} -> {res.upper()} (à l'eau)")
    print()
    print("Grille finale :")
    print(g)

if __name__ == "__main__":
    main()
