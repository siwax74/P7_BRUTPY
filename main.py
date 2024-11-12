from app.scripts.brutforce import start_brutforce
from app.scripts.optimized import start_optimized

def main(algo_file, csv, max_budget):
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

    max_budget = 500

    main(optimized, actions_2, max_budget)