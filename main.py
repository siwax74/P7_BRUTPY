from app.scripts.brutforce import start_brutforce
from app.scripts.optimized import start_optimized
from typing import Union

def main(algo_file: str, csv: str, max_budget: int) -> Union[None, True]:
    if algo_file == "app/brutforce.py":
        return start_brutforce(csv, max_budget)
    elif algo_file == "app/optimized.py":
        return start_optimized(csv, max_budget)

if __name__ == "__main__":
    
    # bruteforce / optimized.py
    brut_force = "app/brutforce.py"
    optimized = "app/optimized.py"

    # CSV
    actions_1 = "datas/actions_1.csv"
    actions_2 = "datas/actions_2.csv"
    actions_3 = "datas/actions_3.csv"

    # MAX_BUDGET
    max_budget = 500

    # Choisissez votre script "ALGORITHME" ainsi que le fichier "CSV" et votre "MAX_BUDGET" #
    #    ALGORITHME    CSV      MAX_BUDGET
    #        |          |           |
    #        V          V           V
    main(brut_force, actions_1, max_budget)