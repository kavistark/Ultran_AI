# scratch/print_header.py
with open(r"c:\Users\MrHat\app\ai_ultran\templates\voice_wave.html", "r", encoding="utf-8") as f:
    text = f.read()

s = text.find('<header class="platform-top-bar"')
e = text.find('</header>', s) + len('</header>')
print("=== NEW HEADER ===")
print(text[s:e])
print("==================")

