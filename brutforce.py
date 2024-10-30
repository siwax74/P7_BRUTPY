import csv

def read_file(filename):
    """Lit un fichier CSV et retourne les données sous forme de tuple de chaînes formatées."""
    datas = []
    with open(filename, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            action = data["Actions #"]
            cost = float(data["Coût par action (en euros)"])
            # Convertir le bénéfice en pourcentage en nombre décimal
            benefit_percentage = float(data["Bénéfice (après 2 ans)"].replace('%', '').strip())
            benefit = benefit_percentage / 100  # Convertir en nombre décimal
            datas.append((action, cost, benefit))

    return tuple(datas)


def go_calculate(max_budget, datas):
    """Calcule le nombre d'actions à acheter pour maximiser le bénéfice avec un
    budget donné, en utilisant les données fournies."""
    print(datas)
    max_benefit = 0
    for action, cost, benefit in datas:
        test = cost * benefit
        max_benefit += test
        print(f"{action}, {max_benefit}")


def go_buy(max_budget, datas):
    """Calcule le budget restant après achats d'actions."""
    for action, cost, benefit in datas:
        if max_budget >= cost:
            max_budget -= cost
            print(f"Achat de l'action: {action}, Coût: {cost}")
        else:
            print(f"Pas assez de budget pour l'action: {action}, Coût: {cost}")

    print(f"Budget restant: {max_budget}")
    print("Finito")


def main(max_budget, filename):
    # Lire le fichier
    datas = read_file(filename)
    go_calculate(max_budget, datas)
    
    """go_buy(max_budget, datas)"""


if __name__ == "__main__":
    filename = "actions.csv"
    max_budget = 500
    main(max_budget, filename)