# ⚽ WorldCup TripMate

**An AI-powered travel architect for first-time international travelers attending the 2026 FIFA World Cup**

Built for the [Google Cloud Rapid Agent Hackathon](https://rapid-agent.devpost.com/) — Arize Partner Track

## The Problem

The 2026 World Cup spans 16 cities across 3 countries (USA, Mexico, Canada). For a first-time international traveler from India, Nigeria, Brazil, or Argentina, planning is overwhelming — different visa rules per country, unfamiliar transit systems, dietary needs in foreign cities, multi-currency budgeting, and complex cross-border logistics.

## The Solution

WorldCup TripMate is an agent that acts like a knowledgeable friend who has lived in every host city. It gives specific restaurant names, exact transit routes, real costs, and culturally-aware advice. And it gets smarter with every conversation.

## Agent Tools

| Tool | What It Does |
|------|-------------|
| Match Finder | Search World Cup matches by team, city, or date |
| Visa Checker | Nationality-specific visa requirements for all 3 host countries |
| Local Guide | City-specific food (vegetarian/halal), transit, and cultural tips |
| Budget Estimator | Itemized cost breakdown across flights, accommodation, food, tickets |
| Itinerary Builder | Complete day-by-day multi-city travel plan following a team |
| Self-Reflection | Agent queries its own performance and adapts in real-time |

## Self-Improvement Loop (Arize Integration)

This is what makes TripMate different:

1. **Every response is traced** via OpenTelemetry to Arize Phoenix Cloud
2. **LLM-as-a-judge** automatically evaluates each response on 5 criteria: relevance, specificity, cultural sensitivity, accuracy, and actionability
3. **The agent queries its own performance** using the check_my_performance tool
4. **It adapts** — if specificity scores are low, it gives more exact names and prices next time

## Tech Stack

- **Google ADK** — Agent Development Kit for building the agent
- **Gemini 2.5 Flash** — LLM via Vertex AI
- **Arize Phoenix Cloud** — Tracing, evaluation, and observability
- **OpenInference** — Auto-instrumentation for Google ADK
- **Streamlit** — Web interface with live performance dashboard
- **Python** — Backend logic

## Setup

1. Clone the repo
2. Create a virtual environment and install dependencies
3. Configure environment variables (see .env.example)
4. Authenticate with Google Cloud
5. Run with streamlit

```bash
git clone https://github.com/hsata/worldcup-trip-agent.git
cd worldcup-trip-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
streamlit run app.py
```

## Environment Variables

See .env.example for required variables:
- GOOGLE_CLOUD_PROJECT — Your Google Cloud project ID
- PHOENIX_API_KEY — From Arize Phoenix Cloud settings
- PHOENIX_COLLECTOR_ENDPOINT — Your Phoenix space URL

## Demo

[Watch the demo video](link-to-video)

## Author

**Harshvardhan Sata** — B.S. Computer Science, UMass Amherst

- GitHub: [@hsata](https://github.com/hsata)
- LinkedIn: [harshvardhan-sata](https://linkedin.com/in/harshvardhan-sata)

## License

MIT
