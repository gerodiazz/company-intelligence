import requests, re
import string
import json
from pathlib import Path

from bs4 import BeautifulSoup

DATA_DIR = Path(__file__).parent.parent / "data"


def load_technologies(path):
    result = {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for name, info in data.items():
        if "scriptSrc" in info:
            patterns = info["scriptSrc"]
            if isinstance(patterns, str):
                patterns = [patterns]
            patterns = [p.split("\\;version")[0] for p in patterns]
            result[name] = patterns
    return result


def load_all_technologies():
    all_technologies = {}
    for letter in string.ascii_lowercase:
        try:
            data = load_technologies(DATA_DIR / f"{letter}.json")
            all_technologies.update(data)
        except FileNotFoundError:
            pass
    return all_technologies


technologies = load_all_technologies()


def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def detect_src(soup):
    results_src = set()
    scripts = soup.find_all("script")
    for script in scripts:
        if "src" in script.attrs:
            for name, patterns in technologies.items():
                for pattern in patterns:
                    if re.search(pattern, script["src"]):
                        results_src.add(name)

    return list(results_src)


def detect_meta(soup):
    return []


def ver_scripts(url):
    soup = get_soup(url)
    scripts = soup.find_all("script")
    for script in scripts:
        if "src" in script.attrs:
            print(script["src"])


def analize(url):
    soup = get_soup(url)
    src = detect_src(soup)
    meta = detect_meta(soup)
    return {"url": url, "technologies": src + meta}


if __name__ == "__main__":
    print(analize("https://wordpress.com"))
    print(analize("https://shopify.com"))
    print(analize("https://github.com"))
