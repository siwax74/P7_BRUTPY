import csv
from typing import List, Dict, Any, Tuple

from app.utils.utils import read_file

def start_brutforce(csv: str, max_budget: float) -> None:
    """Point d'entrée principal pour le programme.

    Args:
        csv (str): Le nom du fichier CSV à lire.
        max_budget (float): Le budget maximum disponible.
    """
    print(max_budget)
    datas: List[Tuple[str, float, float]] = read_file(csv)
    best_combination: Dict[str, Any] = {"total_benefit": 0, "actions": []}
    best_combination = find_best_combination(max_budget, datas)

    print("Meilleure combinaison d'actions:")
    for action in best_combination["actions"]:
        action_name, cost, benefit = action
        print(f"{action_name} - Coût: {cost:.2f} €, Bénéfice: {cost * benefit:.2f} €")
    
    print(f"\nCoût total: {sum(cost for _, cost, _ in best_combination['actions']):.2f} €")
    print(f"Bénéfice total après 2 ans: {best_combination['total_benefit']:.2f} €")

def find_best_combination(
    max_budget: float,
    datas: List[Tuple[str, float, float]],
    index: int = 0,
    current_combination: List[Tuple[str, float, float]] = [],
    best_combination: Dict[str, Any] = {"total_benefit": 0, "actions": []}
) -> Dict[str, Any]:
    """Fonction récursive pour trouver la meilleure combinaison d'actions avec un budget donné.

    Args:
        max_budget (float): Le budget maximum disponible.
        datas (List[Tuple[str, float, float]]): Les données des actions sous forme de tuples (nom, coût, bénéfice).
        index (int, optional): L'index actuel dans les données. Defaults to 0.
        current_combination (List[Tuple[str, float, float]], optional): La combinaison actuelle d'actions. Defaults to [].
        best_combination (Dict[str, Any], optional): La meilleure combinaison trouvée. Defaults to {"total_benefit": 0, "actions": []}.

    Returns:
        Dict[str, Any]: La meilleure combinaison trouvée.
    """
    total_cost: float = sum(cost for _, cost, _ in current_combination)
    total_benefit: float = sum(cost * benefit for _, cost, benefit in current_combination)

    if total_cost <= max_budget:
        if total_benefit > best_combination["total_benefit"]:
            best_combination["total_benefit"] = total_benefit
            best_combination["actions"] = current_combination[:]

    if index >= len(datas):
        return best_combination

    # Inclure l'élément courant dans la combinaison
    current_combination.append(datas[index])
    best_combination = find_best_combination(
        max_budget, datas, index + 1, current_combination, best_combination
    )
    
    # Ne pas inclure l'élément courant et continuer
    current_combination.pop()
    best_combination = find_best_combination(
        max_budget, datas, index + 1, current_combination, best_combination
    )
    
    return best_combination
