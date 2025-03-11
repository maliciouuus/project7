import csv
from optimized import knapsack, lire_actions
from time import time

def lire_solution_sienna(fichier):
    """Lit les résultats de Sienna depuis le fichier texte"""
    with open(fichier, 'r') as f:
        contenu = f.read()
        cout = float(contenu.split('Total cost: ')[1].split('€')[0])
        if 'Profit:' in contenu:
            benefice = float(contenu.split('Profit: ')[1].split('€')[0])
        else:
            benefice = float(contenu.split('Total return: ')[1].split('€')[0])
        
        # Extraction des actions
        actions = []
        if 'Share-' in contenu:
            parts = contenu.split('Share-')[1:]
            actions = ['Share-' + p.split()[0] for p in parts]
            
        return cout, benefice, actions

def comparer_dataset(numero_dataset):
    print(f"\nAnalyse comparative - Dataset {numero_dataset}:")
    print("-" * 80)
    
    # Résultats de Sienna
    cout_sienna, benefice_sienna, actions_sienna = lire_solution_sienna(f"data/solution{numero_dataset}_Python+P7.txt")
    rendement_sienna = (benefice_sienna/cout_sienna)*100
    
    # Notre algorithme
    actions = lire_actions(f"dataset{numero_dataset}")
    debut = time()
    combo_knapsack, benefice_knapsack = knapsack(actions, cout_sienna)
    temps_knapsack = time() - debut
    cout_knapsack = sum(action['cout'] for action in combo_knapsack)
    rendement_knapsack = (benefice_knapsack/cout_knapsack)*100
    
    # Affichage comparatif
    print(f"{'Algorithme':<15} {'Temps (s)':<12} {'Coût (€)':<12} {'Bénéfice (€)':<12} {'Rendement (%)':<12} {'Nb Actions':<12}")
    print("-" * 80)
    print(f"{'Knapsack':<15} {temps_knapsack:<12.4f} {cout_knapsack:<12.2f} "
          f"{benefice_knapsack:<12.2f} {rendement_knapsack:<12.2f} {len(combo_knapsack):<12d}")
    print(f"{'Sienna':<15} {'N/A':<12} {cout_sienna:<12.2f} "
          f"{benefice_sienna:<12.2f} {rendement_sienna:<12.2f} {len(actions_sienna):<12d}")
    
    # Différences
    print("\nDifférences avec Sienna:")
    print(f"Bénéfice: {benefice_knapsack - benefice_sienna:.2f}€")
    print(f"Rendement: {rendement_knapsack - rendement_sienna:.2f}%")
    print(f"Utilisation budget: {cout_knapsack - cout_sienna:.2f}€")
    
    return {
        'knapsack': {
            'temps': temps_knapsack,
            'cout': cout_knapsack,
            'benefice': benefice_knapsack,
            'rendement': rendement_knapsack,
            'nb_actions': len(combo_knapsack)
        },
        'sienna': {
            'cout': cout_sienna,
            'benefice': benefice_sienna,
            'rendement': rendement_sienna,
            'nb_actions': len(actions_sienna)
        }
    }

def main():
    resultats = {}
    
    # Test des deux datasets
    for i in [1, 2]:
        resultats[f'dataset{i}'] = comparer_dataset(i)
    
    # Résumé global
    print("\nRésumé Global:")
    print("-" * 80)
    for dataset, res in resultats.items():
        print(f"\n{dataset.upper()}:")
        print(f"Amélioration bénéfice: {res['knapsack']['benefice'] - res['sienna']['benefice']:.2f}€")
        print(f"Amélioration rendement: {res['knapsack']['rendement'] - res['sienna']['rendement']:.2f}%")
        print(f"Différence actions: {res['knapsack']['nb_actions'] - res['sienna']['nb_actions']}")

if __name__ == "__main__":
    main() 