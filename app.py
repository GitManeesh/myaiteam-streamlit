import os
import uuid

import requests
import streamlit as st

st.set_page_config(
    page_title="Mapranex. | AI Tools",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      :root {
        --bg: #000000;
        --sidebar: #050505;
        --panel: #2f2f2f;
        --panel-hover: #1d1d1d;
        --line: #242424;
        --text: #ececec;
        --muted: #8f8f8f;
        --cyan: #00d4ff;
        --blue: #0a84ff;
      }

      html, body, [class*="css"] {
        font-family: Arial, Helvetica, sans-serif;
      }

      html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: var(--bg) !important;
        color: var(--text) !important;
      }

      #MainMenu,
      footer,
      [data-testid="stToolbar"],
      [data-testid="stDecoration"],
      [data-testid="stStatusWidget"],
      [data-testid="stHeaderActionElements"],
      [data-testid="stAppDeployButton"] {
        display: none !important;
        visibility: hidden !important;
      }

      [data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
      }

      [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
      }

      /* Sidebar — ChatGPT-inspired compact layout */
      [data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
        background: #050505 !important;
        border-right: 1px solid #242424 !important;
      }

      [data-testid="stSidebar"] > div:first-child {
        padding: 0 10px 16px !important;
      }

      [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
      }

      .mx-brand-wrap {
        padding: 10px 4px 12px;
        margin: 0 0 8px;
      }

      .mx-brand {
        display: inline-flex;
        align-items: center;
        color: #fff;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -1.15px;
        white-space: nowrap;
      }

      .mx-brand img {
        width: 30px;
        height: 30px;
        object-fit: contain;
        margin: 0 9px 0 0;
        display: block;
      }

      .mx-brand .cyan,
      .mx-brand .period {
        color: var(--cyan);
      }

      .mx-brand-sub {
        margin: 3px 0 0 39px;
        color: #686868;
        font-size: 9px;
        font-weight: 700;
        letter-spacing: .8px;
        text-transform: uppercase;
      }

      .mx-side-divider {
        height: 1px;
        background: #202020;
        margin: 4px 0 8px;
      }

      .mx-side-section {
        margin: 8px 10px 6px;
        color: #626262;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: .8px;
      }

      /* Compact radio navigation without radio circles */
      [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        display: none !important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 2px !important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] > label {
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        min-height: 38px !important;
        height: 38px !important;
        padding: 0 10px !important;
        margin: 0 !important;
        border-radius: 8px !important;
        background: transparent !important;
        color: #bdbdbd !important;
        cursor: pointer !important;
        box-sizing: border-box !important;
        transition: background .14s ease, color .14s ease !important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] > label:hover {
        background: #1f1f1f !important;
        color: #fff !important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) {
        background: #202020 !important;
        color: #fff !important;
      }

      /* Hide all radio indicator visuals */
      [data-testid="stSidebar"] [role="radiogroup"] input[type="radio"] {
        position: absolute !important;
        opacity: 0 !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] > label > div:first-child {
        display: none !important;
        width: 0 !important;
        min-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] > label > div:last-child {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] p {
        margin: 0 !important;
        color: inherit !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        line-height: 38px !important;
      }

      [data-testid="stSidebar"] .stLinkButton {
        margin: 14px 4px 0 !important;
        padding-top: 10px;
        border-top: 1px solid #202020;
      }

      [data-testid="stSidebar"] .stLinkButton > a {
        width: 100%;
        min-height: 38px;
        height: 38px;
        justify-content: flex-start;
        padding: 0 10px;
        border-radius: 8px !important;
        border: 0 !important;
        background: transparent !important;
        color: #bdbdbd !important;
        font-size: 13px;
        font-weight: 500;
      }

      [data-testid="stSidebar"] .stLinkButton > a:hover {
        background: #1f1f1f !important;
        color: #fff !important;
      }

      .mx-side-foot {
        padding: 8px 10px 0;
        color: #505050;
        font-size: 10px;
        line-height: 1.45;
      }

      /* Main */
      .block-container {
        max-width: 980px !important;
        margin: 0 auto !important;
        padding: 0 24px 9rem !important;
      }

      .mx-topbar {
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid var(--line);
        background: #000;
        position: sticky;
        top: 0;
        z-index: 20;
      }

      .mx-top-title {
        color: #d8d8d8;
        font-size: 14px;
        font-weight: 650;
      }

      .mx-top-actions {
        display: flex;
        gap: 18px;
        color: #858585;
        font-size: 13px;
      }

      .mx-new-chat {
        max-width: 760px;
        min-height: calc(100vh - 250px);
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding-bottom: 86px;
      }

      .mx-new-chat h1 {
        margin: 0;
        color: #f1f1f1;
        font-size: 30px;
        line-height: 1.15;
        font-weight: 700;
        letter-spacing: -1.2px;
      }

      .mx-new-chat p {
        max-width: 580px;
        margin: 11px 0 0;
        color: #777;
        font-size: 13px;
        line-height: 1.6;
      }

      .mx-result-head {
        max-width: 780px;
        margin: 34px auto 18px;
      }

      .mx-result-head h1 {
        margin: 0;
        color: #f2f2f2;
        font-size: 28px;
        font-weight: 720;
        letter-spacing: -1px;
      }

      .mx-result-head p {
        margin: 8px 0 0;
        color: #848484;
        font-size: 13px;
        line-height: 1.55;
      }

      .mx-result-title {
        max-width: 780px;
        margin: 30px auto 10px;
        color: #f1f1f1;
        font-size: 19px;
        font-weight: 750;
        letter-spacing: -.4px;
      }

      [data-testid="stMarkdownContainer"] p,
      [data-testid="stMarkdownContainer"] li {
        color: #d0d0d0;
      }

      [data-testid="stAlert"],
      [data-testid="stExpander"] {
        max-width: 780px;
        margin-left: auto;
        margin-right: auto;
      }

      [data-testid="stExpander"] {
        border: 1px solid #3c3c3c !important;
        border-radius: 12px !important;
        background: #171717 !important;
      }

      /* Responsive composer */
      [data-testid="stBottom"] {
        position: fixed !important;
        left: 300px !important;
        right: 0 !important;
        bottom: 0 !important;
        width: auto !important;
        z-index: 1000 !important;
        background: linear-gradient(180deg, rgba(0,0,0,0) 0%, #000 35%, #000 100%) !important;
        padding: 24px 0 18px !important;
        border: 0 !important;
      }

      [data-testid="stBottom"] > div,
      [data-testid="stBottomBlockContainer"] {
        width: 100% !important;
        max-width: none !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        border: 0 !important;
      }

      [data-testid="stChatInput"] {
        width: min(760px, calc(100vw - 350px)) !important;
        margin: 0 auto !important;
        border: 1px solid #3b3b3b !important;
        border-radius: 26px !important;
        background: #2f2f2f !important;
        box-shadow: 0 8px 24px rgba(0,0,0,.3) !important;
        overflow: hidden !important;
      }

      [data-testid="stChatInput"] > div,
      [data-testid="stChatInput"] section {
        background: #2f2f2f !important;
        border: 0 !important;
      }

      [data-testid="stChatInput"] textarea {
        min-height: 58px !important;
        max-height: 200px !important;
        padding: 18px 62px 18px 20px !important;
        background: transparent !important;
        color: #ececec !important;
        -webkit-text-fill-color: #ececec !important;
        font-size: 16px !important;
        line-height: 1.45 !important;
        border: 0 !important;
        outline: 0 !important;
        box-shadow: none !important;
        resize: none !important;
        overflow-y: auto !important;
      }

      [data-testid="stChatInput"] textarea::placeholder {
        color: #8a8a8a !important;
        -webkit-text-fill-color: #8a8a8a !important;
        opacity: 1 !important;
      }

      [data-testid="stChatInput"] button {
        position: absolute !important;
        right: 11px !important;
        bottom: 11px !important;
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
        min-height: 36px !important;
        border: 0 !important;
        border-radius: 50% !important;
        color: #fff !important;
        background: var(--blue) !important;
      }

      .mx-about-grid {
        display: grid;
        grid-template-columns: repeat(2,minmax(0,1fr));
        gap: 14px;
        max-width: 780px;
        margin: 28px auto 0;
      }

      .mx-about-card {
        padding: 20px;
        border: 1px solid #2f2f2f;
        border-radius: 14px;
        background: #111;
      }

      .mx-about-card strong {
        display: block;
        color: #f2f2f2;
        margin-bottom: 7px;
      }

      .mx-about-card span {
        color: #8d8d8d;
        font-size: 13px;
        line-height: 1.55;
      }

      @media (max-width: 760px) {
        [data-testid="stSidebar"] {
          display: none;
        }

        [data-testid="stBottom"] {
          left: 0 !important;
        }

        [data-testid="stChatInput"] {
          width: calc(100vw - 24px) !important;
        }

        .block-container {
          padding: 0 14px 8rem !important;
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
    "Requirements": {
        "tool": "requirements_analyzer",
        "title": "Requirements Analyzer",
        "description": "Turn raw requirements into functional coverage, risks, acceptance criteria, and test scenarios.",
        "placeholder": "Message Requirements Analyzer",
    },
    "Test Cases": {
        "tool": "test_case_generator",
        "title": "Test Case Generator",
        "description": "Generate functional, negative, and edge test cases from a feature or requirement.",
        "placeholder": "Message Test Case Generator",
    },
    "API Tests": {
        "tool": "api_test_generator",
        "title": "API Test Generator",
        "description": "Generate positive, negative, validation, security, and example API tests.",
        "placeholder": "Message API Test Generator",
    },
    "Summarizer": {
        "tool": "document_summarizer",
        "title": "Document Summarizer",
        "description": "Condense technical or business text into decisions, key points, actions, and open questions.",
        "placeholder": "Message Document Summarizer",
    },
    "QA Assistant": {
        "tool": "qa_assistant",
        "title": "QA Assistant",
        "description": "Get practical help with QA strategy, defects, automation, and quality engineering decisions.",
        "placeholder": "Message QA Assistant",
    },
}

NAV_ITEMS = ["Requirements", "Test Cases", "API Tests", "Summarizer", "QA Assistant", "About"]

if "page" not in st.session_state:
    st.session_state.page = "Requirements"

with st.sidebar:
    st.markdown(
        """
        <div class="mx-brand-wrap">
          <div class="mx-brand">
            <img src="https://myaiteam-company.vercel.app/images/mapranex-logo.webp" alt="Mapranex logo">
            <span>Mapra</span><span class="cyan">nex</span><span class="period">.</span>
          </div>
          <div class="mx-brand-sub">AI Tools</div>
        </div>
        <div class="mx-side-divider"></div>
        <div class="mx-side-section">Tools</div>
        """,
        unsafe_allow_html=True,
    )

    current_index = NAV_ITEMS.index(st.session_state.page) if st.session_state.page in NAV_ITEMS else 0

    page = st.radio(
        "Navigation",
        NAV_ITEMS,
        index=current_index,
        label_visibility="collapsed",
        key="sidebar_navigation",
    )

    st.session_state.page = page

    st.link_button("Main website ↗", "https://myaiteam-company.vercel.app/")

    st.markdown(
        '<div class="mx-side-foot">n8n · OmniRoute · Oracle Cloud</div>',
        unsafe_allow_html=True,
    )

page = st.session_state.page


st.markdown(
    f"""
    <div class="mx-topbar">
      <div class="mx-top-title">{page}</div>
      <div class="mx-top-actions"><span>Share</span><span>•••</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

if page == "About":
    st.markdown(
        """
        <div class="mx-result-head">
          <h1>About Mapranex. AI Tools</h1>
          <p>Focused AI-assisted quality engineering tools backed by n8n and OmniRoute.</p>
        </div>
        <div class="mx-about-grid">
          <div class="mx-about-card">
            <strong>Architecture</strong>
            <span>Streamlit provides the workspace, n8n handles orchestration, and OmniRoute provides model access on Oracle Cloud.</span>
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

    if result_key in st.session_state:
        st.markdown(
            f"""
            <div class="mx-result-head">
              <h1>{config["title"]}</h1>
              <p>{config["description"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        data = st.session_state[result_key]

        if data and data.get("status") == "success":
            render_result(config["tool"], data.get("result") or {})

            with st.expander("Technical response details"):
                st.caption(f'Request ID: {data.get("request_id", "")}')
                st.json(data)
    else:
        st.markdown(
            f"""
            <div class="mx-new-chat">
              <h1>{config["title"]}</h1>
              <p>{config["description"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    prompt = st.chat_input(config["placeholder"])

    if prompt:
        if len(prompt.strip()) < 20:
            st.warning("Enter at least 20 characters.")
        else:
            with st.spinner("Processing with Mapranex. AI Tools..."):
                data = call_suite(config["tool"], prompt)

            if data and data.get("status") == "success":
                st.session_state[result_key] = data
                st.rerun()
