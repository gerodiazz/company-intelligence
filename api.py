
from agent import agent
from fastapi import FastAPI
from pydantic import BaseModel
from intelligence import generate_insights
from pipeline import analyze_company


app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/analyze")
def analyze(company: str, url: str, github_org: str = None):
    result = analyze_company(company, url, github_org)
    insights = generate_insights(company, result["events"])
    return {
        "company": company,
        "events": result["events"],
        "insights": insights
    }

@app.post("/ask")
def ask(body: Question):
    response = agent.invoke({
        "messages": [("human", body.question)]
    })
    return {"answer": response["messages"][-1].content}