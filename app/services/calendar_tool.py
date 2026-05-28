"""
calendar_tool.py — Jarvis Google Calendar Integration (Step 8)
--------------------------------------------------
Completely isolated module. Uses Google Calendar API with OAuth2.

ONE-TIME SETUP:
  Uses the same `credentials.json` from the Gmail step!
  It will create a separate `calendar_token.json` on first run to avoid scope conflicts.
"""

import os
import datetime
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_CREDS_PATH   = _PROJECT_ROOT / "credentials.json"
_TOKEN_PATH   = _PROJECT_ROOT / "calendar_token.json"

_SCOPES = ["https://www.googleapis.com/auth/calendar"]

# ── Auth Helper ────────────────────────────────────────────────────────────────

def _get_calendar_service():
    """Authenticate and return a Google Calendar API service object."""
    if not _CREDS_PATH.exists():
        raise FileNotFoundError("credentials.json not found. Please set it up as described in the Gmail step.")

    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if _TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(_TOKEN_PATH), _SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(_CREDS_PATH), _SCOPES)
            creds = flow.run_local_server(port=0)
        _TOKEN_PATH.write_text(creds.to_json())

    return build("calendar", "v3", credentials=creds)

# ── Public Functions ───────────────────────────────────────────────────────────

def get_upcoming_events(days: int = 7) -> str:
    """List events in the next N days."""
    try:
        service = _get_calendar_service()
        
        now = datetime.datetime.utcnow()
        time_min = now.isoformat() + 'Z'  # 'Z' indicates UTC time
        time_max = (now + datetime.timedelta(days=days)).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId='primary', timeMin=time_min, timeMax=time_max,
            singleEvents=True, orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])

        if not events:
            return f"No upcoming events found in the next {days} days."

        lines = [f"Upcoming events for the next {days} days:\n"]
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            
            # Make dates readable
            try:
                dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                start_readable = dt.strftime('%a, %d %b at %I:%M %p')
            except ValueError:
                start_readable = start
                
            summary = event.get('summary', 'No Title').encode("ascii", "ignore").decode("ascii")
            lines.append(f"- {start_readable}: {summary}")
            
        return "\n".join(lines)
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Calendar error: {e}"


def check_today_schedule() -> str:
    """What's on today's agenda, with time remaining until each event."""
    try:
        service = _get_calendar_service()
        now = datetime.datetime.utcnow()
        time_min = now.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
        time_max = now.replace(hour=23, minute=59, second=59).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId='primary', timeMin=time_min, timeMax=time_max,
            singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            return "You have nothing scheduled for today."

        lines = [f"Today's schedule ({len(events)} event(s)):\n"]
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            try:
                dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                start_readable = dt.strftime('%I:%M %p')

                # Time remaining calculation
                diff = dt.replace(tzinfo=None) - now
                total_minutes = int(diff.total_seconds() / 60)
                if total_minutes < 0:
                    time_remaining = "(already started)"
                elif total_minutes < 60:
                    time_remaining = f"in {total_minutes} minute(s)"
                else:
                    time_remaining = f"in {total_minutes // 60}h {total_minutes % 60}m"
            except Exception:
                start_readable = start
                time_remaining = ""

            summary = event.get('summary', 'No Title').encode("ascii", "ignore").decode("ascii")
            lines.append(f"  ⏰ {start_readable} — {summary} ({time_remaining})")

        return "\n".join(lines)
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Calendar error: {e}"


def add_event(title: str, date: str, time: str = None, notes: str = "") -> str:
    """
    Create a new event in Google Calendar.
    - title: "Project Meeting"
    - date: "YYYY-MM-DD", "today", "tomorrow", or natural language like "next Friday"
    - time: "HH:MM" (24-hour) or None for all-day event
    - notes: Description for the event
    """
    try:
        service = _get_calendar_service()

        now = datetime.datetime.now()

        # ── Natural date parsing ──────────────────────────────────────────────────
        if date.lower() == "today":
            target_date = now.date()
        elif date.lower() == "tomorrow":
            target_date = (now + datetime.timedelta(days=1)).date()
        else:
            # Try YYYY-MM-DD first
            try:
                target_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                # Fall back to natural language parsing
                try:
                    import dateparser
                    parsed = dateparser.parse(date, settings={"PREFER_DATES_FROM": "future"})
                    if not parsed:
                        return f"Could not understand the date: '{date}'. Try 'YYYY-MM-DD', 'today', 'tomorrow', or 'next Monday'."
                    target_date = parsed.date()
                except ImportError:
                    return f"Invalid date format: '{date}'. Please use YYYY-MM-DD, 'today', or 'tomorrow'."

        event_body = {
            'summary': title,
            'description': notes,
        }

        if time:
            try:
                target_time = datetime.datetime.strptime(time, "%H:%M").time()
            except ValueError:
                # Try 12-hour format too
                try:
                    target_time = datetime.datetime.strptime(time, "%I:%M %p").time()
                except ValueError:
                    return f"Invalid time format: '{time}'. Use HH:MM (24-hour) or HH:MM AM/PM."

            start_dt = datetime.datetime.combine(target_date, target_time)
            end_dt = start_dt + datetime.timedelta(hours=1)

            # ── Conflict detection ─────────────────────────────────────────────────
            conflict_warning = ""
            try:
                conflict_check = service.events().list(
                    calendarId='primary',
                    timeMin=start_dt.isoformat() + 'Z',
                    timeMax=end_dt.isoformat() + 'Z',
                    singleEvents=True
                ).execute()
                conflicts = conflict_check.get('items', [])
                if conflicts:
                    conflict_title = conflicts[0].get('summary', 'another event')
                    conflict_warning = f" ⚠️ Note: You already have '{conflict_title}' at that time."
            except Exception:
                pass

            event_body['start'] = {'dateTime': start_dt.isoformat(), 'timeZone': 'UTC'}
            event_body['end'] = {'dateTime': end_dt.isoformat(), 'timeZone': 'UTC'}
        else:
            event_body['start'] = {'date': target_date.isoformat()}
            event_body['end'] = {'date': (target_date + datetime.timedelta(days=1)).isoformat()}
            conflict_warning = ""

        event = service.events().insert(calendarId='primary', body=event_body).execute()
        time_str = f" at {time}" if time else " (all day)"
        return f"Added '{title}' on {target_date}{time_str}.{conflict_warning}"

    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Calendar error: {e}"
