# scratch/generate_neural_ui.py
import os
import sys

TEMPLATES_DIR = r"c:\Users\MrHat\app\ai_ultran\templates"
VW_PATH = os.path.join(TEMPLATES_DIR, "voice_wave.html")

with open(VW_PATH, "r", encoding="utf-8") as f:
    orig = f.read()

# Verify markers
style_end_marker = "</style>"
if style_end_marker not in orig:
    print("Error: </style> not found")
    sys.exit(1)

body_start_marker = '<body class="state-idle" id="stageBody" onclick="handleStageTap()">'
if body_start_marker not in orig:
    # check fallback
    body_start_marker = "<body"

print("Markers located.")

