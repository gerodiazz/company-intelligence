
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_insights(company, events):
    events_str = json.dumps(events, default=str, indent=2)

    prompt = f"""
    Analizá los siguientes eventos recolectados sobre la empresa {company}:

    {events_str}

    Respondé ÚNICAMENTE con un JSON válido, sin texto adicional, con esta estructura exacta:

    {{
        "technologies": ["lista de tecnologías principales"],
        "signals": ["lista de señales detectadas"],
        "innovation_score": número entre 0-100 basado en presencia de IA, cloud, tecnologías modernas,
        "tech_maturity_score": número entre 0-100 basado en diversidad y solidez del stack tecnológico,
        "insights": ["lista de insights accionables"]
    }}

    Basate SOLO en la evidencia de los eventos. No inventes información.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    raw = response.choices[0].message.content
    return json.loads(raw)


if __name__ == "__main__":
    from pipeline import analyze_company

    result = analyze_company("Stripe", "https://www.stripe.com", github_org="stripe")
    print(generate_insights("Stripe", result["events"]))