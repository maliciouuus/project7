import csv
from time import time
import sys
import os

def lire_actions(nom_fichier):
    """Lit le fichier CSV et retourne la liste des actions"""
    # Construit le chemin du fichier
    fichier_csv = f"data/{nom_fichier}.csv"
    if not os.path.exists(fichier_csv):
        print(f"Erreur: Le fichier {fichier_csv} n'existe pas.")
        sys.exit(1)
        
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
                        'benefice': benefice,
                        'rendement': benefice_pct
                    })
            except ValueError:
                continue
    return actions

def knapsack(actions, budget_max):
    """
    Algorithme du sac à dos (knapsack) pour optimiser l'investissement.
    Utilise la programmation dynamique.
    Complexité temporelle : O(n * W) où n est le nombre d'actions et W le budget
    Complexité spatiale : O(n * W)
    """
    n = len(actions)
    # Conversion du budget en centimes pour éviter les problèmes de précision
    W = int(budget_max * 100)
    
    # Création de la matrice de programmation dynamique
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    # Matrice pour tracer les actions sélectionnées
    keep = [[False for _ in range(W + 1)] for _ in range(n + 1)]
    
    # Remplissage de la matrice
    for i in range(1, n + 1):
        cout_i = int(actions[i-1]['cout'] * 100)  # Conversion en centimes
        benefice_i = actions[i-1]['benefice']
        
        for w in range(W + 1):
            if cout_i <= w:
                if benefice_i + dp[i-1][w-cout_i] > dp[i-1][w]:
                    dp[i][w] = benefice_i + dp[i-1][w-cout_i]
                    keep[i][w] = True
                else:
                    dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = dp[i-1][w]
    
    # Reconstruction de la solution
    selection = []
    w = W
    total_cost = 0
    
    for i in range(n, 0, -1):
        if keep[i][w] and total_cost + actions[i-1]['cout'] <= budget_max:
            selection.append(actions[i-1])
            w -= int(actions[i-1]['cout'] * 100)
            total_cost += actions[i-1]['cout']
    
    return selection, dp[n][W]

def afficher_resultats(combinaison, benefice_total, temps_execution):
    """Affiche les résultats de manière formatée"""
    print("\nRésultats de l'optimisation (Knapsack):")
    print(f"Temps d'exécution: {temps_execution:.4f} secondes")
    
    cout_total = 0
    print("\n{:<12} {:<15} {:<15} {:<15}".format(
        "Action", "Coût (€)", "Bénéfice (€)", "Rendement (%)"
    ))
    print("-" * 60)
    
    for action in combinaison:
        cout = action['cout']
        benefice = action['benefice']
        rendement = action['rendement']
        cout_total += cout
        print("{:<12} {:<15.2f} {:<15.2f} {:<15.2f}".format(
            action['nom'], cout, benefice, rendement
        ))
    
    print("-" * 60)
    print(f"Coût total: {cout_total:.2f} €")
    print(f"Bénéfice total: {benefice_total:.2f} €")
    print(f"Rendement total: {(benefice_total/cout_total)*100:.2f}%")

def main():
    # Vérification des arguments
    if len(sys.argv) < 2:
        print("Usage: python optimized.py <nom_fichier> [montant_budget]")
        print("Exemples:")
        print("  python optimized.py dataset1")
        print("  python optimized.py dataset2 720")
        print("  python optimized.py test_shares")
        print("  python optimized.py test_shares 450")
        sys.exit(1)
    
    # Paramètres par défaut
    BUDGET_MAX = 500
    nom_fichier = sys.argv[1]
    
    # Gestion du budget personnalisé
    if len(sys.argv) > 2:
        try:
            BUDGET_MAX = float(sys.argv[2])
            print(f"Budget personnalisé : {BUDGET_MAX}€")
        except ValueError:
            print("Erreur: Le montant doit être un nombre.")
            sys.exit(1)
    else:
        print(f"Budget par défaut : {BUDGET_MAX}€")
    
    # Lecture des données
    print("Lecture des données...")
    actions = lire_actions(nom_fichier)
    
    if not actions:
        print("Erreur: Aucune action valide n'a été trouvée dans le fichier.")
        return
    
    # Mesure du temps d'exécution
    debut = time()
    
    # Optimisation de l'investissement avec Knapsack
    print("Optimisation de l'investissement...")
    meilleure_combo, meilleur_benefice = knapsack(actions, BUDGET_MAX)
    
    # Calcul du temps d'exécution
    temps_execution = time() - debut
    
    # Affichage des résultats
    afficher_resultats(meilleure_combo, meilleur_benefice, temps_execution)

if __name__ == "__main__":
    main() 