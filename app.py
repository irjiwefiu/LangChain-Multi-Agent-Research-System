import html
import streamlit as st
from src.pipelines.pipeline import run_research_pipeline

st.set_page_config(
    page_title="Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

light_mode = not st.session_state.dark_mode
current_theme = "dark" if st.session_state.dark_mode else "light"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {{
        color-scheme: {current_theme};
        --surface: {'#0f172a' if st.session_state.dark_mode else '#ffffff'};
        --surface-2: {'#111827' if st.session_state.dark_mode else '#f7f7f8'};
        --surface-3: {'#1f2937' if st.session_state.dark_mode else '#f3f4f6'};
        --border: {'#334155' if st.session_state.dark_mode else '#e5e7eb'};
        --text: {'#e5e7eb' if st.session_state.dark_mode else '#111827'};
        --text-muted: {'#cbd5e1' if st.session_state.dark_mode else '#4b5563'};
        --accent: {'#7dd3fc' if st.session_state.dark_mode else '#10a37f'};
        --accent-soft: {'#0f172a' if st.session_state.dark_mode else '#ecfdf5'};
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.06);
        --radius-lg: 16px;
        --radius-xl: 24px;
    }}

    /* Force background and default text colors across all Streamlit elements */
    html, body, [class*="st-"], [class*="css"], .stApp {{
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        font-weight: 300;
        color: var(--text) !important;
        background-color: var(--surface) !important;
    }}

    .stApp {{
        background: linear-gradient(180deg, var(--surface) 0%, var(--surface-2) 100%) !important;
    }}

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        padding: 1rem 1.25rem 3rem;
        max-width: 1400px;
    }

    section[data-testid="stSidebar"] {
        background-color: var(--surface-2) !important;
        border-right: 1px solid var(--border);
        padding-top: 0.75rem;
    }

    /* Force chat message text visibility */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        color: var(--text) !important;
    }

    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] span, 
    [data-testid="stChatMessage"] div {
        color: var(--text) !important;
    }

    .sidebar-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1rem;
        box-shadow: var(--shadow-sm);
        margin-bottom: 0.9rem;
    }

    .sidebar-title {
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: var(--text) !important;
    }

    .sidebar-subtitle {
        font-size: 0.85rem;
        color: var(--text-muted) !important;
        line-height: 1.5;
    }

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.2rem 0 1rem;
        margin-bottom: 0.75rem;
    }

    .topbar h1 {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0;
        color: var(--text) !important;
    }

    .topbar .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.45rem 0.7rem;
        border-radius: 999px;
        background: var(--accent-soft);
        color: var(--accent) !important;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .hero-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-xl);
        padding: 1.4rem 1.5rem;
        box-shadow: var(--shadow-sm);
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--text) !important;
        margin: 0 0 0.35rem;
    }

    .hero-text {
        font-size: 0.95rem;
        color: var(--text-muted) !important;
        line-height: 1.6;
        margin: 0;
    }

    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 0.85rem 0 0;
    }

    .chip {
        border: 1px solid var(--border);
        background: var(--surface);
        color: var(--text) !important;
        border-radius: 999px;
        padding: 0.4rem 0.7rem;
        font-size: 0.82rem;
        cursor: pointer;
    }

    .bubble {
        max-width: 100%;
        border-radius: 18px;
        padding: 0.95rem 1rem;
        line-height: 1.6;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
        margin-top: 0.5rem;
    }

    .bubble.user {
        background: var(--accent) !important;
        color: #ffffff !important;
        border-color: var(--accent);
    }

    .bubble.assistant {
        background: var(--surface) !important;
        color: var(--text) !important;
    }

    .bubble.assistant * {
        color: var(--text) !important;
    }

    .bubble h3, .bubble h4 {
        margin: 0.2rem 0 0.45rem;
        font-size: 1rem;
        color: var(--text) !important;
    }

    .bubble p {
        margin: 0.25rem 0;
        color: var(--text) !important;
    }

    .bubble code {
        font-family: 'JetBrains Mono', monospace;
        background: var(--surface-3);
        padding: 0.1rem 0.35rem;
        border-radius: 6px;
        font-size: 0.9em;
        color: var(--text) !important;
    }

    .empty-state {
        background: var(--surface);
        border: 1px dashed var(--border);
        border-radius: var(--radius-xl);
        padding: 1.25rem;
        margin-top: 0.5rem;
    }

    .empty-state h3 {
        margin: 0 0 0.3rem;
        font-size: 1rem;
        color: var(--text) !important;
    }

    .empty-state p {
        margin: 0;
        color: var(--text-muted) !important;
        line-height: 1.6;
    }

    .stButton > button {
        border-radius: 999px;
        border: 1px solid var(--border);
        background: var(--surface) !important;
        color: var(--text) !important;
        padding: 0.55rem 0.85rem;
        transition: all 180ms ease;
    }

    .stButton > button:hover {
        border-color: var(--accent);
        color: var(--accent) !important;
    }

    .stTextInput input, .stTextArea textarea {
        color: var(--text) !important;
        background: var(--surface) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def reset_chat() -> None:
    st.session_state.messages = []
    st.session_state.is_running = False
    st.session_state.pending_prompt = None


def normalize_content(value):
    if isinstance(value, list):
        if value and isinstance(value[0], dict) and "text" in value[0]:
            return "\n".join(str(item.get("text", "")) for item in value if isinstance(item, dict))
        return "\n".join(str(item) for item in value)
    if isinstance(value, dict):
        if "text" in value:
            return str(value["text"])
        return str(value)
    return str(value)


def format_message_content(text: str) -> str:
    return normalize_content(text)


def render_message(message: dict, index: int) -> None:
    role = message["role"]
    content = message.get("content", "")

    with st.chat_message(role):
        if role == "user":
            st.markdown(format_message_content(content))
            return

        data = message.get("data", {})
        available_views = [view for view in ["search", "reader", "writer", "critic"] if data.get(view)]

        if not available_views:
            st.markdown(f"<div class='bubble assistant'>{format_message_content(content)}</div>", unsafe_allow_html=True)
            return

        default_view = "critic" if "critic" in available_views else available_views[0]
        view_key = f"assistant_view_{index}"
        if view_key not in st.session_state:
            st.session_state[view_key] = default_view

        cols = st.columns(len(available_views))
        for col, view in zip(cols, available_views):
            labels = {
                "search": "Search",
                "reader": "Reader",
                "writer": "Writer",
                "critic": "Critic",
            }
            if col.button(labels[view], key=f"{view_key}_{view}", use_container_width=True):
                st.session_state[view_key] = view

        selected_view = st.session_state[view_key]
        selected_content = data.get(selected_view, data[available_views[0]])

        # Wrap view content inside assistant bubble to maintain contrast styling
        formatted = format_message_content(selected_content)
        st.markdown(f"<div class='bubble assistant'>{formatted}</div>", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Research Assistant</div>
            <div class="sidebar-subtitle">A calm, conversation-first workspace for exploring any topic with a multi-agent research workflow.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.session_state.dark_mode = st.toggle("Dark mode", value=st.session_state.dark_mode, key="theme_toggle")
    st.caption("Default is light mode; this setting overrides the device default.")

    if st.button("New chat", use_container_width=True):
        reset_chat()

    st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-title'>Suggested prompts</div>", unsafe_allow_html=True)

    example_prompts = [
        "Future of LLMs in the next five years",
        "Top AI agents to watch in 2026",
        "How generative AI is changing education",
    ]

    for prompt in example_prompts:
        if st.button(prompt, key=f"prompt_{prompt}", use_container_width=True):
            st.session_state.pending_prompt = prompt
            st.session_state.is_running = True

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="topbar">
        <h1>Research workspace</h1>
        <div class="pill">● Live multi-agent research</div>
    </div>
    """,
    unsafe_allow_html=True,
)


if not st.session_state.messages and not st.session_state.is_running:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Ask anything and let the agents research it for you.</div>
            <p class="hero-text">The workflow searches the web, reads the strongest source, drafts a report, and reviews it before presenting the result.</p>
            <div class="chip-row">
                <span class="chip">Search</span>
                <span class="chip">Read</span>
                <span class="chip">Write</span>
                <span class="chip">Critique</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="empty-state">
            <h3>Start with a topic</h3>
            <p>Examples include market trends, product strategy, or a deep-dive into a new technology.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


for index, message in enumerate(st.session_state.messages):
    render_message(message, index)


if st.session_state.is_running and st.session_state.pending_prompt:
    if not any(message["role"] == "user" and message["content"] == st.session_state.pending_prompt for message in st.session_state.messages):
        st.session_state.messages.append({"role": "user", "content": st.session_state.pending_prompt})

    with st.spinner("The agents are researching your topic..."):
        try:
            state = run_research_pipeline(st.session_state.pending_prompt)
            report = state.get("report", "")
            feedback = state.get("feedback", "")

            assistant_data = {
                "search": state.get("search_results", ""),
                "reader": state.get("scraped_content", ""),
                "writer": state.get("report", ""),
                "critic": state.get("feedback", ""),
            }
            assistant_content = f"### Research complete\n\n**Topic:** {st.session_state.pending_prompt}"
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_content,
                    "data": assistant_data,
                }
            )
        except Exception as exc:  # pragma: no cover - UI fallback
            st.session_state.messages.append(
                {"role": "assistant", "content": f"The research workflow hit an issue. Please check your API configuration.\n\nError: {exc}"}
            )

        st.session_state.is_running = False
        st.session_state.pending_prompt = None
        st.rerun()


if st.session_state.pending_prompt and not st.session_state.is_running:
    st.session_state.is_running = True
    st.rerun()


prompt = st.chat_input("Ask the assistant to research a topic...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.pending_prompt = prompt
    st.session_state.is_running = True
    st.rerun()
