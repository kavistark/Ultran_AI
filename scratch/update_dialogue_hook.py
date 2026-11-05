# scratch/update_dialogue_hook.py
VW_PATH = r"c:\Users\MrHat\app\ai_ultran\templates\voice_wave.html"
with open(VW_PATH, "r", encoding="utf-8") as f:
    text = f.read()

target = '            hud.scrollTop = hud.scrollHeight;'
addition = """
            const deckAiBody = document.getElementById('deckAiBody');
            const deckAiSub = document.getElementById('deckAiSubheading');
            if (userText && deckAiSub) {
                deckAiSub.textContent = `User Directive: "${userText}"`;
            }
            if (assistantText && deckAiBody) {
                deckAiBody.textContent = assistantText;
                if (typeof triggerSynapseSurge === 'function') triggerSynapseSurge(2.5);
            }
            hud.scrollTop = hud.scrollHeight;"""

if target in text:
    text = text.replace(target, addition, 1)
    with open(VW_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated showDialogueResponse successfully!")
else:
    print("Target not found")

