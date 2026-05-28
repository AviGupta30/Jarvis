"""
gmail_tool.py — Jarvis Gmail Integration (Step 5)
--------------------------------------------------
Completely isolated module. Uses Gmail API with OAuth2.

ONE-TIME SETUP (done by user, not code):
  1. Go to https://console.cloud.google.com
  2. Create project → Enable Gmail API
  3. Credentials → Create OAuth2 client ID (Desktop App)
  4. Download → save as 'credentials.json' in Jarvis project root
  5. First run: browser opens, you click Allow → token.json auto-saved
  6. All future runs: fully automatic, no re-login needed.

Public API:
  check_emails(query, max_results=5)  → str   search inbox by keyword/sender
  list_unread(max_results=5)          → str   list unread emails with preview
  get_email_body(email_id)            → str   read full email body
  summarize_inbox(max_results=10)     → str   quick overview of recent emails
"""

import os
import base64
import json
import re
from pathlib import Path
from datetime import datetime

# ── Paths ─────────────────────────────────────────────────────────────────────

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_CREDS_PATH   = _PROJECT_ROOT / "credentials.json"
_TOKEN_PATH   = _PROJECT_ROOT / "token.json"

# Gmail API scopes — read-only is sufficient for Jarvis
_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# ── Auth Helper ────────────────────────────────────────────────────────────────

def _get_gmail_service():
    """
    Authenticate and return a Gmail API service object.
    Handles first-time OAuth flow and token refresh automatically.
    Raises FileNotFoundError if credentials.json is missing.
    """
    if not _CREDS_PATH.exists():
        raise FileNotFoundError(
            f"credentials.json not found at '{_CREDS_PATH}'.\n"
            "To set up Gmail integration:\n"
            "  1. Go to https://console.cloud.google.com\n"
            "  2. Enable Gmail API for your project\n"
            "  3. Create OAuth2 credentials (Desktop App)\n"
            "  4. Download and rename the file to 'credentials.json'\n"
            "  5. Place it in the Jarvis project root folder\n"
            "  6. Run Jarvis again — a browser window will open for you to allow access."
        )

    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None

    # Load existing token
    if _TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(_TOKEN_PATH), _SCOPES)

    # Refresh or re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(_CREDS_PATH), _SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the token for next time
        _TOKEN_PATH.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)


# ── Text Extraction Helpers ────────────────────────────────────────────────────

def _decode_body(payload: dict) -> str:
    """Recursively extract readable text from an email payload."""
    body = ""
    if "body" in payload and payload["body"].get("data"):
        raw = payload["body"]["data"]
        body = base64.urlsafe_b64decode(raw + "==").decode("utf-8", errors="replace")
    elif "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") in ("text/plain", "text/html"):
                data = part.get("body", {}).get("data", "")
                if data:
                    decoded = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="replace")
                    # Remove characters that cause UnicodeEncodeError on Windows terminals (like emojis/hourglass)
                    decoded = decoded.encode("ascii", "ignore").decode("ascii")
                    if part["mimeType"] == "text/plain":
                        body += decoded
                    elif not body:  # Use HTML as fallback if no plain text
                        # Strip HTML tags for readable output
                        decoded = re.sub(r"<[^>]+>", "", decoded)
                        body += decoded
            elif "parts" in part:
                body += _decode_body(part)
    return body.strip()


def _get_header(headers: list, name: str) -> str:
    """Extract a specific header value by name."""
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def _format_date(date_str: str) -> str:
    """Convert raw email date string to a clean readable format."""
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_str)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return date_str


def _truncate(text: str, max_len: int = 300) -> str:
    """Truncate text to a max length with ellipsis."""
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


# ── Public Functions ───────────────────────────────────────────────────────────

def check_emails(query: str = "is:unread", max_results: int = 5) -> str:
    """
    Search Gmail inbox by keyword, sender, label, or status.
    Examples:
      check_emails("internship")            → emails about internships
      check_emails("from:college@edu.in")   → emails from your college
      check_emails("is:unread")             → all unread emails
      check_emails("subject:offer letter")  → emails with that subject
    """
    try:
        service = _get_gmail_service()

        result = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()

        messages = result.get("messages", [])
        if not messages:
            return f"No emails found for: '{query}'."

        lines = [f"Found {len(messages)} email(s) for '{query}':\n"]
        for i, msg in enumerate(messages, 1):
            detail = service.users().messages().get(
                userId="me", id=msg["id"], format="metadata",
                metadataHeaders=["From", "Subject", "Date"]
            ).execute()

            headers = detail.get("payload", {}).get("headers", [])
            sender  = _get_header(headers, "From")
            subject = _get_header(headers, "Subject") or "(No subject)"
            subject = subject.encode("ascii", "ignore").decode("ascii")
            date    = _format_date(_get_header(headers, "Date"))

            # Quick snippet preview
            snippet = detail.get("snippet", "")
            snippet = snippet.encode("ascii", "ignore").decode("ascii")
            snippet = _truncate(snippet, 120)

            lines.append(f"{i}. From:    {sender}")
            lines.append(f"   Subject: {subject}")
            lines.append(f"   Date:    {date}")
            lines.append(f"   Preview: {snippet}")
            lines.append("")

        return "\n".join(lines)

    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Gmail error: {e}"


def list_unread(max_results: int = 5) -> str:
    """List unread emails with priority triage and LLM one-line summaries."""
    try:
        service = _get_gmail_service()
        result = service.users().messages().list(
            userId="me", q="is:unread label:inbox", maxResults=max_results
        ).execute()
        messages = result.get("messages", [])
        if not messages:
            return "You have no unread emails."

        # Priority keywords
        high_priority_kw = [
            "offer", "interview", "internship", "result", "admit", "rejection",
            "selected", "shortlisted", "urgent", "action required", "deadline",
            "payment", "invoice", "verify", "otp", "password reset"
        ]

        lines = [f"You have {len(messages)} unread email(s):\n"]
        email_bodies_for_llm = []

        for i, msg in enumerate(messages, 1):
            detail = service.users().messages().get(
                userId="me", id=msg["id"], format="metadata",
                metadataHeaders=["From", "Subject", "Date"]
            ).execute()
            headers = detail.get("payload", {}).get("headers", [])
            sender  = _get_header(headers, "From")
            subject = _get_header(headers, "Subject") or "(No subject)"
            subject = subject.encode("ascii", "ignore").decode("ascii")
            date    = _format_date(_get_header(headers, "Date"))
            snippet = detail.get("snippet", "").encode("ascii", "ignore").decode("ascii")

            # Priority triage
            combined = (subject + " " + snippet).lower()
            priority = "🔴 HIGH" if any(kw in combined for kw in high_priority_kw) else "⚪ NORMAL"

            email_bodies_for_llm.append(f"Subject: {subject}\nFrom: {sender}\nPreview: {snippet[:200]}")

            lines.append(f"{i}. [{priority}] {subject}")
            lines.append(f"   From: {sender}  |  {date}")
            lines.append("")

        # LLM one-line summary for top 3 emails
        try:
            from groq import Groq
            from app.core.config import settings
            client = Groq(api_key=settings.GROQ_API_KEY)
            email_text = "\n\n".join(email_bodies_for_llm[:3])
            prompt = (
                f"Summarize each of these emails in one short sentence each. "
                f"Number them 1, 2, 3.\n\n{email_text}"
            )
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.2
            )
            summaries = resp.choices[0].message.content.strip()
            lines.append("\nQuick summaries of top emails:")
            lines.append(summaries)
        except Exception:
            pass

        return "\n".join(lines)

    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Gmail error: {e}"


def get_email_body(email_id: str) -> str:
    """
    Read the full body of a specific email by its ID.
    email_id is the numeric Gmail message ID shown in check_emails results.
    """
    try:
        service = _get_gmail_service()
        msg = service.users().messages().get(
            userId="me", id=email_id, format="full"
        ).execute()

        headers  = msg.get("payload", {}).get("headers", [])
        sender   = _get_header(headers, "From")
        subject  = _get_header(headers, "Subject") or "(No subject)"
        subject = subject.encode("ascii", "ignore").decode("ascii")
        date     = _format_date(_get_header(headers, "Date"))
        body     = _decode_body(msg.get("payload", {}))

        if not body:
            body = "(Could not extract email body — may be an image-only email)"

        return (
            f"From:    {sender}\n"
            f"Subject: {subject}\n"
            f"Date:    {date}\n"
            f"---\n"
            f"{body[:3000]}"
        )

    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Gmail error: {e}"


def summarize_inbox(max_results: int = 10) -> str:
    """
    Get a quick summary of the most recent emails in the inbox.
    Returns sender and subject for each email — great for a morning briefing.
    """
    try:
        service = _get_gmail_service()

        result = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            maxResults=max_results
        ).execute()

        messages = result.get("messages", [])
        if not messages:
            return "Your inbox appears to be empty."

        unread_result = service.users().messages().list(
            userId="me", q="is:unread label:inbox", maxResults=1
        ).execute()
        unread_est = unread_result.get("resultSizeEstimate", 0)

        lines = [f"Inbox summary — {len(messages)} recent emails, ~{unread_est} unread:\n"]
        for i, msg in enumerate(messages, 1):
            detail = service.users().messages().get(
                userId="me", id=msg["id"], format="metadata",
                metadataHeaders=["From", "Subject", "Date"]
            ).execute()
            headers = detail.get("payload", {}).get("headers", [])
            sender  = _get_header(headers, "From")
            subject = _get_header(headers, "Subject") or "(No subject)"
            subject = subject.encode("ascii", "ignore").decode("ascii")
            date    = _format_date(_get_header(headers, "Date"))
            is_unread = "UNREAD" in detail.get("labelIds", [])
            mark = "[UNREAD] " if is_unread else "         "
            lines.append(f"{i:2}. {mark}{subject}")
            lines.append(f"    From: {sender}  |  {date}")
        return "\n".join(lines)

    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Gmail error: {e}"
