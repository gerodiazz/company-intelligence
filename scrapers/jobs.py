import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / "data"

url = "https://jsearch.p.rapidapi.com/search"

headers = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

with open(DATA_DIR / "tech_keywords.json", "r", encoding="utf-8") as f:
    keywords = json.load(f)


def get_job_technologies(company):
    params = {
        "query": f"{company} developer",
        "num_results": 10,
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()["data"]
    all_technologies = set()
    for job in data:
        techs = detect_technologies_in_text(job["job_description"])
        all_technologies.update(techs)

    return list(all_technologies)


def detect_technologies_in_text(text):
    detected = set()

    for category, technologies in keywords.items():
        for tech in technologies:
            if tech.lower() in text.lower():
                detected.add(tech)

    return list(detected)


if __name__ == "__main__":
    print(get_job_technologies("Globant"))
    print(get_job_technologies("Accenture"))
    print(get_job_technologies("Shopify"))
