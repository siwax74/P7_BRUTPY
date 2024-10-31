import csv


def read_file(filename):
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
    max_budget,
    datas,
    index=0,
    current_combination=[],
    best_combination={"total_benefit": 0, "actions": []},
    all_combinations=[],
):
    """Fonction récursive pour trouver la meilleure combinaison d'actions avec un budget donné."""
    # Calculer le coût et le bénéfice total de la combinaison actuelle
    total_cost = sum(cost for _, cost, _ in current_combination)
    total_benefit = sum(cost * benefit for _, cost, benefit in current_combination)

    # Vérifier si la combinaison actuelle est valide et meilleure que la meilleure trouvée
    if total_cost <= max_budget:
        if total_benefit > best_combination["total_benefit"]:
            best_combination["total_benefit"] = total_benefit
            best_combination["actions"] = current_combination[:]

        # Ajouter la combinaison actuelle à la liste de toutes les combinaisons
        all_combinations.append((current_combination[:], total_cost, total_benefit))

    # Si toutes les actions ont été explorées, retourner
    if index >= len(datas):
        return best_combination, all_combinations

    # Essayer la combinaison avec et sans l'action actuelle
    # 1. Inclure l'action actuelle
    current_combination.append(datas[index])
    best_combination, all_combinations = find_best_combination(
        max_budget, datas, index + 1, current_combination, best_combination, all_combinations
    )
    current_combination.pop()  # Retirer l'action pour explorer sans elle
    # 2. Exclure l'action actuelle
    best_combination, all_combinations = find_best_combination(
        max_budget, datas, index + 1, current_combination, best_combination, all_combinations
    )

    return best_combination, all_combinations

def write_combinations_to_csv(all_combinations, filename):
    """Écrit toutes les combinaisons d'actions dans un fichier CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Actions", "Coût Total", "Bénéfice Total"])
        for combination, total_cost, total_benefit in all_combinations:
            actions_str = ", ".join(action[0] for action in combination)  # Concaténer les noms des actions
            writer.writerow([actions_str, total_cost, total_benefit])


def main(max_budget, filename):
    # Lire les données du fichier
    datas = read_file(filename)
    # Initialiser le meilleur résultat
    best_combination = {"total_benefit": 0, "actions": []}
    # Trouver la meilleure combinaison
    best_combination, all_combinations = find_best_combination(max_budget, datas)

    # Afficher les résultats
    print("Meilleure combinaison d'actions:")
    for action in best_combination["actions"]:
        action_name, cost, benefit = action
        print(f"{action_name} - Coût: {cost:.2f} €, Bénéfice: {cost * benefit:.2f} €")
    print(f"\nCoût total: {sum(cost for _, cost, _ in best_combination['actions']):.2f} €")
    print(f"Bénéfice total après 2 ans: {best_combination['total_benefit']:.2f} €")

    # Écrire toutes les combinaisons dans un fichier CSV
    write_combinations_to_csv(all_combinations, "all_combinations.csv")


if __name__ == "__main__":
    filename = "actions.csv"
    max_budget = 500
    main(max_budget, filename)
