import csv
from typing import List, Tuple, Dict, Any

def read_file(filename: str) -> Tuple[Tuple[str, float, float]]:
    """Lit un fichier CSV et retourne les données sous forme de tuple de chaînes formatées."""
    datas = []
    with open(filename, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            action = data["name"]
            cost = float(data["price"])
            benefit_percentage = float(data["profit"])
            benefit = benefit_percentage / 100
            if cost > 0:
                datas.append((action, cost, benefit))
    return tuple(datas)

def knapsack_dp(max_budget: float, datas: Tuple[Tuple[str, float, float]]) -> Dict[str, Any]:
    """Utilise la programmation dynamique pour trouver la meilleure combinaison d'actions sous contrainte de budget."""
    n = len(datas)
    max_budget = int(max_budget * 100)
    costs = [int(cost * 100) for _, cost, _ in datas]
    benefits = [int(cost * benefit * 100) for _, cost, benefit in datas]

    dp = [[0] * (max_budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(max_budget + 1):
            if costs[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - costs[i-1]] + benefits[i-1])
            else:
                dp[i][w] = dp[i-1][w]

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

def main(max_budget: float, filename: str) -> None:
    """Point d'entrée principal pour le programme."""
    datas = read_file(filename)
    
    if not datas:
        print("Aucune donnée valide à traiter.")
        return

    result = knapsack_dp(max_budget, datas)

    print("Meilleure combinaison d'actions:")
    for action in result["actions"]:
        action_name, cost, benefit = action
        print(f"{action_name} - Coût: {cost:.2f} €, Bénéfice: {cost * benefit:.2f} €")
    
    total_cost = sum(cost for _, cost, _ in result["actions"])
    print(f"\nCoût total: {total_cost:.2f} €")
    print(f"Bénéfice total après 2 ans: {result['total_benefit']:.2f} €")

if __name__ == "__main__":
    filename = "dataset1.csv"
    max_budget = 500
    main(max_budget, filename)
