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
    max_budget, datas, index=0, current_combination=[], best_combination={"total_benefit": 0, "actions": []}
):
    """Fonction récursive pour trouver la meilleure combinaison d'actions avec un budget donné."""
    # Calculer le coût et le bénéfice total de la combinaison actuelle
    total_cost = sum(cost for _, cost, _ in current_combination)
    total_benefit = sum(cost * benefit for _, cost, benefit in current_combination)

    # Vérifier si la combinaison actuelle est valide et meilleure que la meilleure trouvée
    if total_cost <= max_budget and total_benefit > best_combination["total_benefit"]:
        best_combination["total_benefit"] = total_benefit
        best_combination["actions"] = current_combination[:]

    # Si toutes les actions ont été explorées, retourner
    if index >= len(datas):
        return
    
    # Essayer la combinaison avec et sans l'action actuelle
    # 1. Inclure l'action actuelle
    current_combination.append(datas[index])
    find_best_combination(max_budget, datas, index + 1, current_combination, best_combination)
    current_combination.pop()  # Retirer l'action pour explorer sans elle
    # 2. Exclure l'action actuelle
    find_best_combination(max_budget, datas, index + 1, current_combination, best_combination)

    return best_combination


def main(max_budget, filename):
    # Lire les données du fichier
    datas = read_file(filename)
    # Initialiser le meilleur résultat
    best_combination = {"total_benefit": 0, "actions": []}
    # Trouver la meilleure combinaison
    best_combination = find_best_combination(max_budget, datas)

    # Afficher les résultats
    print("Meilleure combinaison d'actions:")
    for action in best_combination["actions"]:
        action_name, cost, benefit = action
        print(f"{action_name} - Coût: {cost:.2f} €, Bénéfice: {cost * benefit:.2f} €")
    print(f"\nCoût total: {sum(cost for _, cost, _ in best_combination['actions']):.2f} €")
    print(f"Bénéfice total après 2 ans: {best_combination['total_benefit']:.2f} €")


if __name__ == "__main__":
    filename = "actions.csv"
    max_budget = 500
    main(max_budget, filename)
