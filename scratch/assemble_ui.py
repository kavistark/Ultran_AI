# scratch/assemble_ui.py
import os
import sys

TEMPLATES_DIR = r"c:\Users\MrHat\app\ai_ultran\templates"
VW_PATH = os.path.join(TEMPLATES_DIR, "voice_wave.html")

with open(VW_PATH, "r", encoding="utf-8") as f:
    orig = f.read()

# Let's inspect CSS insertion point
style_end_idx = orig.find("</style>")
if style_end_idx == -1:
    print("Error: </style> not found")
    sys.exit(1)

print(f"</style> found at index {style_end_idx}")

# Let's inspect where stage elements start
# Earlier we saw:
# <body class="state-idle" id="stageBody" onclick="handleStageTap()">
# We want to replace the old top-voice-bar, voice-entity-stage, etc.
body_tag_idx = orig.find("<body")
print(f"<body found at index {body_tag_idx}")
