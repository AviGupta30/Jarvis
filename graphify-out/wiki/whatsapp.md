# whatsapp

> 6 nodes · cohesion 0.33

## Key Concepts

- **send_whatsapp_message()** (5 connections) — `app/services/whatsapp.py`
- **_focus_or_open_whatsapp()** (4 connections) — `app/services/whatsapp.py`
- **open_whatsapp()** (4 connections) — `app/services/whatsapp.py`
- **Focus the WhatsApp window or open it if not running. Returns True on success.** (1 connections) — `app/services/whatsapp.py`
- **Opens the WhatsApp desktop app.** (1 connections) — `app/services/whatsapp.py`
- **Sends a WhatsApp message using the Windows desktop app via keyboard automation.…** (1 connections) — `app/services/whatsapp.py`

## Relationships

- [whatsapp_call + dump_wa_ui](whatsapp_call_+_dump_wa_ui.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (1 shared connections)

## Source Files

- `app/services/whatsapp.py`

## Audit Trail

- EXTRACTED: 10 (91%)
- INFERRED: 1 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*