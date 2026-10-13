import os
import time
import uuid
import requests
import streamlit as st

st.set_page_config(page_title="Mapranex | AI Tools", page_icon="🤖", layout="wide")
st.title("Mapranex · AI Tools")
st.caption("Practical AI utilities powered by Streamlit and n8n.")
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
    payload = {"tool": tool, "input": text.strip(), "source": "myaiteam-streamlit", "request_id": str(uuid.uuid4())}
    headers = {"Content-Type": "application/json", "X-Mapranex-Token": secret}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=90)
        r.raise_for_status()
        return r.json()
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code in (401,403):
            st.error("Authentication failed between Streamlit and n8n.")
        else:
            st.error("The AI tool returned an error. Check the n8n execution log.")
    except requests.RequestException:
        st.error("The AI tool could not be reached.")
    return None

def render_list(title, values):
    st.markdown(f"### {title}")
    if not values:
        st.caption("No items returned.")
        return
    for item in values:
        if isinstance(item, dict):
            st.json(item)
        else:
            st.markdown(f"- {item}")

def render_result(tool, r):
    if tool == "requirements_analyzer":
        st.markdown("### Summary"); st.write(r.get("summary",""))
        render_list("Functional Requirements", r.get("functional_requirements"))
        render_list("Non-Functional Requirements", r.get("non_functional_requirements"))
        render_list("Ambiguities", r.get("ambiguities"))
        render_list("Risks", r.get("risks"))
        render_list("Acceptance Criteria", r.get("acceptance_criteria"))
        render_list("Test Scenarios", r.get("test_scenarios"))
        render_list("Questions for Stakeholder", r.get("questions_for_stakeholder"))
    elif tool == "test_case_generator":
        st.markdown("### Summary"); st.write(r.get("summary",""))
        st.markdown("### Test Cases")
        for tc in r.get("test_cases",[]):
            with st.expander(f"{tc.get('id','TC')} — {tc.get('title','Test Case')}"):
                st.write(f"**Priority:** {tc.get('priority','')}")
                st.write(f"**Preconditions:** {tc.get('preconditions','')}")
                st.write("**Steps:**")
                steps = tc.get("steps",[])
                if isinstance(steps,list):
                    for i,s in enumerate(steps,1): st.write(f"{i}. {s}")
                else: st.write(steps)
                st.write(f"**Expected result:** {tc.get('expected_result','')}")
        render_list("Edge Cases", r.get("edge_cases"))
        render_list("Negative Cases", r.get("negative_cases"))
        render_list("Assumptions", r.get("assumptions"))
    elif tool == "api_test_generator":
        st.markdown("### Summary"); st.write(r.get("summary",""))
        render_list("Positive Tests", r.get("positive_tests"))
        render_list("Negative Tests", r.get("negative_tests"))
        render_list("Validation Tests", r.get("validation_tests"))
        render_list("Security Tests", r.get("security_tests"))
        render_list("Example Requests", r.get("example_requests"))
        render_list("Assumptions", r.get("assumptions"))
    elif tool == "document_summarizer":
        st.markdown("### Summary"); st.write(r.get("summary",""))
        render_list("Key Points", r.get("key_points"))
        render_list("Decisions", r.get("decisions"))
        render_list("Action Items", r.get("action_items"))
        render_list("Risks / Open Questions", r.get("risks_or_open_questions"))
    elif tool == "qa_assistant":
        st.markdown("### Answer"); st.write(r.get("answer",""))
        render_list("Recommended Actions", r.get("recommended_actions"))
        render_list("Risks", r.get("risks"))
        render_list("Checks", r.get("checks"))
        render_list("Assumptions", r.get("assumptions"))

def tool_tab(tool, title, description, placeholder, button):
    st.subheader(title)
    st.write(description)
    text = st.text_area("Input", placeholder=placeholder, height=220, key=f"{tool}_input")
    if st.button(button, type="primary", key=f"{tool}_button"):
        if len(text.strip()) < 20:
            st.warning("Enter at least 20 characters.")
        else:
            with st.spinner("Processing..."):
                data = call_suite(tool, text)
            if data and data.get("status") == "success":
                st.success("Completed.")
                render_result(tool, data.get("result") or {})
                with st.expander("Technical response details"):
                    st.caption(f"Request ID: {data.get('request_id','')}")
                    st.json(data)

tabs = st.tabs([
    "Requirements Analyzer",
    "Test Case Generator",
    "API Test Generator",
    "Document Summarizer",
    "QA Assistant",
    "Workflow Assistant",
    "About",
])

with tabs[0]:
    tool_tab("requirements_analyzer","Requirements Analyzer","Analyze requirements for completeness, risks, acceptance criteria, and test coverage.","Paste a requirement, user story, or feature description.","Analyze requirements")

with tabs[1]:
    tool_tab("test_case_generator","Test Case Generator","Generate structured functional, negative, and edge test cases.","Paste the requirement or feature.","Generate test cases")

with tabs[2]:
    tool_tab("api_test_generator","API Test Generator","Generate API test coverage from an endpoint description, API requirement, or OpenAPI excerpt.","Paste an API endpoint description or OpenAPI excerpt.","Generate API tests")

with tabs[3]:
    tool_tab("document_summarizer","Document Summarizer","Summarize business or technical text into key points, decisions, actions, and open questions.","Paste the document text.","Summarize document")

with tabs[4]:
    tool_tab("qa_assistant","QA Assistant","Ask a QA, test automation, defect analysis, or quality engineering question.","Describe the QA question, defect, test problem, or context.","Ask QA Assistant")

with tabs[5]:
    st.subheader("AI Workflow Assistant")
    st.write("Describe a task or workflow you want Mapranex to process.")
    webhook = get_secret("N8N_WEBHOOK_URL")
    secret = get_secret("N8N_SHARED_SECRET")
    text = st.text_area("Your request", placeholder="Example: Summarize this workflow and suggest the next automation step.", height=160, key="workflow_input")
    if st.button("Run AI workflow", type="primary", key="workflow_button"):
        if not webhook or not secret:
            st.error("Workflow webhook or shared secret is not configured.")
        elif not text.strip():
            st.warning("Enter a request first.")
        else:
            payload = {"tool":"workflow_assistant","message":text.strip(),"source":"myaiteam-streamlit","request_id":str(uuid.uuid4())}
            headers = {"Content-Type":"application/json","X-Mapranex-Token":secret}
            try:
                r = requests.post(webhook,json=payload,headers=headers,timeout=30)
                r.raise_for_status()
                data = r.json()
                if data.get("status") == "success": st.success("Workflow completed.")
                st.json(data)
            except requests.RequestException:
                st.error("The workflow returned an error. Check n8n.")

with tabs[6]:
    st.markdown("**Architecture**")
    st.write("Vercel hosts the main Mapranex website. Streamlit hosts Python AI tools. n8n runs the automation workflows on Oracle Cloud.")
    st.markdown("**Security**")
    st.write("Webhook URLs and authentication secrets are stored server-side and are not displayed in the UI.")
