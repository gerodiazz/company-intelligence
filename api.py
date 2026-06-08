from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from graph.builder import research_graph
from db.client import supabase

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    company: str
    url: str
    github_org: str | None = None


@app.post("/analyze")
def analyze(body: AnalyzeRequest):
    initial_state = {
        "company": body.company,
        "url": body.url,
        "github_org": body.github_org,
        "raw_events": [],
        "insights": {},
        "report": "",
        "error": None,
    }
    result = research_graph.invoke(initial_state)
    if result.get("error"):
        raise HTTPException(status_code=500, detail=result["error"])
    return {
        "company": result["company"],
        "insights": result["insights"],
        "report": result["report"],
    }


@app.get("/reports")
def list_reports():
    response = supabase.table("reports").select("*").order("created_at", desc=True).execute()
    return response.data


@app.get("/reports/{company}")
def get_report(company: str):
    response = (
        supabase.table("reports")
        .select("*")
        .eq("company", company)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail=f"No report found for '{company}'")
    return response.data[0]
