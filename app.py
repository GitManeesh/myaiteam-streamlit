import os
import time
import uuid

import requests
import streamlit as st

st.set_page_config(page_title='Mapranex | AI Tools', page_icon='🤖', layout='wide')

st.title('Mapranex · AI Tools')
st.caption('Practical AI utilities powered by Streamlit and n8n.')
st.link_button('← Main website', 'https://myaiteam-company.vercel.app/')


def get_secret(name: str) -> str:
    try:
        return st.secrets.get(name, os.getenv(name, ''))
    except Exception:
        return os.getenv(name, '')


def render_list_section(title: str, values) -> None:
    st.markdown(f'### {title}')
    if isinstance(values, list) and values:
        for item in values:
            st.markdown(f'- {item}')
    else:
        st.caption('No items returned.')


workflow_webhook = get_secret('N8N_WEBHOOK_URL')
requirements_webhook = get_secret('N8N_REQUIREMENTS_WEBHOOK_URL') or (
    'https://n8n.myaiteam.work.gd/webhook/myaiteam-requirements-analyzer'
)
shared_secret = get_secret('N8N_SHARED_SECRET')

requirements_tab, workflow_tab, about_tab = st.tabs(
    ['Requirements Analyzer', 'Workflow Assistant', 'About']
)

with requirements_tab:
    st.subheader('Requirements Analyzer')
    st.write(
        'Paste a software requirement, user story, or feature description. '
        'Mapranex will analyze it for clarity, risks, acceptance criteria, and test coverage.'
    )

    requirements_input = st.text_area(
        'Requirements',
        placeholder=(
            'Example: Users should be able to upload a PDF invoice, extract supplier name, '
            'invoice number, amount, VAT, and due date.'
        ),
        max_chars=10000,
        height=200,
        key='requirements_input',
    )

    if 'requirements_last_submit_ts' not in st.session_state:
        st.session_state.requirements_last_submit_ts = 0.0

    if st.button('Analyze requirements', type='primary', key='analyze_requirements'):
        now = time.time()
        if now - st.session_state.requirements_last_submit_ts < 3:
            st.warning('Please wait a few seconds before submitting again.')
        elif not shared_secret:
            st.error('N8N_SHARED_SECRET is not configured in Streamlit secrets.')
        elif not requirements_webhook.startswith('https://'):
            st.error('Requirements webhook URL must use HTTPS.')
        elif len(requirements_input.strip()) < 20:
            st.warning('Enter at least 20 characters of requirements text.')
        else:
            st.session_state.requirements_last_submit_ts = now
            payload = {
                'requirements': requirements_input.strip(),
                'source': 'myaiteam-streamlit',
                'request_id': str(uuid.uuid4()),
            }
            headers = {
                'Content-Type': 'application/json',
                'X-Mapranex-Token': shared_secret,
            }

            with st.spinner('Analyzing requirements...'):
                try:
                    response = requests.post(
                        requirements_webhook,
                        json=payload,
                        headers=headers,
                        timeout=60,
                    )
                    response.raise_for_status()
                    data = response.json()

                    if not isinstance(data, dict) or data.get('status') != 'success':
                        st.error('The Requirements Analyzer returned an unexpected response.')
                        st.json(data)
                    else:
                        analysis = data.get('analysis') or {}
                        st.success('Requirements analysis completed.')

                        st.markdown('### Summary')
                        st.write(analysis.get('summary') or 'No summary returned.')

                        render_list_section(
                            'Functional Requirements',
                            analysis.get('functional_requirements'),
                        )
                        render_list_section(
                            'Non-Functional Requirements',
                            analysis.get('non_functional_requirements'),
                        )
                        render_list_section('Ambiguities', analysis.get('ambiguities'))
                        render_list_section('Risks', analysis.get('risks'))
                        render_list_section(
                            'Acceptance Criteria',
                            analysis.get('acceptance_criteria'),
                        )
                        render_list_section(
                            'Test Scenarios',
                            analysis.get('test_scenarios'),
                        )
                        render_list_section(
                            'Questions for Stakeholder',
                            analysis.get('questions_for_stakeholder'),
                        )

                        with st.expander('Technical response details'):
                            st.caption(f"Request ID: {data.get('request_id', 'Not returned')}")
                            st.json(data)
                except requests.HTTPError as exc:
                    if exc.response is not None and exc.response.status_code in (401, 403):
                        st.error('Authentication failed between Streamlit and n8n.')
                    elif exc.response is not None and exc.response.status_code == 400:
                        st.error('n8n rejected the requirements input. Check the workflow validation.')
                    else:
                        st.error('The Requirements Analyzer returned an error. Check the n8n execution log.')
                except ValueError:
                    st.error('The Requirements Analyzer returned an invalid response.')
                except requests.RequestException:
                    st.error('The Requirements Analyzer could not be reached. Check the n8n webhook configuration.')

with workflow_tab:
    st.subheader('AI Workflow Assistant')
    st.write('Describe a task or workflow you want Mapranex to process.')

    user_input = st.text_area(
        'Your request',
        placeholder='Example: Summarize this workflow and suggest the next automation step.',
        max_chars=5000,
        height=160,
        key='workflow_input',
    )

    if 'workflow_last_submit_ts' not in st.session_state:
        st.session_state.workflow_last_submit_ts = 0.0

    if st.button('Run AI workflow', type='primary', key='run_workflow'):
        now = time.time()
        if now - st.session_state.workflow_last_submit_ts < 3:
            st.warning('Please wait a few seconds before submitting again.')
        elif not workflow_webhook:
            st.error('N8N_WEBHOOK_URL is not configured in Streamlit secrets.')
        elif not shared_secret:
            st.error('N8N_SHARED_SECRET is not configured in Streamlit secrets.')
        elif not workflow_webhook.startswith('https://'):
            st.error('Webhook URL must use HTTPS.')
        elif not user_input.strip():
            st.warning('Enter a request first.')
        else:
            st.session_state.workflow_last_submit_ts = now
            payload = {
                'tool': 'workflow_assistant',
                'message': user_input.strip(),
                'source': 'myaiteam-streamlit',
                'request_id': str(uuid.uuid4()),
            }
            headers = {
                'Content-Type': 'application/json',
                'X-Mapranex-Token': shared_secret,
            }

            with st.spinner('Running workflow...'):
                try:
                    response = requests.post(
                        workflow_webhook,
                        json=payload,
                        headers=headers,
                        timeout=30,
                    )
                    response.raise_for_status()
                    try:
                        data = response.json()
                    except ValueError:
                        data = {'message': response.text[:10000]}

                    if isinstance(data, dict) and data.get('status') == 'success':
                        st.success('Workflow completed.')
                    st.json(data)
                except requests.HTTPError as exc:
                    if exc.response is not None and exc.response.status_code in (401, 403):
                        st.error('Authentication failed between Streamlit and n8n.')
                    else:
                        st.error('The workflow returned an error. Check the n8n execution log.')
                except requests.RequestException:
                    st.error('The workflow could not be reached. Check the n8n webhook and network configuration.')

    st.divider()
    st.markdown('**Planned next tools**')
    st.write('Test Case Generator · API Test Generator · Document Summarizer · QA Assistant')

with about_tab:
    st.markdown('**Architecture**')
    st.write(
        'Vercel hosts the main Mapranex website. Streamlit hosts Python AI tools. '
        'n8n runs the automation workflows on the existing Oracle Cloud instance.'
    )
    st.markdown('**Security**')
    st.write(
        'The webhook URLs and shared authentication secret are stored server-side '
        'and are not displayed in the UI.'
    )
