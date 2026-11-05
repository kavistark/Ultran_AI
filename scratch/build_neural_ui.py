# scratch/build_neural_ui.py
import re
import os

TEMPLATES_DIR = r"c:\Users\MrHat\app\ai_ultran\templates"
VW_PATH = os.path.join(TEMPLATES_DIR, "voice_wave.html")

print(f"Reading {VW_PATH}...")
with open(VW_PATH, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Original file length: {len(content)} chars, {content.count(chr(10))} lines")

