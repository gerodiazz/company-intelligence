from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from pipeline import analyze_company
from intelligence import generate_insights
import os
from dotenv import load_dotenv

load_dotenv()


@tool
def analyze_company_tool(company: str) -> dict:
    """
    Analiza una empresa buscando tecnologías en su sitio web,
    ofertas de trabajo y noticias recientes.
    Recibe el nombre de la empresa y devuelve eventos estructurados.
    """
    return analyze_company(company, f"https://www.{company.lower()}.com")


@tool
def generate_insights_tool(company: str) -> dict:
    """
    Analiza una empresa y genera insights accionables: tecnologías detectadas,
    score de innovación (0-100), madurez tecnológica (0-100) y señales clave.
    Usá esta herramienta para evaluar si vale la pena aplicar a una empresa
    o para entender su stack tecnológico en profundidad.
    """
    result = analyze_company(company, f"https://www.{company.lower()}.com")
    return generate_insights(company, result["events"])


llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
tools = [analyze_company_tool, generate_insights_tool]
agent = create_agent(llm, tools)

if __name__ == "__main__":
    result = agent.invoke({
        "messages": [("human", "¿Conviene aplicar a Stripe como AI Engineer?")]
    })
    print(result["messages"][-1].content)
