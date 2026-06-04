import sys
sys.path.insert(0, '.')
from app.api.chat import keyword_detect_tool

tests = [
    ('open google',             'open_website'),
    ('open chrome',             'open_app'),
    ('open calculator',         'open_app'),
    ('open spotify',            'open_app'),
    ('open vs code',            'open_app'),
    ('open github',             'open_website'),
    ('open whatsapp',           'open_whatsapp'),
    ('play shape of you',       'play_music'),
    ('play shape of you on spotify', 'play_music'),
    ('open youtube',            'open_website'),
    ('open netflix',            'open_website'),
    ('open notepad',            'open_app'),
]

print('Routing Test Results:')
passed = 0
failed = 0
for text, expected in tests:
    result = keyword_detect_tool(text)
    got = result['tool_name'] if result else None
    if got == expected:
        print(f'  [PASS] "{text}" -> {got}')
        passed += 1
    else:
        print(f'  [FAIL] "{text}" -> {got}  (expected {expected})')
        failed += 1

print()
print(f'{passed}/{passed+failed} tests passed')
if failed == 0:
    print('ALL PASS')
