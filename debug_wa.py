import re

text = 'make an whatsapp call to archit shukla'
lower = text.lower()

print("=== Checking keyword_detect_tool whatsapp block ===")
cond = 'whatsapp' in lower or ('send' in lower and ('message' in lower or 'msg' in lower or 'text' in lower) and re.search(r'\bto\b', lower))
print('whatsapp block triggered:', cond)

if cond:
    read_wa = re.search(
        r"(?:read|show|check|open|what(?:'s| are| did| has)|any)\s+(?:my\s+)?(?:whatsapp\s+)?(?:messages?|chats?|msgs?)\s+(?:from|with|of)\s+(.+?)(?:\s*\?|$)",
        lower
    )
    print('read_wa:', read_wa)

    open_wa = re.search(r'\bopen\s+whatsapp\b|\blaunch\s+whatsapp\b|\bstart\s+whatsapp\b', lower)
    print('open_wa:', open_wa)

    send_wa1 = re.search(
        r"(?:send|text|message|msg)\s+(?:a\s+)?(?:message\s+)?(?:to\s+)?(.+?)\s+(?:saying|saying that|that|:)[\s\"'](.+?)[\"']?$",
        lower
    )
    print('send_wa1:', send_wa1)

    send_wa2 = re.search(
        r"(?:send|text|message|msg)\s+(.+?)\s+(?:on|via|using)?\s*(?:whatsapp)?[:\s]+[\"']?(.+?)[\"']?$",
        lower
    )
    print('send_wa2:', send_wa2)

    search_wa = re.search(
        r"(?:find|search|look\s+up|who\s+is)\s+(.+?)\s+(?:on|in)?\s*whatsapp",
        lower
    )
    print('search_wa:', search_wa)
    
    print("\nResult: None returned -> falls to detect_whatsapp_send at line 746")

print("\n=== Checking detect_whatsapp_call ===")
_NON_CONTACTS = {'me', 'a', 'the', 'my', 'him', 'her', 'them', 'someone', 'anybody', 'anyone', 'you', 'it', 'that', 'this', 'message', 'msg', 'text'}

def detect_whatsapp_call(text):
    normalized = text.strip().rstrip('.,!?')
    call_kw = re.search(r'\b(call|audio call|voice call|ring|phone)\b', normalized, re.IGNORECASE)
    if not call_kw:
        print("  call_kw not found -> return None")
        return None
    print(f"  call_kw found: {call_kw.group()}")
    call_patterns = [
        r'(?:make|place|give|do)\s+(?:a\s+)?(?:whatsapp\s+)?(?:call|audio\s+call|voice\s+call)\s+(?:to\s+)?([\w\s\.]+?)(?:\s+on\s+(?:whatsapp|wp))?\s*$',
        r'(?:call|ring|phone)\s+([\w\s\.]+?)\s+(?:on|via|using|through|over)\s+(?:whatsapp|wa|wp)',
        r'(?:whatsapp\s+)?call\s+([\w\s\.]+?)\s+(?:on|via|over)\s+whatsapp',
    ]
    for i, pattern in enumerate(call_patterns):
        m = re.search(pattern, normalized, re.IGNORECASE)
        print(f"  call pattern {i}: {m.group(0) if m else 'no match'}")
        if m:
            return m.group(1).strip()
    return None

result = detect_whatsapp_call(text)
print("detect_whatsapp_call result:", result)

print("\n=== Checking detect_whatsapp_send ===")
def detect_whatsapp_send(text):
    if detect_whatsapp_call(text):
        return None
    normalized = text.strip().rstrip('.,!?')
    patterns = [
        r'send\s+(?:a\s+)?(?:message|msg|text|whatsapp\s+message)\s+to\s+([\w\s\.]+?)(?:\s+on\s+(?:whatsapp|wp)|$)',
        r'message\s+([\w\s\.]+?)\s+on\s+(?:whatsapp|wp)',
        r'whatsapp\s+(?:message\s+(?:to\s+)?|text\s+(?:to\s+)?)?([\\w\\s\\.]+?)(?:\s+saying.*)?$',
        r'send\s+([\w\s\.]+?)\s+a\s+(?:message|msg|text|whatsapp)',
        r'send\s+(?:a\s+)?(?:message|msg|text)(?:\s+to)?\s+([\w\s\.]+?)(?:\s+on\s+(?:whatsapp|wp)|$)',
    ]
    for i, pattern in enumerate(patterns):
        m = re.search(pattern, normalized, re.IGNORECASE)
        if m:
            contact = m.group(1).strip()
            print(f"  send pattern {i} matched: contact={contact}")
            return contact
    return None

result2 = detect_whatsapp_send(text)
print("detect_whatsapp_send result:", result2)

print("\n=== Fix: pattern 0 with 'an?' ===")
p0_fixed = r'(?:make|place|give|do)\s+(?:an?\s+)?(?:whatsapp\s+)?(?:call|audio\s+call|voice\s+call)\s+(?:to\s+)?([\w\s\.]+?)(?:\s+on\s+(?:whatsapp|wp))?\s*$'
m = re.search(p0_fixed, text, re.IGNORECASE)
print("Fixed P0 match:", m)
if m:
    print("Contact:", m.group(1))
