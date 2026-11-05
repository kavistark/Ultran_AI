# scratch/remove_toolbar.py
import re
import os

TEMPLATES_DIR = r"c:\Users\MrHat\app\ai_ultran\templates"
VW_PATH = os.path.join(TEMPLATES_DIR, "voice_wave.html")

print(f"Reading {VW_PATH}...")
with open(VW_PATH, "r", encoding="utf-8") as f:
    text = f.read()

pattern = re.compile(
    r'\s*<!-- Floating Dark Glass Toolbar \(Center\) -->\s*<div class="floating-toolbar" id="canvasToolbar">.*?</div>',
    re.DOTALL
)

match = pattern.search(text)
if match:
    text = pattern.sub('', text, count=1)
    with open(VW_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("canvasToolbar removed successfully!")
else:
    print("Error: canvasToolbar pattern not found.")
    import sys
    sys.exit(1)

