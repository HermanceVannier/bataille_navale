# main.py
import random
from grille1 import Grille, ErreurPlacement
from bateau import PorteAvions, Croiseur, Torpilleur, SousMarin

def placer_bateaux_aleatoirement(grille):
    """Place un ensemble de bateaux aléatoirement sans chevauchement."""
    types = [PorteAvions, Croiseur, Torpilleur, SousMarin]
    bateaux = []

    for TypeBateau in types:
        placé = False
        while not placé:
            vertical = random.choice([True, False])
            ligne = random.randint(0, grille.lignes - 1)
            colonne = random.randint(0, grille.colonnes - 1)
            b = TypeBateau(ligne, colonne, vertical)
            try:
                grille.place_bateau(b)
                bateaux.append(b)
                placé = True
            except ErreurPlacement:
                # on recommence
                continue
    return bateaux


def tous_coules(bateaux, grille):
    """Vérifie si tous les bateaux sont coulés."""
    return all(b.coule(grille) for b in bateaux)


def afficher_intro():
    print("🚢  Bienvenue dans la Bataille Navale !")
    print("Entrez les coordonnées du tir sous la forme : ligne colonne (ex : 3 5)")
    print("---------------------------------------------------------")


def main():
    lignes, colonnes = 8, 10
    grille = Grille(lignes, colonnes)
    bateaux = placer_bateaux_aleatoirement(grille)

    afficher_intro()
    coups = 0

    while not tous_coules(bateaux, grille):
        print()
        print(grille)
        print()
        try:
            tir = input("➡️  Votre tir (ligne colonne) : ").strip()
            if tir.lower() in {"q", "quit", "exit"}:
                print("Fin de partie.")
                return
            ligne, colonne = map(int, tir.split())
            res, bateau = grille.tirer((ligne, colonne))
            coups += 1
            if res == "miss":
                print("🌊 Plouf ! Rien touché.")
            elif res == "hit":
                print("🔥 Touché !")
            elif res == "sunk":
                print(f"💥 Coulé ! ({bateau})")
            elif res == "repeat":
                print("⚠️  Déjà tiré ici.")
        except ValueError:
            print("❌ Entrée invalide. Exemple : 3 5")
        except IndexError:
            print("❌ En dehors de la grille.")
    print()
    print("🏆 Tous les bateaux sont coulés ! Bravo !")
    print(f"Nombre total de tirs : {coups}")


if __name__ == "__main__":
    main()
