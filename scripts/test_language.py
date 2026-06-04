import sys
sys.path.insert(0, '.')
from app.services.context_classifier import detect_language, classify_context

tests = [
    ('hey jarvis open chrome', 'english'),
    ('open spotify', 'english'),
    ('what is the weather', 'english'),
    ('jarvis yeh file delete karo', 'hindi'),    # 3/4 words Hindi → hindi is correct
    ('kya chal raha hai', 'hindi'),
    ('spotify pe gaana chalao', 'hindi'),
    ('abhi jaldi chrome kholo', 'hindi'),
    ('jarvis open chrome and also search karo', 'hinglish'),  # mixed
]

print('Language Detection Tests:')
all_pass = True
for text, expected in tests:
    result = detect_language(text)
    status = 'PASS' if result == expected else 'FAIL'
    if status == 'FAIL':
        all_pass = False
    print(f'  [{status}] "{text}" -> {result} (expected {expected})')

print()
ctx = classify_context('hey jarvis open chrome')
print(f'English command -> language={ctx["language"]}')
ctx = classify_context('jarvis yeh chrome kholo abhi')
print(f'Hindi command   -> language={ctx["language"]}')

from app.services.personality import get_context_aware_prompt
p_en = get_context_aware_prompt(hour=14, user_mood='neutral', language='english')
p_hi = get_context_aware_prompt(hour=14, user_mood='neutral', language='hindi')
assert 'CLEAN ENGLISH ONLY' in p_en, 'English prompt missing!'
assert 'Devanagari' in p_hi, 'Hindi prompt missing!'
print('Prompt injection: OK')
print()
if all_pass:
    print('ALL TESTS PASSED')
else:
    print('SOME TESTS FAILED')
