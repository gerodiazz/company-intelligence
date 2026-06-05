from pydantic import BaseModel
from datetime import date

class TechnologyEvent(BaseModel):
    type: str
    value: str
    source: str
    company: str
    date: date
class JobEvent(BaseModel):
    type: str = "job_posting"
    technology: str
    company: str
    date: date

class NewsEvent(BaseModel):
    type: str = "news_event"
    title: str
    description: str
    company: str
    date: date

if __name__ == "__main__":
    event = TechnologyEvent(
        type="technology_detected",
        value="Python",
        source="jobs",
        company="Stripe",
        date=date.today()
    )
    print(event)