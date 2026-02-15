from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
import os
import json
from dotenv import load_dotenv
from datetime import date

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.environ["GROQ_API_KEY"].strip()


def extract_json(text: str) -> dict:
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end <= start:
            raise ValueError("No JSON object found")
        return json.loads(text[start:end])
    except Exception as e:
        raise RuntimeError(
            f"Assistant did not return valid JSON.\n\nRAW OUTPUT:\n{text}"
        ) from e


def run_agent_with_fallback(prompt: str):
    """
    Run agent with tools.
    If a tool hard-fails (DuckDuckGo), retry WITHOUT tools.
    """
    try:
        return web_search_agent.run(prompt)
    except Exception as e:
        print("\n⚠️ Tool failed. Retrying WITHOUT tools...\n")

        fallback_agent = Agent(
            name="Fallback Agent",
            role="Summarize AI news from general knowledge",
            model=Groq(id="llama-3.3-70b-versatile"),
            tools=[],  # 🔑 no tools
            instructions=[
                "Answer from general knowledge only",
                "Return a single valid JSON object",
                "Use this schema:",
                "{",
                "  \"query\": string,",
                "  \"date\": string (YYYY-MM-DD),",
                "  \"results\": []",
                "}"
            ],
        )
        return fallback_agent.run(prompt)


# ---- Web Search Agent (NO NEWS TOOL) ----
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the latest AI news",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        DuckDuckGo(fixed_max_results=3),  # 🔑 SEARCH only, not news
        YFinanceTools()
    ],
    instructions=[
        "Search the web for the most recent AI-related news",
        "Use search tools only (do NOT use news tools)",
        "Summarize results clearly",

        "FINAL ANSWER REQUIREMENTS:",
        "Return a single valid JSON object ONLY",
        "Do not include markdown or explanations",
        "Use this exact schema:",
        "{",
        "  \"query\": string,",
        "  \"date\": string (YYYY-MM-DD),",
        "  \"results\": [",
        "    {",
        "      \"title\": string,",
        "      \"summary\": string,",
        "      \"source\": string,",
        "      \"url\": string",
        "    }",
        "  ]",
        "}"
    ],
    show_tool_calls=False,
)

if __name__ == "__main__":
    response = run_agent_with_fallback(
        "What are the latest AI news today?"
    )

    assistant_text = None
    for msg in response.messages:
        if msg.role == "assistant" and msg.content:
            assistant_text = msg.content
            break

    if not assistant_text:
        raise RuntimeError("No assistant output received")

    if not assistant_text.strip().startswith("{"):
        raise RuntimeError(f"Non-JSON response:\n{assistant_text}")

    parsed = extract_json(assistant_text)
    print(json.dumps(parsed, indent=2))
