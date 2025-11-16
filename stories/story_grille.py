import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# stories/story_grille.py
"""
User story simple :
- créer une grille
- placer un bateau
- tirer à quelques positions et afficher le résultat
"""
from grille1 import Grille

class BateauMinimal:
    def __init__(self, positions):
        self.positions = positions
    def coule(self, grille):
        return all(grille[pos] == grille.TOUCHE for pos in self.positions)

def main():
    g = Grille(5, 6)
    b = BateauMinimal([(1,1),(2,1),(3,1)])
    g.place_bateau(b)
    print("Grille initiale:")
    print(g)
    for pos in [(0,0),(1,1),(2,1),(3,1)]:
        res, boat = g.tirer(pos)
        print(f"Tir en {pos} -> {res}")
    print("Grille finale:")
    print(g)

if __name__ == "__main__":
    main()
