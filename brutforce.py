import csv
from typing import List, Tuple, Dict, Any


def read_file(filename: str) -> Tuple[Tuple[str, float, float]]:
    """Lit un fichier CSV et retourne les données sous forme de tuple de chaînes formatées.

    Args:
        filename (str): Le nom du fichier CSV à lire.

    Returns:
        Tuple[Tuple[str, float, float]]: Les données sous forme de tuples (action, coût, bénéfice).
    """
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
    best_combination: Dict[str, Any] = {"total_benefit": 0, "actions": []},
    all_combinations: List[Tuple[List[Tuple[str, float, float]], float, float]] = [],
) -> Tuple[Dict[str, Any], List[Tuple[List[Tuple[str, float, float]], float, float]]]:
    """Fonction récursive pour trouver la meilleure combinaison d'actions avec un budget donné.

    Args:
        max_budget (float): Le budget maximum disponible.
        datas (Tuple[Tuple[str, float, float]]): Les données des actions.
        index (int, optional): L'index actuel dans les données. Defaults to 0.
        current_combination (List[Tuple[str, float, float]], optional): La combinaison actuelle d'actions. Defaults to [].
        best_combination (Dict[str, Any], optional): La meilleure combinaison trouvée. Defaults to {"total_benefit": 0, "actions": []}.
        all_combinations (List[Tuple[List[Tuple[str, float, float]], float, float]], optional): Liste de toutes les combinaisons. Defaults to [].

    Returns:
        Tuple[Dict[str, Any], List[Tuple[List[Tuple[str, float, float]], float, float]]]: La meilleure combinaison et toutes les combinaisons.
    """
    total_cost = sum(cost for _, cost, _ in current_combination)
    total_benefit = sum(cost * benefit for _, cost, benefit in current_combination)

    if total_cost <= max_budget:
        if total_benefit > best_combination["total_benefit"]:
            best_combination["total_benefit"] = total_benefit
            best_combination["actions"] = current_combination[:]

        all_combinations.append((current_combination[:], total_cost, total_benefit))

    if index >= len(datas):
        return best_combination, all_combinations

    current_combination.append(datas[index])
    best_combination, all_combinations = find_best_combination(
        max_budget, datas, index + 1, current_combination, best_combination, all_combinations
    )
    current_combination.pop()
    best_combination, all_combinations = find_best_combination(
        max_budget, datas, index + 1, current_combination, best_combination, all_combinations
    )

    return best_combination, all_combinations


def write_combinations_to_csv(
    all_combinations: List[Tuple[List[Tuple[str, float, float]], float, float]], filename: str
) -> None:
    """Écrit toutes les combinaisons d'actions dans un fichier CSV.

    Args:
        all_combinations (List[Tuple[List[Tuple[str, float, float]], float, float]]): Liste de toutes les combinaisons.
        filename (str): Le nom du fichier CSV à écrire.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Actions", "Coût Total", "Bénéfice Total"])
        for combination, total_cost, total_benefit in all_combinations:
            actions_str = ", ".join(action[0] for action in combination)
            writer.writerow([actions_str, total_cost, total_benefit])


def main(max_budget: float, filename: str) -> None:
    """Point d'entrée principal pour le programme.

    Args:
        max_budget (float): Le budget maximum disponible.
        filename (str): Le nom du fichier CSV à lire.
    """
    datas = read_file(filename)
    best_combination = {"total_benefit": 0, "actions": []}
    best_combination, all_combinations = find_best_combination(max_budget, datas)

    print("Meilleure combinaison d'actions:")
    for action in best_combination["actions"]:
        action_name, cost, benefit = action
        print(f"{action_name} - Coût: {cost:.2f} €, Bénéfice: {cost * benefit:.2f} €")
    print(f"\nCoût total: {sum(cost for _, cost, _ in best_combination['actions']):.2f} €")
    print(f"Bénéfice total après 2 ans: {best_combination['total_benefit']:.2f} €")

    write_combinations_to_csv(all_combinations, "all_combinations.csv")


if __name__ == "__main__":
    filename = "actions.csv"
    max_budget = 500
    main(max_budget, filename)
