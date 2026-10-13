import os
import time
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
        --mx-navy: #081e35;
        --mx-navy-2: #0a2540;
        --mx-cyan: #00d4ff;
        --mx-cyan-2: #0aa8d2;
        --mx-violet: #7c5cff;
        --mx-ink: #122b43;
        --mx-muted: #687b8d;
        --mx-line: #e3eaf0;
        --mx-soft: #f5f8fb;
        --mx-white: #ffffff;
      }

      html, body, [class*="css"] {
        font-family: Arial, Helvetica, sans-serif;
      }

      .stApp {
        background:
          radial-gradient(circle at 88% 0%, rgba(0, 212, 255, 0.08), transparent 24rem),
          linear-gradient(180deg, #f7fafc 0%, #ffffff 38%);
        color: var(--mx-ink);
      }

      [data-testid="stHeader"] {
        background: rgba(255,255,255,.86);
        backdrop-filter: blur(14px);
        border-bottom: 1px solid rgba(227,234,240,.85);
      }

      [data-testid="stAppViewContainer"] > .main {
        background: transparent;
      }

      .block-container {
        max-width: 1240px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
      }

      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}

      .mx-hero {
        position: relative;
        overflow: hidden;
        border-radius: 24px;
        padding: 34px 38px;
        margin-bottom: 22px;
        color: #fff;
        background:
          radial-gradient(circle at 82% 35%, rgba(0,212,255,.22), transparent 30%),
          linear-gradient(135deg, #081e35 0%, #0a2540 58%, #103d59 100%);
        border: 1px solid rgba(255,255,255,.08);
        box-shadow: 0 24px 70px rgba(8,30,53,.16);
      }

      .mx-hero:after {
        content: "";
        position: absolute;
        width: 340px;
        height: 340px;
        right: -90px;
        top: -150px;
        border-radius: 50%;
        border: 1px solid rgba(0,212,255,.24);
        box-shadow:
          0 0 0 38px rgba(0,212,255,.045),
          0 0 0 78px rgba(0,212,255,.025);
      }

      .mx-kicker {
        position: relative;
        z-index: 1;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        color: var(--mx-cyan);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.8px;
        text-transform: uppercase;
      }

      .mx-kicker:before {
        content: "";
        width: 22px;
        height: 2px;
        background: var(--mx-cyan);
      }

      .mx-title {
        position: relative;
        z-index: 1;
        margin: 12px 0 8px;
        font-size: clamp(34px, 4vw, 54px);
        line-height: 1.05;
        letter-spacing: -2.5px;
        font-weight: 800;
      }

      .mx-title span { color: var(--mx-cyan); }

      .mx-subtitle {
        position: relative;
        z-index: 1;
        max-width: 720px;
        margin: 0;
        color: #bfd0df;
        font-size: 15px;
        line-height: 1.65;
      }

      .mx-meta {
        position: relative;
        z-index: 1;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 22px;
      }

      .mx-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        border-radius: 999px;
        padding: 7px 11px;
        background: rgba(255,255,255,.08);
        border: 1px solid rgba(255,255,255,.12);
        color: #d5e2ec;
        font-size: 11px;
        font-weight: 700;
      }

      .mx-tool-card {
        margin: 18px 0 18px;
        padding: 22px 24px;
        background: rgba(255,255,255,.92);
        border: 1px solid var(--mx-line);
        border-radius: 18px;
        box-shadow: 0 12px 35px rgba(10,37,64,.06);
      }

      .mx-tool-head {
        display: flex;
        align-items: flex-start;
        gap: 14px;
      }

      .mx-tool-icon {
        width: 42px;
        height: 42px;
        flex: 0 0 42px;
        display: grid;
        place-items: center;
        border-radius: 12px;
        background: #eafaff;
        color: #067fa2;
        font-size: 19px;
        font-weight: 800;
      }

      .mx-tool-card h3 {
        margin: 0 0 5px;
        color: var(--mx-navy);
        font-size: 21px;
        letter-spacing: -.6px;
      }

      .mx-tool-card p {
        margin: 0;
        color: var(--mx-muted);
        font-size: 13px;
        line-height: 1.6;
      }

      div[data-baseweb="tab-list"] {
        gap: 6px;
        padding: 6px;
        margin-top: 6px;
        margin-bottom: 14px;
        overflow-x: auto;
        border: 1px solid var(--mx-line);
        border-radius: 14px;
        background: rgba(255,255,255,.92);
        box-shadow: 0 10px 30px rgba(10,37,64,.05);
      }

      button[data-baseweb="tab"] {
        height: 40px;
        white-space: nowrap;
        border-radius: 9px;
        padding: 0 14px;
        color: #53697b;
        font-size: 12px;
        font-weight: 800;
      }

      button[data-baseweb="tab"][aria-selected="true"] {
        color: #fff !important;
        background: var(--mx-navy-2) !important;
      }

      button[data-baseweb="tab"][aria-selected="true"] p {
        color: #fff !important;
      }

      [data-testid="stTextArea"] textarea {
        min-height: 190px !important;
        border-radius: 16px !important;
        border: 1px solid #dce6ed !important;
        background: #fbfdff !important;
        padding: 16px !important;
        color: var(--mx-ink) !important;
        box-shadow: inset 0 1px 2px rgba(10,37,64,.025);
      }

      [data-testid="stTextArea"] textarea:focus {
        border-color: var(--mx-cyan-2) !important;
        box-shadow: 0 0 0 3px rgba(0,212,255,.12) !important;
      }

      .stButton > button,
      .stLinkButton > a {
        min-height: 42px;
        border-radius: 10px !important;
        border: 1px solid #d9e4eb !important;
        font-weight: 800 !important;
        transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
      }

      .stButton > button[kind="primary"] {
        color: #08243d !important;
        background: var(--mx-cyan) !important;
        border-color: var(--mx-cyan) !important;
        box-shadow: 0 10px 22px rgba(0,212,255,.18);
      }

      .stButton > button:hover,
      .stLinkButton > a:hover {
        transform: translateY(-1px);
        border-color: #b8cad6 !important;
      }

      .stButton > button[kind="primary"]:hover {
        box-shadow: 0 14px 28px rgba(0,212,255,.24);
      }

      [data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid var(--mx-line);
      }

      [data-testid="stExpander"] {
        border: 1px solid var(--mx-line);
        border-radius: 14px;
        overflow: hidden;
        background: #fff;
      }

      .mx-result-title {
        margin: 26px 0 10px;
        color: var(--mx-navy);
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -.5px;
      }

      .mx-about-grid {
        display: grid;
        grid-template-columns: repeat(2,minmax(0,1fr));
        gap: 16px;
        margin-top: 14px;
      }

      .mx-about-card {
        padding: 20px;
        border: 1px solid var(--mx-line);
        border-radius: 16px;
        background: #fff;
        box-shadow: 0 10px 28px rgba(10,37,64,.045);
      }

      .mx-about-card strong {
        display: block;
        color: var(--mx-navy);
        margin-bottom: 7px;
      }

      .mx-about-card span {
        color: var(--mx-muted);
        font-size: 13px;
        line-height: 1.55;
      }

      @media (max-width: 760px) {
        .block-container { padding-top: 1rem; }
        .mx-hero { padding: 26px 22px; border-radius: 18px; }
        .mx-title { font-size: 36px; }
        .mx-about-grid { grid-template-columns: 1fr; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="mx-hero">
      <div class="mx-kicker">Mapranex AI workspace</div>
      <div class="mx-title">Practical AI for <span>quality engineering.</span></div>
      <p class="mx-subtitle">
        Analyze requirements, generate test coverage, validate APIs, summarize documents,
        and solve QA problems from one secure workspace connected to your n8n automation stack.
      </p>
      <div class="mx-meta">
        <span class="mx-pill">✦ OmniRoute powered</span>
        <span class="mx-pill">↔ n8n automated</span>
        <span class="mx-pill">◈ Secure gateway</span>
      </div>
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
        "Workflow",
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
        <div class="mx-tool-card">
          <div class="mx-tool-head">
            <div class="mx-tool-icon">↔</div>
            <div>
              <h3>AI Workflow Assistant</h3>
              <p>Send a workflow or automation task through the existing secure n8n workflow gateway.</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    webhook = get_secret("N8N_WEBHOOK_URL")
    secret = get_secret("N8N_SHARED_SECRET")

    text = st.text_area(
        "Your request",
        placeholder="Describe the workflow, automation, or process you want Mapranex to handle...",
        height=220,
        key="workflow_input",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        run_workflow = st.button(
            "Run workflow",
            type="primary",
            key="workflow_button",
            use_container_width=True,
        )

    if run_workflow:
        if not webhook or not secret:
            st.error("Workflow webhook or shared secret is not configured.")
        elif not text.strip():
            st.warning("Enter a request first.")
        else:
            payload = {
                "tool": "workflow_assistant",
                "message": text.strip(),
                "source": "myaiteam-streamlit",
                "request_id": str(uuid.uuid4()),
            }
            headers = {
                "Content-Type": "application/json",
                "X-Mapranex-Token": secret,
            }

            with st.spinner("Running workflow..."):
                try:
                    response = requests.post(
                        webhook,
                        json=payload,
                        headers=headers,
                        timeout=30,
                    )
                    response.raise_for_status()
                    data = response.json()

                    if data.get("status") == "success":
                        st.success("Workflow completed.")
                    st.json(data)

                except requests.RequestException:
                    st.error("The workflow returned an error. Check n8n.")


with tabs[6]:
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
