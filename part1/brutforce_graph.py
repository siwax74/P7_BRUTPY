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

def find_best_combination(
    max_budget: float,
    datas: Tuple[Tuple[str, float, float]],
    index: int = 0,
    current_combination: List[Tuple[str, float, float]] = [],
    best_combination: Dict[str, Any] = {"total_benefit": 0, "actions": []}
) -> Dict[str, Any]:
    """Fonction récursive pour trouver la meilleure combinaison d'actions avec un budget donné."""
    total_cost = sum(cost for _, cost, _ in current_combination)
    total_benefit = sum(cost * benefit for _, cost, benefit in current_combination)

    if total_cost <= max_budget:
        if total_benefit > best_combination["total_benefit"]:
            best_combination["total_benefit"] = total_benefit
            best_combination["actions"] = current_combination[:]

    if index >= len(datas):
        return best_combination

    current_combination.append(datas[index])
    best_combination = find_best_combination(
        max_budget, datas, index + 1, current_combination, best_combination
    )
    current_combination.pop()
    best_combination = find_best_combination(
        max_budget, datas, index + 1, current_combination, best_combination
    )

    return best_combination

def measure_execution_time(datas: Tuple[Tuple[str, float, float]], max_budget: float) -> List[float]:
    """Mesure le temps d'exécution pour différentes tailles de données."""
    times = []
    sizes = list(range(1, len(datas) + 1))
    
    for size in sizes:
        start_time = time.time()
        find_best_combination(max_budget, datas[:size])
        end_time = time.time()
        times.append(end_time - start_time)
    
    return sizes, times

def plot_complexity(sizes: List[int], times: List[float]) -> None:
    """Trace la courbe de complexité."""
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, marker='o')
    plt.title("Complexité temporelle en fonction de la taille des données")
    plt.xlabel("Nombre d'actions")
    plt.ylabel("Temps d'exécution (secondes)")
    plt.grid(True)
    plt.show()

def main(max_budget: float, filename: str) -> None:
    """Point d'entrée principal pour le programme."""
    datas = read_file(filename)
    
    sizes, times = measure_execution_time(datas, max_budget)
    
    plot_complexity(sizes, times)

if __name__ == "__main__":
    filename = "actions.csv"
    max_budget = 500
    main(max_budget, filename)
