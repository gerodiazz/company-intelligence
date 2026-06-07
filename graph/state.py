from typing import TypedDict


class ResearchState(TypedDict):
    company: str
    url: str
    github_org: str | None
    raw_events: list[dict]
    insights: dict
    report: str
    error: str | None
