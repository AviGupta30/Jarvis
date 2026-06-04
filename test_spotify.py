import subprocess, time, pyautogui, pygetwindow as gw
subprocess.Popen('start "" "spotify:search:blinding lights"', shell=True)
time.sleep(3)
wins = [w for w in gw.getAllWindows() if w.title and 'spotify' in w.title.lower()]
if wins:
    wins[0].activate()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)
    # Tab to the Play button (Top Result)
    for _ in range(4):
        pyautogui.press('tab')
        time.sleep(0.2)
    pyautogui.press('enter')
    print('Tabs sent')
