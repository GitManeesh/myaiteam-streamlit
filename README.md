# MyAITeam Streamlit AI Tools

A separate Python tool portal for the existing Next.js/Vercel company website. **Does not modify or replace the production website.**

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publish on Streamlit Community Cloud

1. Create a separate GitHub repository and add these files (including `.streamlit/config.toml`).
2. Visit https://share.streamlit.io/ and choose **Create app** from the repository, branch `main`, entrypoint `app.py`.
3. Under **Advanced settings → Secrets**, optionally set `N8N_WEBHOOK_URL = "https://<your-n8n-host>/webhook/<dedicated-path>"` (do not commit real secrets).
4. Deploy, test, and then add the new Streamlit URL to the existing Vercel website when ready.

## Security

The workflow runner is a starter. Do **not** connect it to a privileged or costly webhook in a public deployment without access control, rate limiting, and authorization. Prefer a dedicated least-privilege n8n webhook. Never put API keys in frontend code or Git.

## Hybrid architecture

- Existing website: https://myaiteam-company.vercel.app/
- Streamlit: separately deployed Python AI tools
- Backend: existing n8n instance on Oracle Cloud

No deployment or production changes are performed by this package.
