from scrapers.detector import analize
from scrapers.jobs import get_job_technologies
from scrapers.github_scraper import get_github_technologies
from scrapers.news_scraper import get_company_news
from models import TechnologyEvent, JobEvent, NewsEvent
from datetime import date

def analyze_company(company, url, github_org=None):
    web_tech = analize(url)
    job_tech = get_job_technologies(company)
    news = get_company_news(company)
    github_tech = get_github_technologies(github_org) if github_org else []

    events = []

    for tech in web_tech["technologies"]:
        events.append(TechnologyEvent(
            type="technology_detected",
            value=tech,
            source="web",
            company=company,
            date=date.today()
        ))

    for tech in job_tech:
        events.append(JobEvent(
            technology=tech,
            company=company,
            date=date.today()
        ))

    for article in news:
        events.append(NewsEvent(
            title=article["title"],
            description=article["description"] or "",
            company=company,
            date=date.today()
        ))

    return {
        "company": company,
        "events": [e.model_dump() for e in events]
    }

if __name__ == "__main__":
    print(analyze_company("Stripe", "https://www.stripe.com", github_org="stripe"))