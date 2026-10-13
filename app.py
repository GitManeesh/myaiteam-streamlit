import os
import uuid

import requests
import streamlit as st

st.set_page_config(
    page_title="Mapranex AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      :root {
        --bg: #212121;
        --sidebar: #171717;
        --panel: #2f2f2f;
        --panel-2: #282828;
        --line: #3d3d3d;
        --text: #ececec;
        --muted: #9b9b9b;
        --accent: #00d4ff;
      }

      html, body, [class*="css"] {
        font-family: Arial, Helvetica, sans-serif;
      }

      html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: var(--bg) !important;
        color: var(--text) !important;
      }

      /* Hide Streamlit chrome for end users */
      #MainMenu,
      footer,
      [data-testid="stToolbar"],
      [data-testid="stDecoration"],
      [data-testid="stStatusWidget"],
      [data-testid="stHeaderActionElements"],
      [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
        visibility: hidden !important;
      }

      [data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
      }

      /* Permanent left sidebar */
      [data-testid="stSidebar"] {
        background: var(--sidebar) !important;
        border-right: 1px solid #2b2b2b;
        width: 268px !important;
        min-width: 268px !important;
      }

      [data-testid="stSidebar"] > div:first-child {
        padding-top: 18px;
      }

      .mx-sidebar-brand {
        padding: 4px 8px 18px;
      }

      .mx-sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #f3f3f3;
        font-size: 17px;
        font-weight: 800;
        letter-spacing: -.35px;
      }

      .mx-sidebar-mark {
        width: 30px;
        height: 30px;
        border-radius: 9px;
        display: grid;
        place-items: center;
        color: #071c32;
        background: linear-gradient(135deg, #00d4ff, #7c5cff);
        box-shadow: 0 5px 18px rgba(0,212,255,.14);
      }

      .mx-sidebar-copy {
        margin-top: 7px;
        color: #747474;
        font-size: 11px;
        line-height: 1.45;
      }

      .mx-sidebar-label {
        margin: 13px 10px 7px;
        color: #606060;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
      }

      [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        display: none;
      }

      [data-testid="stSidebar"] [role="radiogroup"] {
        gap: 4px;
      }

      [data-testid="stSidebar"] [role="radiogroup"] label {
        min-height: 42px;
        padding: 0 11px !important;
        border-radius: 9px;
        background: transparent;
        color: #bdbdbd !important;
        transition: background .14s ease, color .14s ease;
      }

      [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: #242424;
        color: #fff !important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background: #2b2b2b;
        color: #fff !important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] label p {
        color: inherit !important;
        font-size: 13px;
        font-weight: 650;
      }

      [data-testid="stSidebar"] .stLinkButton {
        margin: 14px 8px 0;
      }

      [data-testid="stSidebar"] .stLinkButton > a {
        width: 100%;
        justify-content: flex-start;
        min-height: 40px;
        padding: 0 12px;
        border-radius: 9px !important;
        border: 1px solid #313131 !important;
        background: #202020 !important;
        color: #c9c9c9 !important;
        font-size: 12px;
        font-weight: 700;
      }

      .mx-sidebar-footer {
        margin: 24px 8px 0;
        padding-top: 15px;
        border-top: 1px solid #292929;
        color: #666;
        font-size: 10px;
        line-height: 1.55;
      }

      .mx-live-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        margin-right: 6px;
        border-radius: 50%;
        background: #28c840;
        box-shadow: 0 0 8px rgba(40,200,64,.42);
      }

      /* Main canvas */
      .block-container {
        max-width: 920px;
        padding-top: 3.2rem;
        padding-bottom: 9rem;
      }

      .mx-page-head {
        max-width: 760px;
        margin: 0 auto 24px;
      }

      .mx-eyebrow {
        color: var(--accent);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.05px;
        text-transform: uppercase;
        margin-bottom: 10px;
      }

      .mx-page-title {
        color: #f4f4f4;
        font-size: clamp(31px, 4vw, 43px);
        line-height: 1.08;
        letter-spacing: -1.9px;
        font-weight: 800;
        margin: 0;
      }

      .mx-page-subtitle {
        margin: 11px 0 0;
        color: #969696;
        font-size: 14px;
        line-height: 1.65;
        max-width: 680px;
      }

      .mx-empty {
        max-width: 760px;
        margin: 54px auto 0;
        padding: 24px 0;
        color: #717171;
        text-align: center;
        font-size: 13px;
      }

      .mx-result-title {
        max-width: 760px;
        margin: 30px auto 10px;
        color: #f1f1f1;
        font-size: 19px;
        font-weight: 800;
        letter-spacing: -.45px;
      }

      [data-testid="stMarkdownContainer"] p,
      [data-testid="stMarkdownContainer"] li {
        color: #d0d0d0;
      }

      [data-testid="stAlert"] {
        max-width: 760px;
        margin-left: auto;
        margin-right: auto;
        border-radius: 14px;
        border: 1px solid #414141 !important;
        background: #292929 !important;
        color: #e7e7e7 !important;
      }

      [data-testid="stExpander"] {
        max-width: 760px;
        margin-left: auto;
        margin-right: auto;
        border: 1px solid #414141 !important;
        border-radius: 14px !important;
        overflow: hidden;
        background: #292929 !important;
      }

      [data-testid="stExpander"] summary,
      [data-testid="stExpander"] p,
      [data-testid="stExpander"] span {
        color: #e7e7e7 !important;
      }

      /* ChatGPT-like bottom composer */
      [data-testid="stBottom"] {
        background: linear-gradient(180deg, rgba(33,33,33,0), #212121 28%, #212121 100%) !important;
        padding-top: 22px !important;
      }

      [data-testid="stBottom"] > div {
        max-width: 760px;
        margin: 0 auto;
      }

      [data-testid="stChatInput"] {
        border: 1px solid #444 !important;
        border-radius: 24px !important;
        background: #2f2f2f !important;
        box-shadow: 0 12px 35px rgba(0,0,0,.22) !important;
      }

      [data-testid="stChatInput"] textarea {
        color: #f0f0f0 !important;
        background: transparent !important;
        min-height: 54px !important;
        max-height: 180px !important;
        padding: 16px 52px 16px 18px !important;
      }

      [data-testid="stChatInput"] textarea::placeholder {
        color: #7e7e7e !important;
      }

      [data-testid="stChatInput"] button {
        color: #071c32 !important;
        background: var(--accent) !important;
        border-radius: 50% !important;
      }

      .mx-about-grid {
        display: grid;
        grid-template-columns: repeat(2,minmax(0,1fr));
        gap: 14px;
        max-width: 760px;
        margin: 12px auto 0;
      }

      .mx-about-card {
        padding: 19px;
        border: 1px solid #3f3f3f;
        border-radius: 16px;
        background: #292929;
      }

      .mx-about-card strong {
        display: block;
        color: #f2f2f2;
        margin-bottom: 7px;
      }

      .mx-about-card span {
        color: #999;
        font-size: 13px;
        line-height: 1.55;
      }

      @media (max-width: 760px) {
        [data-testid="stSidebar"] {
          display: none;
        }

        .block-container {
          padding: 1.5rem 1rem 8rem;
        }

        .mx-about-grid {
          grid-template-columns: 1fr;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


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


TOOLS = {
    "◇  Requirements": {
        "tool": "requirements_analyzer",
        "eyebrow": "Requirements",
        "title": "Requirements Analyzer",
        "description": "Turn raw requirements into structured functional coverage, risks, acceptance criteria, and test scenarios.",
        "placeholder": "Paste a requirement, user story, feature description, or business need...",
    },
    "✓  Test Cases": {
        "tool": "test_case_generator",
        "eyebrow": "Test design",
        "title": "Test Case Generator",
        "description": "Generate structured functional, negative, and edge test cases from a feature or requirement.",
        "placeholder": "Paste the requirement or feature you want test cases for...",
    },
    "↗  API Tests": {
        "tool": "api_test_generator",
        "eyebrow": "API quality",
        "title": "API Test Generator",
        "description": "Generate positive, negative, validation, security, and example API tests from an endpoint description.",
        "placeholder": "Paste an API endpoint description, request/response contract, or OpenAPI excerpt...",
    },
    "≡  Summarizer": {
        "tool": "document_summarizer",
        "eyebrow": "Knowledge",
        "title": "Document Summarizer",
        "description": "Condense technical or business text into decisions, key points, actions, and open questions.",
        "placeholder": "Paste document text, meeting notes, technical notes, or business content...",
    },
    "✦  QA Assistant": {
        "tool": "qa_assistant",
        "eyebrow": "Quality engineering",
        "title": "QA Assistant",
        "description": "Get practical help with QA strategy, defects, automation, testing decisions, and quality engineering problems.",
        "placeholder": "Describe your QA question, defect, automation problem, or testing context...",
    },
}


with st.sidebar:
    st.markdown(
        """
        <div class="mx-sidebar-brand">
          <div class="mx-sidebar-logo">
            <span class="mx-sidebar-mark">✦</span>
            <span>Mapranex AI</span>
          </div>
          <div class="mx-sidebar-copy">Secure quality engineering workspace</div>
        </div>
        <div class="mx-sidebar-label">Tools</div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        list(TOOLS.keys()) + ["ⓘ  About"],
        label_visibility="collapsed",
    )

    st.link_button("↗  Main website", "https://myaiteam-company.vercel.app/")

    st.markdown(
        """
        <div class="mx-sidebar-footer">
          <div><span class="mx-live-dot"></span>Services connected</div>
          <div style="margin-top:6px;">n8n · OmniRoute · Oracle Cloud</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if page == "ⓘ  About":
    st.markdown(
        """
        <div class="mx-page-head">
          <div class="mx-eyebrow">About</div>
          <div class="mx-page-title">Built for focused AI-assisted quality work.</div>
          <p class="mx-page-subtitle">
            Mapranex AI Tools keeps the interface simple while n8n and OmniRoute handle secure orchestration behind the scenes.
          </p>
        </div>
        <div class="mx-about-grid">
          <div class="mx-about-card">
            <strong>Architecture</strong>
            <span>Streamlit provides the workspace, n8n handles orchestration, and OmniRoute provides model access on the Oracle Cloud stack.</span>
          </div>
          <div class="mx-about-card">
            <strong>Security</strong>
            <span>Webhook URLs and authentication secrets stay server-side and are never exposed in the end-user interface.</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    config = TOOLS[page]
    result_key = f'{config["tool"]}_result'

    st.markdown(
        f"""
        <div class="mx-page-head">
          <div class="mx-eyebrow">{config["eyebrow"]}</div>
          <div class="mx-page-title">{config["title"]}</div>
          <p class="mx-page-subtitle">{config["description"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if result_key in st.session_state:
        data = st.session_state[result_key]

        if data and data.get("status") == "success":
            render_result(config["tool"], data.get("result") or {})

            with st.expander("Technical response details"):
                st.caption(f'Request ID: {data.get("request_id", "")}')
                st.json(data)
    else:
        st.markdown(
            '<div class="mx-empty">Your analysis will appear here. Enter a request below to begin.</div>',
            unsafe_allow_html=True,
        )

    prompt = st.chat_input(config["placeholder"])

    if prompt:
        if len(prompt.strip()) < 20:
            st.warning("Enter at least 20 characters.")
        else:
            with st.spinner("Processing with Mapranex AI..."):
                data = call_suite(config["tool"], prompt)

            if data and data.get("status") == "success":
                st.session_state[result_key] = data
                st.rerun()
