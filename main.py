import argparse

from graph.builder import research_graph


def main() -> None:
    parser = argparse.ArgumentParser(description="Company Intelligence — LangGraph pipeline")
    parser.add_argument("company", help="Nombre de la empresa")
    parser.add_argument("url", help="URL del sitio web de la empresa")
    parser.add_argument("--github-org", dest="github_org", default=None,
                        help="Organización GitHub (opcional)")
    args = parser.parse_args()

    initial_state = {
        "company": args.company,
        "url": args.url,
        "github_org": args.github_org,
        "raw_events": [],
        "insights": {},
        "report": "",
        "error": None,
    }

    result = research_graph.invoke(initial_state)
    print(result["report"])


if __name__ == "__main__":
    main()
