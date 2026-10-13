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

webhook = get_secret('N8N_WEBHOOK_URL')
shared_secret = get_secret('N8N_SHARED_SECRET')

tab1, tab2 = st.tabs(['Workflow Assistant', 'About'])

with tab1:
    st.subheader('AI Workflow Assistant')
    st.write('Describe a task or workflow you want Mapranex to process.')

    user_input = st.text_area(
        'Your request',
        placeholder='Example: Summarize this workflow and suggest the next automation step.',
        max_chars=5000,
        height=160,
    )

    if 'last_submit_ts' not in st.session_state:
        st.session_state.last_submit_ts = 0.0

    if st.button('Run AI workflow', type='primary'):
        now = time.time()
        if now - st.session_state.last_submit_ts < 3:
            st.warning('Please wait a few seconds before submitting again.')
        elif not webhook:
            st.error('N8N_WEBHOOK_URL is not configured in Streamlit secrets.')
        elif not shared_secret:
            st.error('N8N_SHARED_SECRET is not configured in Streamlit secrets.')
        elif not webhook.startswith('https://'):
            st.error('Webhook URL must use HTTPS.')
        elif not user_input.strip():
            st.warning('Enter a request first.')
        else:
            st.session_state.last_submit_ts = now
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
                        webhook,
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
    st.write('Requirements Analyzer · Test Case Generator · API Test Generator · Document Summarizer · QA Assistant')

with tab2:
    st.markdown('**Architecture**')
    st.write('Vercel hosts the main Mapranex website. Streamlit hosts Python AI tools. n8n runs the automation workflows on the existing Oracle Cloud instance.')
    st.markdown('**Security**')
    st.write('The webhook URL and shared authentication secret are stored server-side in Streamlit secrets and are not displayed in the UI.')
