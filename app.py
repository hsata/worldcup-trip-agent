import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT", "")
os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

from worldcup_agent.tracing_setup import setup_tracing
from worldcup_agent.agent import worldcup_agent
from worldcup_agent.evaluator import evaluate_response, get_evaluation_summary
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

st.set_page_config(
    page_title="WorldCup TripMate",
    page_icon="⚽",
    layout="wide",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .block-container { padding-top: 2rem; max-width: 1200px; }

    .hero {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .hero h1 { font-size: 2.2rem; margin: 0 0 0.3rem; font-weight: 700; }
    .hero p { font-size: 1rem; opacity: 0.85; margin: 0; }
    .hero .badges {
        margin-top: 1rem;
        display: flex;
        gap: 0.5rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    .hero .badge {
        background: rgba(255,255,255,0.15);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
    }

    .eval-panel {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
    }
    .eval-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #1e293b;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid #f1f5f9;
    }
    .metric-name { font-size: 0.85rem; color: #64748b; }
    .metric-bar {
        width: 100px;
        height: 8px;
        background: #e2e8f0;
        border-radius: 4px;
        overflow: hidden;
        display: inline-block;
        vertical-align: middle;
        margin-right: 8px;
    }
    .metric-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    .fill-5 { width: 100%; background: #22c55e; }
    .fill-4 { width: 80%; background: #84cc16; }
    .fill-3 { width: 60%; background: #eab308; }
    .fill-2 { width: 40%; background: #f97316; }
    .fill-1 { width: 20%; background: #ef4444; }

    .overall-score {
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    .overall-number {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1;
    }
    .score-green { color: #22c55e; }
    .score-yellow { color: #eab308; }
    .score-red { color: #ef4444; }

    .insight-box {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-radius: 8px;
        padding: 0.75rem;
        margin-top: 0.75rem;
        font-size: 0.85rem;
    }

    .tools-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        margin-top: 0.5rem;
    }
    .tool-chip {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 0.75rem;
        text-align: center;
    }

    .stChatMessage { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def init_agent():
    setup_tracing()
    return Runner(
        agent=worldcup_agent,
        app_name="worldcup_tripmate",
        session_service=InMemorySessionService(),
    )


runner = init_agent()


async def get_or_create_session():
    if "session_id" not in st.session_state:
        session = await runner.session_service.create_session(
            app_name="worldcup_tripmate",
            user_id="streamlit_user",
        )
        st.session_state.session_id = session.id
    return st.session_state.session_id


async def run_agent(user_input: str) -> str:
    session_id = await get_or_create_session()
    content = Content(parts=[Part(text=user_input)], role="user")
    response_text = ""
    async for event in runner.run_async(
        user_id="streamlit_user",
        session_id=session_id,
        new_message=content,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text
    return response_text


if "messages" not in st.session_state:
    st.session_state.messages = []
if "evaluations" not in st.session_state:
    st.session_state.evaluations = []

col_chat, col_eval = st.columns([3, 1])

with col_chat:
    st.markdown("""
    <div class="hero">
        <h1>⚽ WorldCup TripMate</h1>
        <p>Your AI travel architect for the 2026 FIFA World Cup</p>
        <div class="badges">
            <span class="badge">🤖 Google ADK + Gemini</span>
            <span class="badge">📊 Arize Phoenix</span>
            <span class="badge">🔄 Self-Improving Agent</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    quick_cols = st.columns(3)
    prompts = [
        ("🇮🇳 Plan my Argentina trip", "I'm from India, vegetarian, budget $3000. Plan my trip to watch Argentina at the World Cup!"),
        ("🛂 Visa check from Nigeria", "I'm from Nigeria, what visas do I need for all three World Cup countries?"),
        ("📅 10-day Brazil itinerary", "Build me a 10-day budget itinerary following Brazil. I'm from the UK."),
    ]
    for i, (label, prompt) in enumerate(prompts):
        if quick_cols[i].button(label, use_container_width=True, key=f"q_{i}"):
            st.session_state.quick_input = prompt

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "⚽"):
            st.markdown(msg["content"])

    default_input = st.session_state.pop("quick_input", None)
    user_input = st.chat_input("Where are you from? What team do you support?")

    if default_input and not user_input:
        user_input = default_input

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="⚽"):
            with st.spinner("Planning your World Cup adventure..."):
                response = asyncio.run(run_agent(user_input))
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

        eval_result = asyncio.run(evaluate_response(user_input, response))
        if eval_result.get("scores"):
            st.session_state.evaluations.append(eval_result)

        st.rerun()

with col_eval:
    if st.session_state.evaluations:
        latest = st.session_state.evaluations[-1]
        scores = latest.get("scores", {})
        overall = scores.get("overall", 0)

        color_class = "score-green" if overall >= 4 else "score-yellow" if overall >= 3 else "score-red"
        st.markdown(f"""
        <div class="eval-panel">
            <div class="eval-title">📊 Agent Performance</div>
            <div class="overall-score">
                <div class="overall-number {color_class}">{overall}/5</div>
                <div style="font-size:0.8rem;color:#64748b;margin-top:4px;">Overall Score</div>
            </div>
        """, unsafe_allow_html=True)

        metrics = ["relevance", "specificity", "cultural_sensitivity", "accuracy", "actionability"]
        for m in metrics:
            val = scores.get(m, 0)
            label = m.replace("_", " ").title()
            st.markdown(f"""
            <div class="metric-row">
                <span class="metric-name">{label}</span>
                <span>
                    <span class="metric-bar"><span class="metric-fill fill-{val}"></span></span>
                    {val}/5
                </span>
            </div>
            """, unsafe_allow_html=True)

        suggestion = latest.get("suggestion", "")
        weakness = latest.get("weakest_area", "N/A")
        st.markdown(f"""
            <div class="insight-box">
                <strong>🎯 Focus area:</strong> {weakness}<br/>
                <span style="color:#92400e;">{suggestion[:150]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        summary = get_evaluation_summary()
        st.markdown(f"""
        <div class="eval-panel" style="margin-top:0.75rem;">
            <div class="eval-title">📈 Session Stats</div>
            <div class="metric-row">
                <span class="metric-name">Responses</span>
                <span><strong>{summary.get('total_evaluations', 0)}</strong></span>
            </div>
            <div class="metric-row">
                <span class="metric-name">Avg Score</span>
                <span><strong>{summary.get('average_overall_score', 0)}/5</strong></span>
            </div>
            <div class="metric-row">
                <span class="metric-name">Top Weakness</span>
                <span><strong>{summary.get('most_common_weakness', 'N/A')}</strong></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("""
        <div class="eval-panel" style="margin-top:0.75rem;">
            <div class="eval-title">🔗 Observability</div>
            <a href="https://app.phoenix.arize.com/s/haree-sata/projects" target="_blank" style="font-size:0.85rem;">
                View traces in Phoenix →
            </a>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="eval-panel">
            <div class="eval-title">📊 Agent Performance</div>
            <p style="color:#64748b;font-size:0.85rem;">Ask a question to see live evaluation scores powered by Arize Phoenix</p>
            <div class="tools-grid">
                <div class="tool-chip">🔍 Match Finder</div>
                <div class="tool-chip">🛂 Visa Checker</div>
                <div class="tool-chip">🍽 Local Guide</div>
                <div class="tool-chip">💰 Budget Estimator</div>
                <div class="tool-chip">📅 Itinerary Builder</div>
                <div class="tool-chip">🔄 Self-Reflection</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
