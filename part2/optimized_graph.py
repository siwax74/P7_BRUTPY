import csv
import time
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt

def read_file(filename: str) -> Tuple[Tuple[str, float, float]]:
    """Lit un fichier CSV et retourne les données sous forme de tuple de chaînes formatées."""
    datas = []
    with open(filename, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            action = data["Actions #"]
            cost = float(data["Coût par action (en euros)"])
            benefit_percentage = float(data["Bénéfice (après 2 ans)"].replace("%", "").strip())
            benefit = benefit_percentage / 100
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

def measure_execution_time(datas: Tuple[Tuple[str, float, float]], max_budget: float) -> List[float]:
    """Mesure le temps d'exécution pour différentes tailles de données."""
    times = []
    sizes = list(range(1, len(datas) + 1))
    
    for size in sizes:
        start_time = time.time()
        knapsack_dp(max_budget, datas[:size])
        end_time = time.time()
        times.append(end_time - start_time)
    
    return sizes, times

def plot_complexity(sizes: List[int], times: List[float]) -> None:
    """Trace la courbe de complexité."""
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, marker='o')
    plt.title("Complexité temporelle en fonction de la taille des données (Programmation Dynamique)")
    plt.xlabel("Nombre d'actions")
    plt.ylabel("Temps d'exécution (secondes)")
    plt.grid(True)
    plt.show()

def main(max_budget: float, filename: str) -> None:
    """Point d'entrée principal pour le programme."""
    datas = read_file(filename)
    
    sizes, times = measure_execution_time(datas, max_budget)
    plot_complexity(sizes, times)

    result = knapsack_dp(max_budget, datas)

    print("Meilleure combinaison d'actions:")
    for action in result["actions"]:
        action_name, cost, benefit = action
        print(f"{action_name} - Coût: {cost:.2f} €, Bénéfice: {cost * benefit:.2f} €")
    print(f"\nCoût total: {sum(cost for _, cost, _ in result['actions']):.2f} €")
    print(f"Bénéfice total après 2 ans: {result['total_benefit']:.2f} €")

if __name__ == "__main__":
    filename = "actions.csv"
    max_budget = 500
    main(max_budget, filename)
