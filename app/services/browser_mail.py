"""
browser_mail.py — Standard Browser Mail Automation
-----------------------------------------------
Uses the user's default browser and URL parameters to open Gmail natively.
This avoids all bot protection/login blocks from Google since it uses their existing active browser session.
"""

import os
import json
import urllib.parse
import webbrowser
from pathlib import Path

def _get_api_key():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        try:
            import sys
            _PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
            if str(_PROJECT_ROOT) not in sys.path:
                sys.path.insert(0, str(_PROJECT_ROOT))
            from app.core.config import settings
            api_key = settings.GROQ_API_KEY
        except Exception:
            pass
    return api_key

def check_emails(query: str = "is:unread", max_results: int = 5) -> str:
    encoded_query = urllib.parse.quote(query)
    url = f"https://mail.google.com/mail/u/0/#search/{encoded_query}"
    webbrowser.open(url)
    return f"Opened Gmail with search query: {query}"

def list_unread(max_results: int = 5) -> str:
    return check_emails("is:unread label:inbox", max_results)

def get_email_body(email_id: str) -> str:
    return "To read emails, please ask me to search for them or open your inbox."

def summarize_inbox(max_results: int = 10) -> str:
    webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
    return "Opened your Gmail inbox."

def smart_mail_action(task: str) -> str:
    """A generic tool to perform any mail task (like sending or reading) by pre-filling URLs."""
    task_lower = task.lower()
    
    if "send" in task_lower or "compose" in task_lower or "write" in task_lower or "email to" in task_lower:
        api_key = _get_api_key()
        if not api_key:
            webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1")
            return "Opened Gmail compose window."
            
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            prompt = f"Extract email fields from this task: '{task}'. Return ONLY JSON format: {{\"to\": \"...\", \"subject\": \"...\", \"body\": \"...\"}}. If a field is not specified, leave it empty."
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            fields = json.loads(resp.choices[0].message.content)
            
            to = urllib.parse.quote(fields.get("to", ""))
            su = urllib.parse.quote(fields.get("subject", ""))
            body = urllib.parse.quote(fields.get("body", ""))
            
            url = f"https://mail.google.com/mail/?view=cm&fs=1&to={to}&su={su}&body={body}"
            webbrowser.open(url)
            return f"Opened Gmail compose window pre-filled for task: {task}"
        except Exception as e:
            webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1")
            return f"Opened Gmail compose window (could not pre-fill due to LLM error: {e})."
    else:
        api_key = _get_api_key()
        if not api_key:
            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
            return "Opened your Gmail inbox."
            
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            prompt = f"Extract the Gmail search query from this task: '{task}'. Return ONLY the raw search query string (e.g. 'from:boss', 'is:unread', 'meeting'). If unclear, just return 'is:unread'."
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            query = resp.choices[0].message.content.strip().strip("'\"")
            
            encoded_query = urllib.parse.quote(query)
            url = f"https://mail.google.com/mail/u/0/#search/{encoded_query}"
            webbrowser.open(url)
            return f"Opened Gmail searching for: {query}"
        except Exception as e:
            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
            return "Opened your Gmail inbox."
