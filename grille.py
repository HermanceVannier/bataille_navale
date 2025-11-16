# grille.py
from bateau import Bateau

class ErreurPlacement(Exception):
    pass


class Grille:
    def __init__(self, lignes=8, colonnes=10):
        self.lignes = lignes
        self.colonnes = colonnes
        self.tirs = {}  # (i, j) -> "miss" / "hit"
        self.bateaux = []

    def contient(self, pos):
        i, j = pos
        return 0 <= i < self.lignes and 0 <= j < self.colonnes

    def occupe(self, pos):
        """Retourne True si un bateau occupe cette position."""
        for b in self.bateaux:
            if pos in b.positions:
                return True
        return False

    def place_bateau(self, bateau: Bateau):
        """Place un bateau sur la grille s’il n’y a pas de chevauchement."""
        for pos in bateau.positions:
            if not self.contient(pos):
                raise ErreurPlacement(f"Bateau hors grille en {pos}")
            if self.occupe(pos):
                raise ErreurPlacement(f"Chevauchement détecté en {pos}")
        self.bateaux.append(bateau)

    def tirer(self, pos):
        """Effectue un tir sur la grille."""
        if not self.contient(pos):
            raise IndexError("Tir hors de la grille")

        # déjà tiré ici ?
        if pos in self.tirs:
            return "repeat", None

        # touche ou pas
        for b in self.bateaux:
            if pos in b.positions:
                self.tirs[pos] = "hit"
                if b.coule(self):
                    return "sunk", b.nom
                return "hit", b.nom

        # sinon : raté
        self.tirs[pos] = "miss"
        return "miss", None

    def etat_case(self, pos):
        """Retourne le symbole à afficher pour une case donnée."""
        if pos in self.tirs:
            if self.tirs[pos] == "miss":
                return "x"   # tir dans l’eau
            elif self.tirs[pos] == "hit":
                return "o"   # bateau touché
        return "."           # case non tirée

    def __str__(self):
        """Affiche la grille complète."""
        lignes = []
        header = "   " + " ".join([str(j) for j in range(self.colonnes)])
        lignes.append(header)
        for i in range(self.lignes):
            row = [str(i).rjust(2)]  # numéro de ligne
            for j in range(self.colonnes):
                row.append(self.etat_case((i, j)))
            lignes.append(" ".join(row))
        return "\n".join(lignes)
