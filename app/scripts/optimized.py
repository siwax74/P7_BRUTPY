import csv
from typing import List, Tuple, Dict, Any

from app.utils.utils import read_file

def start_optimized(csv, max_budget):
    """Point d'entrée principal pour le programme.

    Args:
        max_budget (float): Le budget maximum disponible.
        filename (str): Le nom du fichier CSV à lire.
    """
    datas = read_file(csv)
    result = knapsack_dp(max_budget, datas)

    print("Meilleure combinaison d'actions:")
    for action in result["actions"]:
        action_name, cost, benefit = action
        print(f"{action_name} - Coût: {cost:.2f} €, Bénéfice: {cost * benefit:.2f} €")
    print(f"\nCoût total: {sum(cost for _, cost, _ in result['actions']):.2f} €")
    print(f"Bénéfice total après 2 ans: {result['total_benefit']:.2f} €")
    
def knapsack_dp(max_budget: float, datas: Tuple[Tuple[str, float, float]]) -> Dict[str, Any]:
    """Utilise la programmation dynamique pour trouver la meilleure combinaison d'actions sous contrainte de budget.

    Args:
        max_budget (float): Le budget maximum disponible.
        datas (Tuple[Tuple[str, float, float]]): Les données des actions.

    Returns:
        Dict[str, Any]: La meilleure combinaison trouvée avec le bénéfice total.
    """
    n = len(datas)
    max_budget = int(max_budget * 100)  # Convertir le budget en centimes pour éviter les flottants
    costs = [int(cost * 100) for _, cost, _ in datas]
    benefits = [int(cost * benefit * 100) for _, cost, benefit in datas]

    # Initialiser la table dp
    dp = [[0] * (max_budget + 1) for _ in range(n + 1)]

    # Remplissage de la table dp
    for i in range(1, n + 1):
        for w in range(max_budget + 1):
            if costs[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - costs[i-1]] + benefits[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    # Reconstruction de la meilleure combinaison
    w = max_budget
    selected_actions = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_actions.append(datas[i-1])
            w -= costs[i-1]

    total_benefit = dp[n][max_budget] / 100.0
    selected_actions.reverse() 

    return {
        "total_benefit": total_benefit,
        "actions": selected_actions
    }