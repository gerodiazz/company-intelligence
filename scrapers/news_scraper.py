import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://newsapi.org/v2/everything"


def get_company_news(company):
    params = {
        "q": f"{company} AND (technology OR software OR funding OR AI OR product)",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": os.getenv("NEWSAPI_KEY")
    }
    response = requests.get(url, params=params)
    articles = response.json()["articles"]

    company_lower = company.lower()
    news = []
    for article in articles:
        title = article["title"] or ""
        description = article["description"] or ""
        if company_lower not in title.lower() and company_lower not in description.lower():
            continue
        news.append({
            "title": title,
            "description": description
        })
        if len(news) >= 10:
            break

    return news


if __name__ == "__main__":
    print(get_company_news("Stripe"))
