import os
import uuid
import requests
import streamlit as st

st.set_page_config(
    page_title="Mapranex | AI Tools",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      :root {
        --bg: #212121;
        --panel: #2f2f2f;
        --panel-2: #262626;
        --panel-3: #303030;
        --text: #ececec;
        --muted: #a6a6a6;
        --line: #3f3f3f;
        --accent: #00d4ff;
        --accent-2: #0aa8d2;
      }

      html, body, [class*="css"] {
        font-family: Arial, Helvetica, sans-serif;
      }

      html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: var(--bg) !important;
        color: var(--text) !important;
      }

      [data-testid="stHeader"] {
        background: rgba(33,33,33,.94) !important;
        border-bottom: 1px solid #2b2b2b;
        backdrop-filter: blur(12px);
      }

      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}

      .block-container {
        max-width: 980px;
        padding-top: 1.35rem;
        padding-bottom: 5rem;
      }

      .mx-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        margin: 2px 0 22px;
      }

      .mx-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #f4f4f4;
        font-weight: 800;
        font-size: 18px;
        letter-spacing: -.35px;
      }

      .mx-brand-dot {
        width: 24px;
        height: 24px;
        border-radius: 8px;
        display: grid;
        place-items: center;
        background: linear-gradient(135deg, #00d4ff, #7c5cff);
        color: #081e35;
        font-size: 12px;
      }

      .mx-status {
        color: #9e9e9e;
        font-size: 12px;
      }

      .mx-hero {
        max-width: 760px;
        margin: 72px auto 38px;
        text-align: center;
      }

      .mx-kicker {
        color: var(--accent);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        margin-bottom: 14px;
      }

      .mx-title {
        margin: 0;
        color: #f4f4f4;
        font-size: clamp(34px, 4.6vw, 52px);
        line-height: 1.08;
        letter-spacing: -2.3px;
        font-weight: 800;
      }

      .mx-title span {
        color: var(--accent);
      }

      .mx-subtitle {
        max-width: 650px;
        margin: 14px auto 0;
        color: #a9a9a9;
        font-size: 15px;
        line-height: 1.65;
      }

      .stLinkButton {
        display: flex;
        justify-content: center;
        margin-bottom: 22px;
      }

      .stLinkButton > a {
        border-radius: 999px !important;
        border: 1px solid var(--line) !important;
        background: #2b2b2b !important;
        color: #dcdcdc !important;
        min-height: 38px !important;
        padding: 0 15px !important;
        font-weight: 700 !important;
      }

      div[data-baseweb="tab-list"] {
        gap: 6px;
        padding: 5px;
        margin: 0 auto 24px;
        overflow-x: auto;
        border: 1px solid #3a3a3a;
        border-radius: 13px;
        background: #292929;
      }

      button[data-baseweb="tab"] {
        height: 38px;
        white-space: nowrap;
        border-radius: 9px;
        padding: 0 13px;
        color: #aaa !important;
        font-size: 12px;
        font-weight: 700;
      }

      button[data-baseweb="tab"] p {
        color: inherit !important;
      }

      button[data-baseweb="tab"][aria-selected="true"] {
        color: #f2f2f2 !important;
        background: #3a3a3a !important;
      }

      .mx-tool-card {
        max-width: 820px;
        margin: 26px auto 16px;
        padding: 0 4px;
        background: transparent;
      }

      .mx-tool-head {
        display: flex;
        align-items: flex-start;
        gap: 14px;
      }

      .mx-tool-icon {
        width: 38px;
        height: 38px;
        flex: 0 0 38px;
        display: grid;
        place-items: center;
        border-radius: 11px;
        background: #343434;
        border: 1px solid #444;
        color: var(--accent);
        font-size: 17px;
        font-weight: 800;
      }

      .mx-tool-card h3 {
        margin: 1px 0 5px;
        color: #f2f2f2;
        font-size: 22px;
        letter-spacing: -.6px;
      }

      .mx-tool-card p {
        margin: 0;
        color: #9f9f9f;
        font-size: 13px;
        line-height: 1.55;
      }

      [data-testid="stTextArea"] {
        max-width: 820px;
        margin: 0 auto;
      }

      [data-testid="stTextArea"] textarea {
        min-height: 210px !important;
        border-radius: 22px !important;
        border: 1px solid #444 !important;
        background: #2f2f2f !important;
        color: #f1f1f1 !important;
        padding: 18px 18px 48px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,.14) !important;
        caret-color: #fff;
      }

      [data-testid="stTextArea"] textarea::placeholder {
        color: #888 !important;
      }

      [data-testid="stTextArea"] textarea:focus {
        border-color: #565656 !important;
        box-shadow: 0 0 0 1px #565656, 0 12px 30px rgba(0,0,0,.18) !important;
      }

      div[data-testid="stHorizontalBlock"] {
        max-width: 820px;
        margin-left: auto;
        margin-right: auto;
      }

      .stButton > button {
        min-height: 40px;
        border-radius: 999px !important;
        border: 1px solid #4a4a4a !important;
        font-weight: 800 !important;
        transition: transform .16s ease, background .16s ease;
      }

      .stButton > button[kind="primary"] {
        color: #081e35 !important;
        background: var(--accent) !important;
        border-color: var(--accent) !important;
      }

      .stButton > button:hover {
        transform: translateY(-1px);
      }

      [data-testid="stAlert"] {
        max-width: 820px;
        margin-left: auto;
        margin-right: auto;
        border-radius: 14px;
        border: 1px solid #444 !important;
        background: #2b2b2b !important;
        color: #e8e8e8 !important;
      }

      [data-testid="stExpander"] {
        border: 1px solid #444 !important;
        border-radius: 14px !important;
        overflow: hidden;
        background: #2b2b2b !important;
      }

      [data-testid="stExpander"] summary,
      [data-testid="stExpander"] p,
      [data-testid="stExpander"] span {
        color: #e8e8e8 !important;
      }

      .mx-result-title {
        max-width: 820px;
        margin: 30px auto 10px;
        color: #f0f0f0;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -.5px;
      }

      [data-testid="stMarkdownContainer"] {
        color: #e8e8e8;
      }

      [data-testid="stMarkdownContainer"] p,
      [data-testid="stMarkdownContainer"] li {
        color: #d0d0d0;
      }

      .mx-about-grid {
        display: grid;
        grid-template-columns: repeat(2,minmax(0,1fr));
        gap: 14px;
        max-width: 820px;
        margin: 34px auto 0;
      }

      .mx-about-card {
        padding: 18px;
        border: 1px solid #3f3f3f;
        border-radius: 16px;
        background: #292929;
      }

      .mx-about-card strong {
        display: block;
        color: #f1f1f1;
        margin-bottom: 7px;
      }

      .mx-about-card span {
        color: #a5a5a5;
        font-size: 13px;
        line-height: 1.55;
      }

      @media (max-width: 760px) {
        .block-container { padding: 1rem 1rem 4rem; }
        .mx-hero { margin-top: 42px; }
        .mx-title { font-size: 36px; }
        .mx-about-grid { grid-template-columns: 1fr; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="mx-topbar">
      <div class="mx-brand">
        <span class="mx-brand-dot">✦</span>
        <span>Mapranex AI</span>
      </div>
      <div class="mx-status">Secure AI workspace</div>
    </div>

    <section class="mx-hero">
      <div class="mx-kicker">AI Tools</div>
      <div class="mx-title">What can I help you <span>build or test?</span></div>
      <p class="mx-subtitle">
        Use focused AI tools for requirements, test design, API quality, document analysis,
        and QA engineering — all connected to your secure n8n + OmniRoute stack.
      </p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.link_button("← Main website", "https://myaiteam-company.vercel.app/")


def get_secret(name):
    try:
        return st.secrets.get(name, os.getenv(name, ""))
    except Exception:
        return os.getenv(name, "")


def call_suite(tool, text):
    url = get_secret("N8N_AI_SUITE_WEBHOOK_URL") or "https://n8n.myaiteam.work.gd/webhook/myaiteam-ai-suite"
    secret = get_secret("N8N_SHARED_SECRET")
    if not secret:
        st.error("N8N_SHARED_SECRET is not configured.")
        return None

    payload = {
        "tool": tool,
        "input": text.strip(),
        "source": "myaiteam-streamlit",
        "request_id": str(uuid.uuid4()),
    }
    headers = {
        "Content-Type": "application/json",
        "X-Mapranex-Token": secret,
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code in (401, 403):
            st.error("Authentication failed between Streamlit and n8n.")
        else:
            st.error("The AI tool returned an error. Check the n8n execution log.")
    except requests.RequestException:
        st.error("The AI tool could not be reached.")
    return None


def render_list(title, values):
    st.markdown(f'<div class="mx-result-title">{title}</div>', unsafe_allow_html=True)
    if not values:
        st.caption("No items returned.")
        return

    for item in values:
        if isinstance(item, dict):
            st.json(item)
        else:
            st.markdown(f"- {item}")


def render_result(tool, result):
    if tool == "requirements_analyzer":
        st.markdown('<div class="mx-result-title">Summary</div>', unsafe_allow_html=True)
        st.write(result.get("summary", ""))
        render_list("Functional Requirements", result.get("functional_requirements"))
        render_list("Non-Functional Requirements", result.get("non_functional_requirements"))
        render_list("Ambiguities", result.get("ambiguities"))
        render_list("Risks", result.get("risks"))
        render_list("Acceptance Criteria", result.get("acceptance_criteria"))
        render_list("Test Scenarios", result.get("test_scenarios"))
        render_list("Questions for Stakeholder", result.get("questions_for_stakeholder"))

    elif tool == "test_case_generator":
        st.markdown('<div class="mx-result-title">Summary</div>', unsafe_allow_html=True)
        st.write(result.get("summary", ""))
        st.markdown('<div class="mx-result-title">Test Cases</div>', unsafe_allow_html=True)

        for test_case in result.get("test_cases", []):
            with st.expander(f"{test_case.get('id', 'TC')} — {test_case.get('title', 'Test Case')}"):
                st.write(f"**Priority:** {test_case.get('priority', '')}")
                st.write(f"**Preconditions:** {test_case.get('preconditions', '')}")
                st.write("**Steps:**")
                steps = test_case.get("steps", [])
                if isinstance(steps, list):
                    for index, step in enumerate(steps, 1):
                        st.write(f"{index}. {step}")
                else:
                    st.write(steps)
                st.write(f"**Expected result:** {test_case.get('expected_result', '')}")

        render_list("Edge Cases", result.get("edge_cases"))
        render_list("Negative Cases", result.get("negative_cases"))
        render_list("Assumptions", result.get("assumptions"))

    elif tool == "api_test_generator":
        st.markdown('<div class="mx-result-title">Summary</div>', unsafe_allow_html=True)
        st.write(result.get("summary", ""))
        render_list("Positive Tests", result.get("positive_tests"))
        render_list("Negative Tests", result.get("negative_tests"))
        render_list("Validation Tests", result.get("validation_tests"))
        render_list("Security Tests", result.get("security_tests"))
        render_list("Example Requests", result.get("example_requests"))
        render_list("Assumptions", result.get("assumptions"))

    elif tool == "document_summarizer":
        st.markdown('<div class="mx-result-title">Summary</div>', unsafe_allow_html=True)
        st.write(result.get("summary", ""))
        render_list("Key Points", result.get("key_points"))
        render_list("Decisions", result.get("decisions"))
        render_list("Action Items", result.get("action_items"))
        render_list("Risks / Open Questions", result.get("risks_or_open_questions"))

    elif tool == "qa_assistant":
        st.markdown('<div class="mx-result-title">Answer</div>', unsafe_allow_html=True)
        st.write(result.get("answer", ""))
        render_list("Recommended Actions", result.get("recommended_actions"))
        render_list("Risks", result.get("risks"))
        render_list("Checks", result.get("checks"))
        render_list("Assumptions", result.get("assumptions"))


TOOL_META = {
    "requirements_analyzer": ("◇", "Requirements Analyzer"),
    "test_case_generator": ("✓", "Test Case Generator"),
    "api_test_generator": ("↗", "API Test Generator"),
    "document_summarizer": ("≡", "Document Summarizer"),
    "qa_assistant": ("✦", "QA Assistant"),
}


def tool_tab(tool, description, placeholder, button):
    icon, title = TOOL_META[tool]

    st.markdown(
        f"""
        <div class="mx-tool-card">
          <div class="mx-tool-head">
            <div class="mx-tool-icon">{icon}</div>
            <div>
              <h3>{title}</h3>
              <p>{description}</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    text = st.text_area(
        "Input",
        placeholder=placeholder,
        height=220,
        key=f"{tool}_input",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        submit = st.button(button, type="primary", key=f"{tool}_button", use_container_width=True)

    if submit:
        if len(text.strip()) < 20:
            st.warning("Enter at least 20 characters.")
        else:
            with st.spinner("Processing with Mapranex AI..."):
                data = call_suite(tool, text)

            if data and data.get("status") == "success":
                st.success("Completed.")
                render_result(tool, data.get("result") or {})
                with st.expander("Technical response details"):
                    st.caption(f"Request ID: {data.get('request_id', '')}")
                    st.json(data)


tabs = st.tabs(
    [
        "Requirements",
        "Test Cases",
        "API Tests",
        "Summarizer",
        "QA Assistant",
        "About",
    ]
)

with tabs[0]:
    tool_tab(
        "requirements_analyzer",
        "Turn raw requirements into structured functional coverage, risks, acceptance criteria, and test scenarios.",
        "Paste a requirement, user story, feature description, or business need...",
        "Analyze",
    )

with tabs[1]:
    tool_tab(
        "test_case_generator",
        "Generate structured functional, negative, and edge test cases from a feature or requirement.",
        "Paste the requirement or feature you want test cases for...",
        "Generate",
    )

with tabs[2]:
    tool_tab(
        "api_test_generator",
        "Generate positive, negative, validation, security, and example API tests from an endpoint description.",
        "Paste an API endpoint description, request/response contract, or OpenAPI excerpt...",
        "Generate",
    )

with tabs[3]:
    tool_tab(
        "document_summarizer",
        "Condense technical or business text into decisions, key points, actions, and open questions.",
        "Paste document text, meeting notes, technical notes, or business content...",
        "Summarize",
    )

with tabs[4]:
    tool_tab(
        "qa_assistant",
        "Get practical help with QA strategy, defects, automation, testing decisions, and quality engineering problems.",
        "Describe your QA question, defect, automation problem, or testing context...",
        "Ask",
    )

with tabs[5]:
    st.markdown(
        """
        <div class="mx-about-grid">
          <div class="mx-about-card">
            <strong>Architecture</strong>
            <span>Streamlit provides the AI workspace, n8n handles secure orchestration, and OmniRoute provides model access on the Oracle Cloud stack.</span>
          </div>
          <div class="mx-about-card">
            <strong>Security</strong>
            <span>Webhook URLs and authentication secrets remain server-side and are never displayed in the user interface.</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
