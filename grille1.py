# grille.py
from typing import List, Tuple, Optional, Any

Position = Tuple[int, int]

class ErreurPlacement(Exception):
    """Exception levée quand un bateau déborde ou chevauche."""

class Grille:
    """
    Grille de jeu pour la bataille navale.
    Représentation interne en 1D (ligne * nb_colonnes + colonne).
    Peut stocker des "bateaux" (objets ou listes de positions).
    """

    VIDE = "∿"
    TOUCHE = "x"

    def __init__(self, lignes: int, colonnes: int):
        if lignes <= 0 or colonnes <= 0:
            raise ValueError("lignes et colonnes doivent être > 0")
        self.lignes = lignes
        self.colonnes = colonnes
        self._cells: List[str] = [Grille.VIDE] * (lignes * colonnes)
        # mapping index -> bateau_object (whatever you placed)
        self._pos_to_bateau: dict[int, Any] = {}

    def _index(self, ligne: int, colonne: int) -> int:
        if not (0 <= ligne < self.lignes and 0 <= colonne < self.colonnes):
            raise IndexError("Position hors de la grille")
        return ligne * self.colonnes + colonne

    def __getitem__(self, pos: Position) -> str:
        i = self._index(*pos)
        return self._cells[i]

    def __setitem__(self, pos: Position, value: str) -> None:
        i = self._index(*pos)
        self._cells[i] = value

    def within(self, pos: Position) -> bool:
        ligne, colonne = pos
        return 0 <= ligne < self.lignes and 0 <= colonne < self.colonnes

    def est_vide(self, pos: Position) -> bool:
        return self[pos] == Grille.VIDE

    def place_bateau(self, bateau: Any) -> None:
        """
        Place un bateau sur la grille.
        'bateau' peut être soit :
            - un objet ayant un attribut/méthode `positions` (itérable de (ligne, colonne))
            - une liste/itérable de positions
        Vérifie chevauchement et débordement ; en cas d'erreur lève ErreurPlacement.
        Stocke la référence au bateau dans la table interne.
        """
        if hasattr(bateau, "positions"):
            positions = list(bateau.positions)
        else:
            positions = list(bateau)

        # vérifications
        for pos in positions:
            if not self.within(pos):
                raise ErreurPlacement(f"Bateau déborde hors de la grille : {pos}")
        # chevauchement
        for pos in positions:
            idx = self._index(*pos)
            if idx in self._pos_to_bateau:
                raise ErreurPlacement(f"Chevauchement détecté en {pos}")

        # enregistrement (mais on ne change pas le caractère visible : bateau non affiché)
        for pos in positions:
            idx = self._index(*pos)
            self._pos_to_bateau[idx] = bateau

    def tirer(self, pos: Position, touche: str = TOUCHE) -> Tuple[str, Optional[Any]]:
        """
        Tire à la position pos.
        - si hors grille : IndexError
        - si déjà touché : retourne ("repeat", bateau/None)
        - si miss : marque la case et retourne ("miss", None)
        - si touché : marque 'touche' et retourne ("hit", bateau)
        - si touché et bateau coulé (si bateau a méthode `coule(grille)`), retourne ("sunk", bateau)
        """
        if not self.within(pos):
            raise IndexError("Position hors de la grille")
        idx = self._index(*pos)
        if self._cells[idx] == touche:
            # déjà touché
            return ("repeat", self._pos_to_bateau.get(idx))
        # marque la case
        self._cells[idx] = touche
        bateau = self._pos_to_bateau.get(idx)
        if bateau is None:
            return ("miss", None)
        # si le bateau fournit une méthode `coule(grille)` on l'appelle pour vérifier s'il est coulé
        if hasattr(bateau, "coulé") or hasattr(bateau, "coule"):
            # accept both names with/without accent
            coule_fn = getattr(bateau, "coulé", None) or getattr(bateau, "coule", None)
            try:
                is_coule = bool(coule_fn(self))
            except Exception:
                is_coule = False
            if is_coule:
                return ("sunk", bateau)
        return ("hit", bateau)

    def positions_d_un_bateau(self, bateau: Any) -> List[Position]:
        """Retourne les positions d'un bateau déjà placé (utile pour tests)."""
        retour = []
        for idx, b in self._pos_to_bateau.items():
            if b is bateau:
                ligne = idx // self.colonnes
                col = idx % self.colonnes
                retour.append((ligne, col))
        # tri pour stabilité
        retour.sort()
        return retour

    def __str__(self) -> str:
        # entête colonnes
        header = "   " + " ".join(f"{c:2d}" for c in range(self.colonnes))
        lines = [header]
        for r in range(self.lignes):
            row_cells = " ".join(f"{self[(r, c)]:2s}" for c in range(self.colonnes))
            lines.append(f"{r:2d} {row_cells}")
        return "\n".join(lines)
