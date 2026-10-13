import os
import streamlit as st
import requests

st.set_page_config(page_title='MyAITeam | AI Tools', page_icon='🤖', layout='wide')
st.title('MyAITeam · AI Tools')
st.caption('Python-powered tools alongside the existing MyAITeam website.')
st.link_button('← Main website', 'https://myaiteam-company.vercel.app/')

st.info('This is a separate starter application. No changes have been made to the Vercel website.')

tab1, tab2 = st.tabs(['AI Workflow Runner', 'About'])
with tab1:
    st.subheader('Run an automation')
    st.write('Connect a dedicated n8n webhook to enable this tool. The webhook URL is stored server-side in Streamlit secrets.')
    user_input = st.text_area('Your request', placeholder='Describe what you want the workflow to do', max_chars=5000)
    if st.button('Run workflow', type='primary'):
        try:
            webhook = st.secrets.get('N8N_WEBHOOK_URL', os.getenv('N8N_WEBHOOK_URL', ''))
        except Exception:
            webhook = os.getenv('N8N_WEBHOOK_URL', '')
        if not webhook:
            st.error('Configure N8N_WEBHOOK_URL in Streamlit secrets before running workflows.')
        elif not webhook.startswith('https://'):
            st.error('Webhook URL must use HTTPS.')
        elif not user_input.strip():
            st.warning('Enter a request first.')
        else:
            try:
                response = requests.post(webhook, json={'message': user_input.strip(), 'source': 'myaiteam-streamlit'}, timeout=25)
                response.raise_for_status()
                try:
                    st.json(response.json())
                except ValueError:
                    st.text(response.text[:10000])
            except requests.RequestException:
                st.error('The workflow could not be completed. Check the n8n webhook configuration and logs.')
with tab2:
    st.markdown('**Architecture:** Vercel hosts the main website. Streamlit hosts Python AI tools. n8n runs automations on your existing Oracle Cloud instance.')
    st.warning('Do not configure a webhook that performs privileged actions without adding authentication and abuse protection. Public Streamlit apps can be accessed by anyone.')
