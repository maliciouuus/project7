import csv
from itertools import combinations
from time import time
import sys

def lire_actions(fichier_csv="data/test_shares.csv"):
    """Lit le fichier CSV et retourne la liste des actions"""
    actions = []
    with open(fichier_csv, 'r') as fichier:
        lecteur = csv.DictReader(fichier)
        # Détermine le format du fichier en fonction des en-têtes
        en_tetes = lecteur.fieldnames
        format_sienna = 'price' in en_tetes and 'profit' in en_tetes
        
        for ligne in lecteur:
            try:
                if format_sienna:
                    cout = float(ligne['price'])
                    benefice_pct = float(ligne['profit'])
                    nom = ligne['name']
                else:
                    cout = float(ligne['Coût par action (en euros)'])
                    benefice_pct = float(ligne['Bénéfice (après 2 ans)'].strip('%'))
                    nom = ligne['Actions #']
                
                if cout > 0 and benefice_pct > 0:
                    benefice = cout * (benefice_pct / 100)
                    actions.append({
                        'nom': nom,
                        'cout': cout,
                        'benefice': benefice
                    })
            except ValueError:
                continue
    return actions

def force_brute(actions, budget_max):
    """Trouve la meilleure combinaison d'actions par force brute"""
    meilleure_combinaison = []
    meilleur_benefice = 0
    nombre_combinaisons = 0
    
    # Test toutes les tailles possibles de combinaisons
    for taille in range(1, len(actions) + 1):
        # Génère toutes les combinaisons possibles de cette taille
        for combo in combinations(actions, taille):
            nombre_combinaisons += 1
            cout_total = sum(action['cout'] for action in combo)
            
            # Vérifie si la combinaison respecte le budget
            if cout_total <= budget_max:
                benefice_total = sum(action['benefice'] for action in combo)
                
                # Met à jour la meilleure combinaison si nécessaire
                if benefice_total > meilleur_benefice:
                    meilleur_benefice = benefice_total
                    meilleure_combinaison = combo
    
    return meilleure_combinaison, meilleur_benefice, nombre_combinaisons

def afficher_resultats(combinaison, benefice_total, temps_execution, nb_combinaisons):
    """Affiche les résultats de manière formatée"""
    print("\nRésultats de l'algorithme force brute:")
    print(f"Temps d'exécution: {temps_execution:.4f} secondes")
    print(f"Nombre de combinaisons testées: {nb_combinaisons}")
    
    cout_total = 0
    print("\n{:<12} {:<15} {:<15} {:<15}".format(
        "Action", "Coût (€)", "Bénéfice (€)", "Rendement (%)"
    ))
    print("-" * 60)
    
    for action in combinaison:
        cout = action['cout']
        benefice = action['benefice']
        rendement = (benefice / cout) * 100
        cout_total += cout
        print("{:<12} {:<15.2f} {:<15.2f} {:<15.2f}".format(
            action['nom'], cout, benefice, rendement
        ))
    
    print("-" * 60)
    print(f"Coût total: {cout_total:.2f} €")
    print(f"Bénéfice total: {benefice_total:.2f} €")
    print(f"Rendement total: {(benefice_total/cout_total)*100:.2f}%")

def main():
    # Paramètres par défaut
    BUDGET_MAX = 500
    fichier_csv = "data/test_shares.csv"
    
    # Gestion des arguments
    if len(sys.argv) > 1:
        try:
            BUDGET_MAX = float(sys.argv[1])
            print(f"Budget personnalisé : {BUDGET_MAX}€")
        except ValueError:
            print("Usage: python bruteforce.py [montant_budget]")
            print("Exemple: python bruteforce.py 345")
            sys.exit(1)
    else:
        print(f"Budget par défaut : {BUDGET_MAX}€")
    
    # Lecture des données
    print("Lecture des données...")
    actions = lire_actions(fichier_csv)
    
    if not actions:
        print("Erreur: Aucune action valide n'a été trouvée dans le fichier.")
        return
    
    # Mesure du temps d'exécution
    debut = time()
    
    # Recherche de la meilleure combinaison
    print("Recherche de la meilleure combinaison...")
    meilleure_combo, meilleur_benefice, nb_combinaisons = force_brute(
        actions, BUDGET_MAX
    )
    
    # Calcul du temps d'exécution
    temps_execution = time() - debut
    
    # Affichage des résultats
    afficher_resultats(meilleure_combo, meilleur_benefice, 
                      temps_execution, nb_combinaisons)

if __name__ == "__main__":
    main()
