import requests
from pathlib import Path

base_url = "https://raw.githubusercontent.com/dochne/wappalyzer/main/src/technologies/{}.json"

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

for letter in "abcdefghijklmnopqrstuvwxyz":
    url = base_url.format(letter)
    response = requests.get(url)
    if response.status_code == 200:
        with open(DATA_DIR / f"{letter}.json", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Descargado: {letter}.json")
    else:
        print(f"No existe: {letter}.json")