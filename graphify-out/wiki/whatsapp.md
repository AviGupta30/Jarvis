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

- [message_reader + reply_generator](message_reader_+_reply_generator.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)

## Source Files

- `app/services/whatsapp.py`

## Audit Trail

- EXTRACTED: 10 (91%)
- INFERRED: 1 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*