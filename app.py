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
        --bg:#000000;
        --sidebar:#050505;
        --panel:#2f2f2f;
        --panel-2:#1f1f1f;
        --panel-3:#303030;
        --line:#2b2b2b;
        --text:#ececec;
        --muted:#9b9b9b;
        --accent:#0a84ff;
      }

      html, body, [class*="css"] {
        font-family: Arial, Helvetica, sans-serif;
      }

      html, body, .stApp, [data-testid="stAppViewContainer"] {
        background:#000!important;
        color:var(--text)!important;
      }

      /* Hide Streamlit's in-app chrome where possible */
      #MainMenu,
      footer,
      [data-testid="stToolbar"],
      [data-testid="stDecoration"],
      [data-testid="stStatusWidget"],
      [data-testid="stHeaderActionElements"],
      [data-testid="stSidebarCollapsedControl"],
      [data-testid="stAppDeployButton"] {
        display:none!important;
        visibility:hidden!important;
      }

      [data-testid="stHeader"] {
        background:transparent!important;
        height:0!important;
        min-height:0!important;
      }

      /* Sidebar */
      [data-testid="stSidebar"] {
        background:var(--sidebar)!important;
        border-right:1px solid #242424;
        width:300px!important;
        min-width:300px!important;
      }

      [data-testid="stSidebar"] > div:first-child {
        padding:10px 8px 18px;
      }

      .mx-side-top {
        display:flex;
        align-items:center;
        justify-content:space-between;
        padding:4px 5px 14px;
      }

      .mx-brand {
        display:inline-flex;
        align-items:center;
        color:#fff;
        font-size:25px;
        font-weight:800;
        letter-spacing:-1.5px;
        white-space:nowrap;
      }

      .mx-brand img {
        width:32px;
        height:32px;
        object-fit:contain;
        margin-right:11px;
        border-radius:0;
        display:block;
      }

      .mx-brand .mx-brand-cyan,
      .mx-brand .mx-brand-period {
        color:#00d4ff;
      }

      .mx-brand-subtitle {
        margin:6px 0 0 43px;
        color:#747474;
        font-size:11px;
        line-height:1.35;
        letter-spacing:0;
        font-weight:500;
      }

      .mx-side-icon {
        color:#8d8d8d;
        font-size:17px;
      }

      .mx-new {
        margin:0 2px 14px;
        padding:11px 12px;
        border-radius:9px;
        background:#202020;
        border:1px solid #2f2f2f;
        color:#dcdcdc;
        font-size:13px;
        font-weight:650;
      }

      .mx-section {
        margin:14px 10px 7px;
        color:#666;
        font-size:10px;
        font-weight:800;
        letter-spacing:1px;
        text-transform:uppercase;
      }

      [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        display:none;
      }

      [data-testid="stSidebar"] [role="radiogroup"] {
        gap:3px;
      }

      [data-testid="stSidebar"] [role="radiogroup"] input[type="radio"] {
        display:none!important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] label {
        min-height:40px;
        padding:0 11px!important;
        border-radius:8px;
        color:#bdbdbd!important;
        background:transparent;
        transition:background .14s ease,color .14s ease;
      }

      [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background:#242424;
        color:#fff!important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background:#202020;
        color:#fff!important;
      }

      [data-testid="stSidebar"] [role="radiogroup"] label p {
        color:inherit!important;
        font-size:13px;
        font-weight:600;
      }

      [data-testid="stSidebar"] .stLinkButton {
        margin:16px 2px 0;
      }

      [data-testid="stSidebar"] .stLinkButton > a {
        width:100%;
        justify-content:flex-start;
        min-height:40px;
        padding:0 12px;
        border-radius:8px!important;
        border:0!important;
        background:transparent!important;
        color:#bdbdbd!important;
        font-size:13px;
        font-weight:600;
      }

      [data-testid="stSidebar"] .stLinkButton > a:hover {
        background:#242424!important;
        color:#fff!important;
      }

      .mx-side-bottom {
        margin:26px 4px 0;
        padding-top:14px;
        border-top:1px solid #292929;
        color:#666;
        font-size:10px;
        line-height:1.55;
      }

      .mx-live {
        display:inline-block;
        width:7px;
        height:7px;
        margin-right:6px;
        border-radius:50%;
        background:#28c840;
      }

      /* Main top bar */
      .block-container {
        max-width: 980px !important;
        padding-top: 0 !important;
        padding-bottom: 13rem !important;
        margin: 0 auto !important;
      }

      .mx-topbar {
        height: 52px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        border-bottom:1px solid #242424;
        margin-bottom:0;
        position: sticky;
        top: 0;
        z-index: 20;
        background:#000;
      }

      .mx-top-title {
        color:#dedede;
        font-size:14px;
        font-weight:650;
      }

      .mx-top-actions {
        display:flex;
        gap:18px;
        color:#8e8e8e;
        font-size:13px;
      }

      /* Conversation area */
      .mx-page-head {
        max-width: 780px;
        margin: 34px auto 18px;
        padding: 0 2px;
      }

      .mx-eyebrow {
        color:var(--accent);
        font-size:11px;
        font-weight:800;
        letter-spacing:1px;
        text-transform:uppercase;
        margin-bottom:9px;
      }

      .mx-page-title {
        margin:0;
        color:#f2f2f2;
        font-size: 32px;
        line-height:1.15;
        letter-spacing:-1.25px;
        font-weight:750;
      }

      .mx-page-subtitle {
        max-width:720px;
        margin:9px 0 0;
        color:#929292;
        font-size:14px;
        line-height:1.6;
      }

      .mx-empty {
        max-width:780px;
        min-height: 300px;
        margin:0 auto;
        display:flex;
        align-items:center;
        justify-content:center;
        color:#707070;
        text-align:center;
        font-size:13px;
      }

      .mx-result-title {
        max-width:780px;
        margin:30px auto 10px;
        color:#f1f1f1;
        font-size:19px;
        font-weight:750;
        letter-spacing:-.4px;
      }

      [data-testid="stMarkdownContainer"] p,
      [data-testid="stMarkdownContainer"] li {
        color:#d0d0d0;
      }

      [data-testid="stAlert"] {
        max-width:780px;
        margin-left:auto;
        margin-right:auto;
        border-radius:12px;
        border:1px solid #414141!important;
        background:#292929!important;
        color:#e7e7e7!important;
      }

      [data-testid="stExpander"] {
        max-width:780px;
        margin-left:auto;
        margin-right:auto;
        border:1px solid #414141!important;
        border-radius:12px!important;
        overflow:hidden;
        background:#292929!important;
      }

      [data-testid="stExpander"] summary,
      [data-testid="stExpander"] p,
      [data-testid="stExpander"] span {
        color:#e7e7e7!important;
      }

      /* ChatGPT-style bottom composer */
      [data-testid="stBottom"] {
        position: fixed !important;
        left: 300px !important;
        right: 0 !important;
        bottom: 0 !important;
        width: auto !important;
        z-index: 1000 !important;
        background: linear-gradient(180deg, rgba(0,0,0,0) 0%, #000 24%, #000 100%) !important;
        padding: 30px 0 24px !important;
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
        position: relative !important;
        width: 780px !important;
        max-width: calc(100vw - 350px) !important;
        min-height: 150px !important;
        margin: 0 auto !important;
        border: 1px solid #3f3f3f !important;
        border-radius: 28px !important;
        background: #2f2f2f !important;
        box-shadow: 0 10px 34px rgba(0,0,0,.42) !important;
        overflow: hidden !important;
      }

      [data-testid="stChatInput"] > div,
      [data-testid="stChatInput"] section,
      [data-testid="stChatInput"] div {
        background: #2f2f2f !important;
        border: 0 !important;
      }

      [data-testid="stChatInput"] textarea {
        width: 100% !important;
        min-height: 150px !important;
        max-height: 220px !important;
        padding: 22px 72px 50px 22px !important;
        background: #2f2f2f !important;
        color: #ececec !important;
        -webkit-text-fill-color: #ececec !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
        border: 0 !important;
        outline: none !important;
        box-shadow: none !important;
        resize: none !important;
      }

      [data-testid="stChatInput"] textarea::placeholder {
        color: #8a8a8a !important;
        -webkit-text-fill-color: #8a8a8a !important;
        opacity: 1 !important;
      }

      [data-testid="stChatInput"] button {
        position: absolute !important;
        right: 14px !important;
        bottom: 14px !important;
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        min-height: 38px !important;
        margin: 0 !important;
        padding: 0 !important;
        border: 0 !important;
        border-radius: 50% !important;
        color: #fff !important;
        background: #0a84ff !important;
        box-shadow: none !important;
      }

      [data-testid="stChatInput"] button:hover {
        background: #2b95ff !important;
      }

      .mx-about-grid {
        display:grid;
        grid-template-columns:repeat(2,minmax(0,1fr));
        gap:14px;
        max-width:780px;
        margin:22px auto 0;
      }

      .mx-about-card {
        padding:19px;
        border:1px solid #3f3f3f;
        border-radius:14px;
        background:#292929;
      }

      .mx-about-card strong {
        display:block;
        color:#f2f2f2;
        margin-bottom:7px;
      }

      .mx-about-card span {
        color:#999;
        font-size:13px;
        line-height:1.55;
      }

      @media (max-width:760px) {
        [data-testid="stSidebar"] {
          display:none;
        }

        [data-testid="stBottom"] {
          left:0!important;
        }

        [data-testid="stChatInput"] {
          width: calc(100vw - 28px) !important;
          max-width: calc(100vw - 28px) !important;
        }

        .block-container {
          padding:0 1rem 10rem;
        }

        .mx-about-grid {
          grid-template-columns:1fr;
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
        "tool":"requirements_analyzer",
        "title":"Requirements Analyzer",
        "description":"Turn raw requirements into structured functional coverage, risks, acceptance criteria, and test scenarios.",
        "placeholder":"Message Requirements Analyzer",
    },
    "Test Cases": {
        "tool":"test_case_generator",
        "title":"Test Case Generator",
        "description":"Generate structured functional, negative, and edge test cases from a feature or requirement.",
        "placeholder":"Message Test Case Generator",
    },
    "API Tests": {
        "tool":"api_test_generator",
        "title":"API Test Generator",
        "description":"Generate positive, negative, validation, security, and example API tests from an endpoint description.",
        "placeholder":"Message API Test Generator",
    },
    "Summarizer": {
        "tool":"document_summarizer",
        "title":"Document Summarizer",
        "description":"Condense technical or business text into decisions, key points, actions, and open questions.",
        "placeholder":"Message Document Summarizer",
    },
    "QA Assistant": {
        "tool":"qa_assistant",
        "title":"QA Assistant",
        "description":"Get practical help with QA strategy, defects, automation, testing decisions, and quality engineering problems.",
        "placeholder":"Message QA Assistant",
    },
}


with st.sidebar:
    st.markdown(
        """
        <div class="mx-side-top">
          <div>
            <div class="mx-brand">
              <img src="https://myaiteam-company.vercel.app/images/mapranex-logo.webp" alt="Mapranex logo">
              <span>Mapra</span><span class="mx-brand-cyan">nex</span><span class="mx-brand-period">.</span>
            </div>
            <div class="mx-brand-subtitle">AI Tools</div>
          </div>
          <span class="mx-side-icon">⌕</span>
        </div>
        <div class="mx-new">＋ New analysis</div>
        <div class="mx-section">Tools</div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        ["Requirements", "Test Cases", "API Tests", "Summarizer", "QA Assistant", "About"],
        label_visibility="collapsed",
    )

    st.link_button("↗ Main website", "https://myaiteam-company.vercel.app/")

    st.markdown(
        """
        <div class="mx-side-bottom">
          <div><span class="mx-live"></span>Services connected</div>
          <div style="margin-top:6px;">n8n · OmniRoute · Oracle Cloud</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    f"""
    <div class="mx-topbar">
      <div class="mx-top-title">{page if page != "About" else "About Mapranex."} ▾</div>
      <div class="mx-top-actions"><span>Share</span><span>•••</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)


if page == "About":
    st.markdown(
        """
        <div class="mx-page-head">
          <div class="mx-page-title">Built for focused AI-assisted quality work.</div>
          <p class="mx-page-subtitle">
            Mapranex. AI Tools keeps the interface simple while n8n and OmniRoute handle secure orchestration behind the scenes.
          </p>
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

    st.markdown(
        f"""
        <div class="mx-page-head">
          <div class="mx-eyebrow">Mapranex. AI Tools</div>
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
            '<div class="mx-empty">Your result will appear here after you send a message.</div>',
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
