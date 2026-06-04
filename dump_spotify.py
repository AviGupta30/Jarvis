import subprocess
import time
from app.services.ui_inspector import debug_ui_tree

print("Opening Spotify search...")
subprocess.Popen('start "" "spotify:search:blinding lights"', shell=True)
time.sleep(3)

print("Dumping UI tree...")
tree = debug_ui_tree('Spotify', depth=5)
with open('spotify_tree.txt', 'w', encoding='utf-8') as f:
    f.write(tree)
print("Saved to spotify_tree.txt")
