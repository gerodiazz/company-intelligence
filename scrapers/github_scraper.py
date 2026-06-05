import requests


def get_github_technologies(org):
    url = f"https://api.github.com/orgs/{org}/repos"
    response = requests.get(url)
    data = response.json()

    languages = set()
    for repo in data:
        if repo["language"] is not None:
            languages.add(repo["language"])

    return list(languages)


if __name__ == "__main__":
    print(get_github_technologies("stripe"))
