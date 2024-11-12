import csv
from typing import Tuple, List

def read_file(filename: str) -> Tuple[Tuple[str, float, float]]:
    """Lit un fichier CSV et retourne les données sous forme de tuple.

    Args:
        filename (str): Le nom du fichier CSV à lire.

    Returns:
        Tuple[Tuple[str, float, float]]: Les données sous forme de tuples (nom/action, coût/prix, bénéfice).
    """
    datas = []
    with open(filename, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)

        if "Coût par action" in headers or "Bénéfice (après 2 ans)" in headers:
            # Premier format
            for row in reader:
                name = row[0] # Première colonne
                cost = float(row[1]) # Deuxième colonne
                benefit = float(row[2].strip('%')) / 100 # Troisième colonne
                datas.append((name, cost, benefit))
        else:
            # Deuxième format
            for row in reader:
                name = row[0]  
                cost = float(row[1])
                profit = float(row[2]) / 100
                if cost > 0:
                    datas.append((name, cost, profit))

    return tuple(datas)