# bateau.py
from typing import List, Tuple
from grille1 import Grille

Position = Tuple[int, int]


class Bateau:
    """Classe de base pour un bateau."""

    SYMBOLE = "⛵"

    def __init__(self, ligne: int, colonne: int, longueur: int, vertical: bool = False):
        self.ligne = ligne
        self.colonne = colonne
        self.longueur = longueur
        self.vertical = vertical

    # positions du bateau (property calculée à partir des attributs)
    @property
    def positions(self) -> List[Position]:
        pos = []
        for i in range(self.longueur):
            if self.vertical:
                pos.append((self.ligne + i, self.colonne))
            else:
                pos.append((self.ligne, self.colonne + i))
        return pos

    def coule(self, grille: Grille) -> bool:
        """Retourne True si toutes les positions du bateau sont marquées comme touchées."""
        for pos in self.positions:
            if grille[pos] != grille.TOUCHE:
                return False
        return True

    def __str__(self):
        orientation = "vertical" if self.vertical else "horizontal"
        return f"{self.__class__.__name__} ({orientation}, taille={self.longueur})"


# --- Sous-classes de bateaux spécifiques ---
class PorteAvions(Bateau):
    SYMBOLE = "🛳️"

    def __init__(self, ligne: int, colonne: int, vertical: bool = False):
        super().__init__(ligne, colonne, longueur=5, vertical=vertical)


class Croiseur(Bateau):
    SYMBOLE = "🚢"

    def __init__(self, ligne: int, colonne: int, vertical: bool = False):
        super().__init__(ligne, colonne, longueur=4, vertical=vertical)


class Torpilleur(Bateau):
    SYMBOLE = "⛴️"

    def __init__(self, ligne: int, colonne: int, vertical: bool = False):
        super().__init__(ligne, colonne, longueur=3, vertical=vertical)


class SousMarin(Bateau):
    SYMBOLE = "🚤"

    def __init__(self, ligne: int, colonne: int, vertical: bool = False):
        super().__init__(ligne, colonne, longueur=2, vertical=vertical)
