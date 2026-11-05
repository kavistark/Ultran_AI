# scratch/fix_header_and_responsive.py
import re
import os

TEMPLATES_DIR = r"c:\Users\MrHat\app\ai_ultran\templates"
VW_PATH = os.path.join(TEMPLATES_DIR, "voice_wave.html")

print(f"Reading {VW_PATH}...")
with open(VW_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Clean up header: remove all icons, orphan toolbar buttons, and extra </div>
old_header_pattern = re.compile(
    r'<header class="platform-top-bar" id="platformTopBar">.*?</header>',
    re.DOTALL
)

clean_header = """<header class="platform-top-bar" id="platformTopBar">
            <div class="brand-group" onclick="resetCanvasTransform()">
                <div class="brand-text-col">
                    <div class="brand-title" id="platformMainTitle">AI ULTRON // Master Autonomous Core</div>
                    <div class="brand-subtitle"><span class="live-dot"></span> VOICE INTELLIGENCE &bull; DUAL-CORE ONLINE</div>
                </div>
            </div>

            <!-- Top Actions Group (Right - Icon Free) -->
            <div class="top-actions-group">
                <button class="btn-new-simulation" id="btnNewSimulation" onclick="openNewSimulationModal()">
                    New Directive
                </button>
                <button class="dataset-switch-pill" id="btnSwitchPreset" onclick="triggerQuickDiagnostic()" title="Run System Diagnostics">
                    <span id="presetLabelText">Diagnostics</span>
                </button>
                <div class="user-avatar-pill" title="Master Authority: Kavi Stark" onclick="resetCanvasTransform()">
                    <div class="avatar-circle">
                        <span class="avatar-text">KS</span>
                        <span class="online-indicator"></span>
                    </div>
                </div>
            </div>
        </header>"""

if old_header_pattern.search(text):
    text = old_header_pattern.sub(clean_header, text, count=1)
    print("Cleaned up header: removed all header icons and orphan elements.")
else:
    print("Warning: old_header_pattern not found.")

# 2. Fix submitDeckChat to call executeVoiceQuery
old_submit_pattern = re.compile(
    r'function submitDeckChat\(\)\s*\{.*?function toggleVoiceRecognitionFromDeck\(\)\s*\{.*?\}',
    re.DOTALL
)

new_submit_and_mic = """function submitDeckChat() {
            const deckInput = document.getElementById('deckChatInput');
            if (!deckInput) return;
            const text = deckInput.value.trim();
            if (!text) return;

            deckInput.value = '';
            triggerSynapseSurge(2.5);

            const aiBody = document.getElementById('deckAiBody');
            const aiSub = document.getElementById('deckAiSubheading');
            if (aiSub) aiSub.textContent = `Directive: "${text}"`;
            if (aiBody) aiBody.textContent = `Processing directive through Dual-Core Intelligence...`;

            unlockMobileAudioContext();
            activeQueryInFlight = false;
            pauseSpeechCapture();
            executeVoiceQuery(text);
        }

        function toggleVoiceRecognitionFromDeck() {
            unlockMobileAudioContext();
            toggleMicrophoneListening();
            const deckMicBtn = document.getElementById('deckMicBtn');
            if (deckMicBtn) {
                deckMicBtn.classList.toggle('active', isListening);
            }
        }"""

if old_submit_pattern.search(text):
    text = old_submit_pattern.sub(new_submit_and_mic, text, count=1)
    print("Updated submitDeckChat and toggleVoiceRecognitionFromDeck to call executeVoiceQuery & toggleMicrophoneListening.")
else:
    print("Warning: old_submit_pattern not found.")

# 3. Fix triggerQuickDiagnostic and triggerQuickAiAnalysis
old_diag_pattern = re.compile(
    r'function triggerQuickDiagnostic\(\)\s*\{.*?function triggerQuickAiAnalysis\(\)\s*\{.*?\}',
    re.DOTALL
)

new_diag = """function triggerQuickDiagnostic() {
            triggerSynapseSurge(3.0);
            unlockMobileAudioContext();
            activeQueryInFlight = false;
            pauseSpeechCapture();
            executeVoiceQuery('system diagnostics');
        }

        function triggerQuickAiAnalysis() {
            const data = MINDMAP_DATASETS[currentDatasetKey];
            let activeNode = null;
            if (data && data.childNodes) {
                const list = data.childNodes[activeCategoryKey] || [];
                activeNode = list.find(n => n.id === selectedNodeId) || list[0];
            }
            const nodeTitle = activeNode ? activeNode.title : 'system architecture';
            const prompt = `Analyze subsystem status, working process, and operational readiness for: ${nodeTitle}`;
            triggerSynapseSurge(2.5);
            unlockMobileAudioContext();
            activeQueryInFlight = false;
            pauseSpeechCapture();
            executeVoiceQuery(prompt);
        }"""

if old_diag_pattern.search(text):
    text = old_diag_pattern.sub(new_diag, text, count=1)
    print("Updated triggerQuickDiagnostic and triggerQuickAiAnalysis.")
else:
    print("Warning: old_diag_pattern not found.")

# 4. Sync deck mic button in setMicrophoneUI
old_set_mic = "const btn = document.getElementById('agentMicBtn');\n            if (!btn) return;"
new_set_mic = """const btn = document.getElementById('agentMicBtn');
            const deckMic = document.getElementById('deckMicBtn');
            if (deckMic) deckMic.classList.toggle('active', listening);
            if (!btn) return;"""

if old_set_mic in text:
    text = text.replace(old_set_mic, new_set_mic, 1)
    print("Synced deckMicBtn in setMicrophoneUI.")

# 5. Fix safe initialization of mindmap (handling document.readyState)
old_dom_init = re.compile(
    r'// Initialize on DOMContentLoaded\s*document\.addEventListener\(\'DOMContentLoaded\',\s*\(\)\s*=>\s*\{\s*initNeuralMindmap\(\);\s*\}\);',
    re.DOTALL
)

new_dom_init = """// Safe Auto-Initialization
        function safeInitNeuralMindmap() {
            try {
                initNeuralMindmap();
            } catch(e) {
                console.warn('Neural Mindmap initialization notice:', e);
            }
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', safeInitNeuralMindmap);
        } else {
            safeInitNeuralMindmap();
        }
        window.addEventListener('load', () => {
            setTimeout(safeInitNeuralMindmap, 100);
        });"""

if old_dom_init.search(text):
    text = old_dom_init.sub(new_dom_init, text, count=1)
    print("Updated DOMContentLoaded to safeInitNeuralMindmap.")
else:
    print("Warning: old_dom_init pattern not found.")

with open(VW_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved voice_wave.html successfully!")

