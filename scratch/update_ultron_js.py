# scratch/update_ultron_js.py
import re
import os

TEMPLATES_DIR = r"c:\Users\MrHat\app\ai_ultran\templates"
VW_PATH = os.path.join(TEMPLATES_DIR, "voice_wave.html")

print(f"Reading {VW_PATH}...")
with open(VW_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Let's locate the MINDMAP_DATASETS block
start_marker = "const MINDMAP_DATASETS = {"
end_marker = "let currentDatasetKey = 'policy';"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Error: Could not locate MINDMAP_DATASETS boundaries.")
    import sys
    sys.exit(1)

new_js_datasets = """const MINDMAP_DATASETS = {
            ultronVoice: {
                platformTitle: 'AI ULTRON // Master Autonomous Core',
                breadcrumb: 'Active Pipeline: Acoustic Input ➔ Dual-Core Cognitive Matrix ➔ Device Automation & Cellular Call Gateway',
                root: {
                    id: 'root',
                    title: 'AI ULTRON PRIME',
                    subtitle: 'AUTONOMOUS VOICE CORE',
                    status: 'SAFE: ARMED',
                    statusDot: 'green',
                    domain: 'Autonomous Voice OS & Master Brain',
                    analysis: 'Ultron Prime acts as an always-on sovereign voice intelligence agent for Kavi Stark. Operating with dual-core LLM reasoning (Gemini 3 + Claude 3.5), it coordinates workstation RPA, low-power microphone standby, optical computer vision, and outbound cellular reminder calls.'
                },
                categories: [
                    { id: 'receptors', count: 18, label: 'Voice Receptors', icon: 'fas fa-microphone', domain: 'Stage 1: Acoustic Input' },
                    { id: 'cognition', count: 32, label: 'Cognitive Cores', icon: 'fas fa-brain', domain: 'Stage 2: LLM & Memory' },
                    { id: 'automation', count: 24, label: 'Device Automations', icon: 'fas fa-bolt', active: true, domain: 'Stage 3: RPA & Tools' },
                    { id: 'telephony', count: 12, label: 'Telephony & Calls', icon: 'fas fa-phone-volume', domain: 'Stage 4: Proactive Alerts' },
                    { id: 'synthesis', count: 14, label: 'Voice Synthesis', icon: 'fas fa-waveform-lines', domain: 'Stage 5: Acoustic Emitter' }
                ],
                childNodes: {
                    automation: [
                        { id: 'u1', title: 'Workstation Battery & Power Sentinel', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Power Subsystem', sentiment: 98, delta: '+2% Nominal', complaints: 0, regulations: 1, services: 18, entities: 2, analysis: 'Continuously monitors laptop battery level, AC charging status, and CPU throttle profiles. Automatically engages low-power standby mode when on battery.' },
                        { id: 'u2', title: 'Cellular Phone Call Dispatcher (+91 9092117397)', statusText: 'ARMED:AUTO', status: 'disputed', dot: 'red', domain: 'Telephony Gateway', sentiment: 95, delta: 'Armed & Ready', complaints: 12, regulations: 1, services: 8, entities: 2, selected: true, analysis: 'Core working process escalation: When a scheduled reminder or urgent directive is due and remains unacknowledged for 5 minutes, Ultron automatically initiates a cellular phone call to Kavi Stark to deliver the alert by voice.' },
                        { id: 'u3', title: 'Google Gemini 3 Flash-Lite Primary Engine', statusText: 'ONLINE', status: 'safe', dot: 'green', domain: 'Primary Neural Core', sentiment: 99, delta: '24ms Latency', complaints: 0, regulations: 2, services: 24, entities: 4, analysis: 'Google Gemini Flash-Lite neural core delivering high-speed conversational understanding, JSON tool parsing, and multimodal context processing.' },
                        { id: 'u4', title: 'Anthropic Claude 3.5 Sonnet Cognitive Matrix', statusText: 'STANDBY', status: 'safe', dot: 'green', domain: 'Fallback Cognitive Core', sentiment: 97, delta: 'Dual-Core Armed', complaints: 0, regulations: 1, services: 14, entities: 2, analysis: 'Anthropic Claude 3.5 Sonnet secondary intelligence providing zero-latency fallback reasoning whenever network or model conditions demand.' },
                        { id: 'u5', title: 'Christopher Deep Neural Voice Synthesizer (-14Hz)', statusText: 'ACTIVE', status: 'safe', dot: 'green', domain: 'Acoustic Synthesizer', sentiment: 98, delta: 'Resonant Deep', complaints: 0, regulations: 1, services: 12, entities: 2, analysis: 'Edge-TTS Christopher deep synthetic voice engine calibrated to -14Hz pitch and -8% cadence, backed by offline SAPI5 pyttsx3 chest resonance.' },
                        { id: 'u6', title: 'Optical Screen Inspector & Frame Grabber', statusText: 'READY', status: 'safe', dot: 'green', domain: 'Computer Vision', sentiment: 94, delta: '1080p Optical', complaints: 1, regulations: 1, services: 10, entities: 2, analysis: 'Captures and analyzes workstation display or camera stream to extract tables, text, and visual context for live multimodal Q&A.' },
                        { id: 'u7', title: 'Windows 10 Host Shell RPA Automation Gateway', statusText: 'ACTIVE', status: 'safe', dot: 'green', domain: 'Host RPA Controller', sentiment: 96, delta: 'Root Authority', complaints: 0, regulations: 1, services: 20, entities: 1, analysis: 'Executes native system commands, launches applications, inspects storage volumes, and automates desktop workflows.' },
                        { id: 'u8', title: 'Acoustic Noise Gate & Wake-Word Receptor', statusText: 'LISTENING', status: 'safe', dot: 'green', domain: 'Audio Input Pipeline', sentiment: 93, delta: 'Low-Latency', complaints: 0, regulations: 1, services: 8, entities: 2, analysis: 'Performs spectral gating and noise floor suppression to reliably capture speech from Kavi Stark even in noisy environments.' },
                        { id: 'u9', title: 'Autonomous Scheduled Reminder Daemon (4s Keepalive)', statusText: 'ACTIVE', status: 'safe', dot: 'green', domain: 'Background Sentinel', sentiment: 100, delta: 'Continuous Keepalive', complaints: 0, regulations: 1, services: 16, entities: 2, analysis: 'Background worker running continuously every 4 seconds to inspect scheduled deadlines and trigger acoustic chimes and telephony calls.' },
                        { id: 'u10', title: 'Microphone Standby Low-Power Sentinel', statusText: 'STANDBY', status: 'safe', dot: 'orange', domain: 'Standby Audio', sentiment: 91, delta: 'Standby Ready', complaints: 0, regulations: 1, services: 6, entities: 1, analysis: 'Maintains low-power microphone listening channel while workstation or phone is locked so Ultron is reachable instantly.' },
                        { id: 'u11', title: 'Master Authority Validator: Kavi Stark', statusText: 'SECURE:SUPREME', status: 'safe', dot: 'green', domain: 'Authority Protocol', sentiment: 100, delta: 'Absolute Master', complaints: 0, regulations: 1, services: 30, entities: 1, analysis: 'Enforces root creator hierarchy: Kavi Stark is the supreme master. Ultron yields to no other user or system override.' },
                        { id: 'u12', title: 'Camera Vision Multimodal Frame Analyzer', statusText: 'ONLINE', status: 'safe', dot: 'green', domain: 'Multimodal Vision', sentiment: 92, delta: 'Optical Sensor', complaints: 0, regulations: 1, services: 7, entities: 1, analysis: 'Connects to workstation webcam and mobile camera feeds for environment awareness: "What is on my desk?", document OCR, and room monitoring.' },
                        { id: 'u13', title: 'System Storage Diagnostics (17.8 GB Free of 237.4 GB)', statusText: 'NOMINAL', status: 'safe', dot: 'green', domain: 'System Telemetry', sentiment: 95, delta: 'Storage Healthy', complaints: 0, regulations: 1, services: 12, entities: 1, analysis: 'Polled live telemetry confirming healthy host drive storage, CPU temperatures, and memory consumption.' },
                        { id: 'u14', title: 'Edge-TTS Neural Cadence Compensator (-8%)', statusText: 'TUNED', status: 'safe', dot: 'green', domain: 'Prosody Controller', sentiment: 97, delta: 'Calibrated', complaints: 0, regulations: 1, services: 8, entities: 2, analysis: 'Paces synthesized speech cadence for an articulate, ruthless, and highly authoritative vocal delivery.' },
                        { id: 'u15', title: 'Browser Satellite Automation (Google / YouTube / GitHub)', statusText: 'READY', status: 'safe', dot: 'green', domain: 'Browser Controller', sentiment: 96, delta: 'Satellite Ready', complaints: 0, regulations: 1, services: 15, entities: 3, analysis: 'Directly opens search queries, developer documentation, and multimedia pipelines upon spoken directive.' },
                        { id: 'u16', title: 'Local Context & Persistent Memory Store', statusText: 'SYNCED', status: 'safe', dot: 'green', domain: 'Context Memory', sentiment: 99, delta: 'Persistent SQLite', complaints: 0, regulations: 1, services: 22, entities: 1, analysis: 'Preserves conversational history, active reminders, user preferences, and hardware telemetry across sessions.' },
                        { id: 'u17', title: 'Urgent Reminder Escalation Protocol (Voice + Outbound Call)', statusText: 'ACTIVE:ARMED', status: 'disputed', dot: 'red', domain: 'Proactive Alert Pipeline', sentiment: 89, delta: 'Armed & Ready', complaints: 12, regulations: 2, services: 18, entities: 4, analysis: 'Complete proactive workflow: 1. Acoustic chime sounds on due time. 2. Spoken reminder announced via Christopher TTS. 3. If unacknowledged within 5 minutes, outbound cellular call placed to +91 9092117397.' }
                    ],
                    receptors: [
                        { id: 'r1', title: 'Acoustic Primary Microphone Ingest', statusText: 'LISTENING', status: 'safe', dot: 'green', domain: 'Acoustic Ingest', sentiment: 96, delta: '48kHz Audio', complaints: 0, regulations: 1, services: 12, entities: 1, analysis: 'Real-time Web Audio API stream capturing high-fidelity voice frequencies.' },
                        { id: 'r2', title: 'Web Speech API Streaming Transcriber', statusText: 'ONLINE', status: 'safe', dot: 'green', domain: 'Speech-to-Text', sentiment: 98, delta: 'Continuous STT', complaints: 0, regulations: 1, services: 16, entities: 2, analysis: 'Converts continuous voice audio into live transcripts with instant auto-restart.' },
                        { id: 'r3', title: 'Low-Power Wake-Word Detection Sentinel', statusText: 'ACTIVE', status: 'safe', dot: 'green', domain: 'Wake-Word Engine', sentiment: 94, delta: 'Keyword Sentinel', complaints: 0, regulations: 1, services: 8, entities: 1, analysis: 'Detects "Ultron" or taps to immediately arm receptors from idle or locked screen state.' },
                        { id: 'r4', title: 'Real-Time Audio Frequency Visualizer (FFT)', statusText: 'ONLINE', status: 'safe', dot: 'green', domain: 'Visualizer', sentiment: 100, delta: '60fps FFT', complaints: 0, regulations: 1, services: 10, entities: 1, analysis: 'Extracts real-time byte frequency data driving the 34-bar equalizer histogram and sine wave.' }
                    ],
                    cognition: [
                        { id: 'c1', title: 'Google Gemini 3 Flash-Lite Primary LLM Core', statusText: 'ONLINE', status: 'safe', dot: 'green', domain: 'Primary LLM', sentiment: 99, delta: 'Primary Core', complaints: 0, regulations: 2, services: 24, entities: 4, analysis: 'Primary conversational brain executing tools, reasoning, and context retrieval.' },
                        { id: 'c2', title: 'Anthropic Claude 3.5 Sonnet Matrix', statusText: 'STANDBY', status: 'safe', dot: 'green', domain: 'Fallback LLM', sentiment: 97, delta: 'Dual-Core Standby', complaints: 0, regulations: 1, services: 14, entities: 2, analysis: 'Fallback LLM matrix ready to handle requests if primary API quotas or network delays occur.' },
                        { id: 'c3', title: 'Deterministic Intent & Tool Selector Engine', statusText: 'ONLINE', status: 'safe', dot: 'green', domain: 'Tool Selector', sentiment: 100, delta: 'Local Heuristics', complaints: 0, regulations: 1, services: 18, entities: 1, analysis: 'Evaluates commands for camera, screen, reminders, shutdown, calculations, and web launches.' },
                        { id: 'c4', title: 'Kavi Stark Supreme Creator Hierarchy Protocol', statusText: 'ACTIVE', status: 'safe', dot: 'green', domain: 'Root Governance', sentiment: 100, delta: 'Immutable', complaints: 0, regulations: 1, services: 20, entities: 1, analysis: 'Protects the system against unauthorized prompt injections and binds Ultron to Kavi Stark.' }
                    ],
                    telephony: [
                        { id: 't1', title: 'Outbound Cellular Call Dispatcher (+91 9092117397)', statusText: 'ARMED:AUTO', status: 'disputed', dot: 'red', domain: 'Telephony Gateway', sentiment: 95, delta: 'Carrier Armed', complaints: 12, regulations: 1, services: 8, entities: 2, analysis: 'Initiates telephone calls directly to Kavi Stark when urgent reminders are due.' },
                        { id: 't2', title: 'Tactical Ringtone & Vibrator Announcer', statusText: 'ACTIVE', status: 'safe', dot: 'green', domain: 'Acoustic Alert', sentiment: 97, delta: 'Synthesized Chime', complaints: 0, regulations: 1, services: 6, entities: 1, analysis: 'Plays multi-oscillator alarm chime and triggers mobile vibration patterns on due alerts.' },
                        { id: 't3', title: '4-Second Autonomous Reminder Polling Daemon', statusText: 'ONLINE', status: 'safe', dot: 'green', domain: 'Daemon Sentinel', sentiment: 100, delta: '4s Cycle', complaints: 0, regulations: 1, services: 15, entities: 2, analysis: 'Scans the database every 4 seconds to detect upcoming or overdue reminders.' }
                    ],
                    synthesis: [
                        { id: 's1', title: 'Edge-TTS Christopher Neural Deep Voice Engine', statusText: 'ACTIVE', status: 'safe', dot: 'green', domain: 'Primary Voice', sentiment: 98, delta: '-14Hz Pitch', complaints: 0, regulations: 1, services: 12, entities: 2, analysis: 'Cinematic Christopher neural voice generator tuned to -14Hz pitch and -8% cadence.' },
                        { id: 's2', title: 'Offline SAPI5 pyttsx3 Resonant Synthesizer', statusText: 'STANDBY', status: 'safe', dot: 'green', domain: 'Offline TTS', sentiment: 95, delta: 'Zero-Network', complaints: 0, regulations: 1, services: 8, entities: 1, analysis: 'Local Windows speech engine providing offline voice delivery when internet is disconnected.' },
                        { id: 's3', title: 'Dynamic 34-Bar Equalizer Waveform Modulator', statusText: 'ACTIVE', status: 'safe', dot: 'green', domain: 'Equalizer Emitter', sentiment: 99, delta: 'Real-Time Sync', complaints: 0, regulations: 1, services: 14, entities: 1, analysis: 'Pulsates histogram bars and traveling photon sparks synchronized to voice phonemes.' }
                    ]
                }
            }
        };

        let currentDatasetKey = 'ultronVoice';
        let activeCategoryKey = 'automation';
        let selectedNodeId = 'u2';"""

text = text[:start_idx] + new_js_datasets + text[end_idx + len(end_marker):]

# Add triggerQuickDiagnostic implementation
diag_func = """
        function triggerQuickDiagnostic() {
            triggerSynapseSurge(3.0);
            const deckInput = document.getElementById('deckChatInput');
            if (deckInput) deckInput.value = 'system diagnostics';
            submitDeckChat();
        }
"""

if "function triggerQuickDiagnostic()" not in text:
    text = text.replace("function triggerQuickAiAnalysis() {", diag_func + "\n        function triggerQuickAiAnalysis() {", 1)

with open(VW_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved updated JavaScript engine successfully!")

