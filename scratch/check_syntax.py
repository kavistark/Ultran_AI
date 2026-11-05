# scratch/check_syntax.py
import re

VW_PATH = r"c:\Users\MrHat\app\ai_ultran\templates\voice_wave.html"
with open(VW_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Extract script blocks
scripts = re.findall(r"<script>(.*?)</script>", text, re.DOTALL)
print(f"Found {len(scripts)} script block(s)")

for i, script in enumerate(scripts):
    print(f"Script block {i+1} has {len(script)} chars, {script.count(chr(10))} lines")
    # Check brace matching
    stack = []
    lines = script.split('\n')
    for line_idx, line in enumerate(lines, 1):
        for ch_idx, ch in enumerate(line, 1):
            if ch in '{[(':
                stack.append((ch, line_idx, ch_idx))
            elif ch in '}])':
                if not stack:
                    print(f"Unmatched closing '{ch}' at line {line_idx}:{ch_idx}")
                else:
                    top, l_idx, c_idx = stack.pop()
                    match = {'{': '}', '[': ']', '(': ')'}[top]
                    if ch != match:
                        print(f"Mismatched '{ch}' at line {line_idx}:{ch_idx}, expected '{match}' opened at {l_idx}:{c_idx}")
    if stack:
        print(f"Unclosed brackets remaining: {len(stack)} items:")
        for top, l_idx, c_idx in stack[:10]:
            print(f"  Unclosed '{top}' from line {l_idx}:{c_idx}")
    else:
        print("Brackets are 100% balanced and valid!")

