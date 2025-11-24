import os
import pandas as pd

env = os.environ.get("ENVIRONMENT", "dev")

file_map = {
    "dev": "data/dev.csv",
    "test": "data/test.csv",
    "prod": "data/prod.csv"
}

file_path = file_map.get(env.lower())
if not file_path:
    raise ValueError(f"Environnement inconnu : {env}")

print(f"=== Lecture du fichier pour l'environnement : {env} ===")
df = pd.read_csv(file_path)
print(df)
