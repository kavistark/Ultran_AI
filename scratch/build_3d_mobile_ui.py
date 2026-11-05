# scratch/build_3d_mobile_ui.py
import re
import os

TEMPLATES_DIR = r"c:\Users\MrHat\app\ai_ultran\templates"
VW_PATH = os.path.join(TEMPLATES_DIR, "voice_wave.html")

print(f"Reading {VW_PATH}...")
with open(VW_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add 3D CSS and Mobile Styles
mobile_and_3d_css = """
        /* ==========================================================================
           3D HOLOGRAPHIC EFFECTS & MOBILE PHONE OPTIMIZATION
           ========================================================================== */

        /* 3D Perspective Canvas Container */
        .central-platform-container {
            perspective: 1400px;
            perspective-origin: 50% 50%;
        }

        .neural-canvas-world {
            transform-style: preserve-3d;
            transition: transform 0.05s ease-out;
        }

        /* 3D Gyroscopic Gimbal Stage */
        .gimbal-stage {
            position: absolute;
            width: 220px;
            height: 220px;
            transform-style: preserve-3d;
            pointer-events: none;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .gimbal-ring {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
            will-change: transform;
            transform-style: preserve-3d;
        }

        .ring-3d-cyan {
            width: 140px;
            height: 140px;
            border: 1.8px dashed rgba(56, 189, 248, 0.65);
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.4), inset 0 0 12px rgba(6, 182, 212, 0.3);
            animation: spinGimbal1 18s linear infinite;
        }

        .ring-3d-violet {
            width: 175px;
            height: 175px;
            border: 1.5px solid rgba(139, 92, 246, 0.55);
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.35);
            animation: spinGimbal2 24s linear infinite;
        }

        .ring-3d-gold {
            width: 205px;
            height: 205px;
            border: 1.2px dotted rgba(251, 191, 36, 0.5);
            box-shadow: 0 0 14px rgba(245, 158, 11, 0.25);
            animation: spinGimbal3 30s linear infinite;
        }

        @keyframes spinGimbal1 {
            0% { transform: rotateX(65deg) rotateY(25deg) rotateZ(0deg); }
            100% { transform: rotateX(65deg) rotateY(25deg) rotateZ(360deg); }
        }

        @keyframes spinGimbal2 {
            0% { transform: rotateX(-48deg) rotateY(60deg) rotateZ(360deg); }
            100% { transform: rotateX(-48deg) rotateY(60deg) rotateZ(0deg); }
        }

        @keyframes spinGimbal3 {
            0% { transform: rotateX(80deg) rotateY(-35deg) rotateZ(0deg); }
            100% { transform: rotateX(80deg) rotateY(-35deg) rotateZ(360deg); }
        }

        /* 3D Planet Sphere with Dynamic Lighting */
        .core-planet-sphere {
            transform-style: preserve-3d;
            transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease;
            position: relative;
        }

        .sphere-lighting-layer {
            position: absolute;
            inset: 0;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 28%, rgba(255, 255, 255, 0.8) 0%, rgba(56, 189, 248, 0.4) 30%, transparent 65%);
            pointer-events: none;
        }

        .sphere-equator-ring {
            position: absolute;
            top: 50%;
            left: -15%;
            right: -15%;
            height: 1.5px;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.9), #ffffff, rgba(56, 189, 248, 0.9), transparent);
            transform: translateY(-50%) rotateX(75deg);
            box-shadow: 0 0 12px #38bdf8;
            pointer-events: none;
        }

        /* 3D Core Reactive State */
        body.state-speaking .core-planet-sphere,
        body.state-speaking #corePlanetSphere {
            transform: scale3d(1.18, 1.18, 1.18);
            box-shadow: 0 0 65px rgba(220, 38, 38, 0.9), 0 0 110px rgba(249, 115, 22, 0.6);
            background: radial-gradient(circle at 35% 35%, #f87171 0%, #dc2626 40%, #7f1d1d 85%, #050814 100%);
        }

        body.state-listening .core-planet-sphere,
        body.state-listening #corePlanetSphere {
            transform: scale3d(1.14, 1.14, 1.14);
            box-shadow: 0 0 65px rgba(6, 182, 212, 0.9), 0 0 110px rgba(56, 189, 248, 0.6);
        }

        body.state-thinking .core-planet-sphere,
        body.state-thinking #corePlanetSphere {
            animation: spherePulse3D 1.4s infinite ease-in-out;
            box-shadow: 0 0 65px rgba(245, 158, 11, 0.9), 0 0 110px rgba(139, 92, 246, 0.6);
        }

        @keyframes spherePulse3D {
            0%, 100% { transform: scale3d(1, 1, 1); }
            50% { transform: scale3d(1.22, 1.22, 1.22) rotateY(15deg); }
        }

        /* 3D Floating Category Cards */
        .category-card {
            transform-style: preserve-3d;
            transform: translateZ(26px) rotateY(-1.5deg);
            transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .category-card:hover {
            transform: translateZ(42px) translateX(6px) rotateY(0deg) scale(1.03);
            box-shadow: 0 16px 42px rgba(0, 0, 0, 0.7), 0 0 25px rgba(6, 182, 212, 0.35);
        }

        .category-card.active {
            transform: translateZ(52px) translateX(10px) rotateY(0deg) scale(1.05);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 35px rgba(251, 191, 36, 0.45);
        }

        /* 3D Child Nodes */
        .child-node-item {
            transform-style: preserve-3d;
            transform: translateZ(16px);
            transition: all 0.2s ease;
        }

        .child-node-item:hover {
            transform: translateZ(28px) translateX(6px);
        }

        .child-node-item.selected {
            transform: translateZ(36px) translateX(8px);
        }

        /* 3D Inspector Deck Panel */
        .inspector-deck-panel {
            transform-style: preserve-3d;
            transform: translateZ(32px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        /* Mobile View Switcher Tabs (Header or Bottom) */
        .mobile-view-tabs {
            display: none;
            position: fixed;
            top: 66px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(12, 20, 34, 0.92);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 9999px;
            padding: 4px;
            gap: 4px;
            z-index: 120;
            backdrop-filter: blur(18px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        }

        .mobile-tab-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 9999px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
        }

        .mobile-tab-btn.active {
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.35), rgba(59, 130, 246, 0.45));
            color: #ffffff;
            border: 1px solid rgba(56, 189, 248, 0.4);
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.4);
        }

        /* Floating Mobile Voice Button */
        .mobile-floating-mic {
            display: none;
            position: fixed;
            bottom: calc(20px + env(safe-area-inset-bottom));
            right: 20px;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, #06b6d4, #3b82f6);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: #ffffff;
            font-size: 1.3rem;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 8px 30px rgba(6, 182, 212, 0.5), 0 0 20px rgba(59, 130, 246, 0.4);
            z-index: 150;
            transition: all 0.25s ease;
        }

        .mobile-floating-mic.active {
            background: linear-gradient(135deg, #ef4444, #f59e0b);
            animation: pulseMobileMic 1.4s infinite;
            box-shadow: 0 0 35px rgba(239, 68, 68, 0.85);
        }

        @keyframes pulseMobileMic {
            0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(239, 68, 68, 0.6); }
            50% { transform: scale(1.12); box-shadow: 0 0 40px rgba(239, 68, 68, 1); }
        }

        /* Mobile Bottom Peek Bar */
        .mobile-peek-bar {
            display: none;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(10, 18, 30, 0.96);
            border-top: 1px solid rgba(56, 189, 248, 0.35);
            padding: 12px 18px calc(14px + env(safe-area-inset-bottom));
            backdrop-filter: blur(24px);
            z-index: 90;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 -8px 30px rgba(0, 0, 0, 0.7);
            cursor: pointer;
        }

        .mobile-peek-info {
            display: flex;
            flex-direction: column;
            gap: 2px;
            max-width: 65%;
        }

        .mobile-peek-title {
            font-size: 0.78rem;
            font-weight: 700;
            color: #ffffff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .mobile-peek-status {
            font-size: 0.62rem;
            font-weight: 700;
            color: #38bdf8;
            letter-spacing: 0.5px;
        }

        .mobile-peek-action {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--plat-cyan);
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 9999px;
            padding: 5px 12px;
        }

        /* Mobile Responsive Breakpoints (< 900px) */
        @media (max-width: 900px) {
            .mobile-view-tabs {
                display: flex;
            }

            .mobile-floating-mic {
                display: flex;
            }

            .mobile-peek-bar {
                display: flex;
            }

            .platform-top-bar {
                padding: 12px 16px;
                height: 60px;
            }

            .brand-title {
                font-size: 0.82rem;
            }

            .brand-subtitle {
                font-size: 0.58rem;
            }

            .top-actions-group .btn-new-simulation,
            .top-actions-group .dataset-switch-pill {
                padding: 5px 10px;
                font-size: 0.72rem;
            }

            .breadcrumb-kpi-pill {
                display: none !important;
            }

            /* View Switching on Mobile */
            .central-platform-container.mobile-mode-mindmap .neural-canvas-viewport {
                position: absolute;
                inset: 0;
                right: 0;
                bottom: 64px;
                display: block;
                z-index: 10;
            }

            .central-platform-container.mobile-mode-mindmap .inspector-deck-panel {
                display: none;
            }

            .central-platform-container.mobile-mode-deck .neural-canvas-viewport {
                display: none;
            }

            .central-platform-container.mobile-mode-deck .inspector-deck-panel {
                position: fixed;
                top: 110px;
                left: 12px;
                right: 12px;
                bottom: calc(14px + env(safe-area-inset-bottom));
                width: auto;
                border-radius: 20px;
                display: flex;
                z-index: 100;
                max-height: none;
                height: auto;
            }

            .central-platform-container.mobile-mode-deck .mobile-peek-bar {
                display: none;
            }

            .central-platform-container.mobile-mode-deck .mobile-floating-mic {
                display: none;
            }
        }
"""

# Replace old CSS closing rule with new 3D and mobile CSS
target_css_end = ".central-platform-container::before {"
if target_css_end in text:
    text = text.replace(target_css_end, mobile_and_3d_css + "\n        " + target_css_end, 1)
    print("Inserted 3D and Mobile CSS.")

# 2. Add Mobile Tabs and 3D Gimbal Markup
# Check if rootCoreNode has gimbal-stage
if '<div class="gimbal-stage">' not in text:
    old_root_markup = '<div class="root-core-container" id="rootCoreNode" onclick="handleRootNodeClick()">'
    new_root_markup = """<div class="root-core-container" id="rootCoreNode" onclick="handleRootNodeClick()">
                        <div class="core-aura-glow"></div>
                        <!-- 3D Gyroscopic Gimbal Stage -->
                        <div class="gimbal-stage">
                            <div class="gimbal-ring ring-3d-cyan"></div>
                            <div class="gimbal-ring ring-3d-violet"></div>
                            <div class="gimbal-ring ring-3d-gold"></div>
                        </div>
                        <div class="core-planet-sphere" id="corePlanetSphere">
                            <div class="sphere-lighting-layer"></div>
                            <div class="sphere-equator-ring"></div>
                        </div>"""
    
    # We replace from old_root_markup up to <div class="core-node-label"
    old_core_block_pattern = re.compile(
        r'<div class="root-core-container" id="rootCoreNode" onclick="handleRootNodeClick\(\)">.*?<div class="core-node-label"',
        re.DOTALL
    )
    text = old_core_block_pattern.sub(new_root_markup + '\n                        <div class="core-node-label"', text, count=1)
    print("Inserted 3D Gimbal Stage & Planet Sphere layers.")

# Add Mobile View Tabs & Floating Mic & Peek Bar inside #centralPlatformContainer
mobile_html_widgets = """
        <!-- Mobile Mode Switcher Tabs (3D Mindmap vs Inspector Deck) -->
        <div class="mobile-view-tabs" id="mobileViewTabs">
            <button class="mobile-tab-btn active" id="tabBtnMindmap" onclick="switchMobileView('mindmap')">
                <i class="fas fa-network-wired"></i> <span>3D Mindmap</span>
            </button>
            <button class="mobile-tab-btn" id="tabBtnDeck" onclick="switchMobileView('deck')">
                <i class="fas fa-sliders"></i> <span>Ultron Deck</span>
            </button>
        </div>

        <!-- Floating Mobile Voice Mic (Thumb-Accessible) -->
        <button class="mobile-floating-mic" id="mobileFloatingMicBtn" title="Speak to Ultron" onclick="toggleVoiceRecognitionFromDeck()">
            <i class="fas fa-microphone"></i>
        </button>

        <!-- Mobile Bottom Peek Bar -->
        <div class="mobile-peek-bar" id="mobilePeekBar" onclick="switchMobileView('deck')">
            <div class="mobile-peek-info">
                <div class="mobile-peek-title" id="mobilePeekTitle">Autonomous Phone Reminder & Voice Dispatch System</div>
                <div class="mobile-peek-status" id="mobilePeekStatus"><span class="status-dot green"></span> ACTIVE // 98% NOMINAL</div>
            </div>
            <div class="mobile-peek-action">
                <span>Inspect</span> <i class="fas fa-angle-up"></i>
            </div>
        </div>
"""

# Place mobile_html_widgets before </aside> or right before modals
if 'id="mobileViewTabs"' not in text:
    target_place = '<!-- Modal: + New Simulation -->'
    text = text.replace(target_place, mobile_html_widgets + "\n        " + target_place, 1)
    print("Inserted Mobile View Tabs, Floating Mic, and Peek Bar.")

# 3. Add Mobile Touch Gestures (Single finger pan, Two finger pinch-zoom, Orientation tilt)
mobile_js_engine = """
        /* ==========================================================================
           MOBILE TOUCH ENGINE & 3D GYROSCOPE ORIENTATION PARALLAX
           ========================================================================== */
        let currentMobileView = 'mindmap'; // 'mindmap' or 'deck'

        function switchMobileView(view) {
            currentMobileView = view;
            const container = document.getElementById('centralPlatformContainer');
            const tabMindmap = document.getElementById('tabBtnMindmap');
            const tabDeck = document.getElementById('tabBtnDeck');

            if (container) {
                container.classList.remove('mobile-mode-mindmap', 'mobile-mode-deck');
                container.classList.add(view === 'mindmap' ? 'mobile-mode-mindmap' : 'mobile-mode-deck');
            }
            if (tabMindmap) tabMindmap.classList.toggle('active', view === 'mindmap');
            if (tabDeck) tabDeck.classList.toggle('active', view === 'deck');

            if (view === 'mindmap') {
                setTimeout(recalculateSplines, 80);
            }
        }

        // Initialize Mobile Mode Container
        function initMobileContainer() {
            const container = document.getElementById('centralPlatformContainer');
            if (container && window.innerWidth <= 900) {
                container.classList.add('mobile-mode-mindmap');
            }
        }

        // Update Mobile Peek Bar
        function updateMobilePeekBar(node) {
            const titleEl = document.getElementById('mobilePeekTitle');
            const statusEl = document.getElementById('mobilePeekStatus');
            if (titleEl && node) titleEl.textContent = node.title;
            if (statusEl && node) {
                statusEl.innerHTML = `<span class="status-dot ${node.dot || 'green'}"></span> ${node.statusText || 'ACTIVE'} // ${node.sentiment || 98}% NOMINAL`;
            }
        }

        // 3D Gyroscope Device Orientation Parallax
        function setup3DGyroscope() {
            if (window.DeviceOrientationEvent) {
                window.addEventListener('deviceorientation', (e) => {
                    if (e.beta === null || e.gamma === null) return;
                    const tiltX = Math.min(20, Math.max(-20, e.beta - 45)) * 0.35;
                    const tiltY = Math.min(25, Math.max(-25, e.gamma)) * 0.35;

                    const sphere = document.getElementById('corePlanetSphere');
                    if (sphere) {
                        sphere.style.transform = `rotateX(${-tiltX}deg) rotateY(${tiltY}deg)`;
                    }
                }, { passive: true });
            }
        }

        // Mobile Touch Pan & Pinch-to-Zoom
        function setupTouchGestures() {
            const vp = document.getElementById('canvasViewport');
            if (!vp) return;

            let touchStartX = 0;
            let touchStartY = 0;
            let initialDistance = 0;
            let initialScale = 1.0;
            let isTouchDragging = false;

            vp.addEventListener('touchstart', (e) => {
                if (e.touches.length === 1) {
                    if (e.target.closest('.category-card') || e.target.closest('.child-node-item') || e.target.closest('.root-core-container')) {
                        return;
                    }
                    isTouchDragging = true;
                    touchStartX = e.touches[0].clientX - canvasPanX;
                    touchStartY = e.touches[0].clientY - canvasPanY;
                } else if (e.touches.length === 2) {
                    isTouchDragging = false;
                    initialDistance = Math.hypot(
                        e.touches[0].clientX - e.touches[1].clientX,
                        e.touches[0].clientY - e.touches[1].clientY
                    );
                    initialScale = canvasScale;
                }
            }, { passive: true });

            vp.addEventListener('touchmove', (e) => {
                if (e.touches.length === 1 && isTouchDragging) {
                    canvasPanX = e.touches[0].clientX - touchStartX;
                    canvasPanY = e.touches[0].clientY - touchStartY;
                    applyCanvasTransform();
                } else if (e.touches.length === 2 && initialDistance > 0) {
                    const currentDist = Math.hypot(
                        e.touches[0].clientX - e.touches[1].clientX,
                        e.touches[0].clientY - e.touches[1].clientY
                    );
                    const factor = currentDist / initialDistance;
                    canvasScale = Math.min(2.4, Math.max(0.4, initialScale * factor));
                    applyCanvasTransform();
                }
            }, { passive: true });

            vp.addEventListener('touchend', (e) => {
                if (e.touches.length < 2) initialDistance = 0;
                if (e.touches.length === 0) isTouchDragging = false;
            }, { passive: true });
        }
"""

# Place mobile_js_engine before initNeuralMindmap
if 'setupTouchGestures' not in text:
    text = text.replace('function initNeuralMindmap() {', mobile_js_engine + '\n        function initNeuralMindmap() {', 1)
    print("Inserted Mobile Touch & 3D Gyroscope Engine.")

# In updateRightDeckDetails, call updateMobilePeekBar
old_update_details = "if (breadcrumbEl) {\n                breadcrumbEl.textContent = `KPI overview: ${activeNode.title.substring(0, 50)}... [${activeNode.statusText}]`;\n            }"
new_update_details = old_update_details + "\n            updateMobilePeekBar(activeNode);"

if old_update_details in text:
    text = text.replace(old_update_details, new_update_details, 1)
    print("Hooked updateMobilePeekBar in updateRightDeckDetails.")

# In initNeuralMindmap, call mobile helpers
old_init_neural = "function initNeuralMindmap() {\n            initHistogramBars();"
new_init_neural = """function initNeuralMindmap() {
            initMobileContainer();
            setupTouchGestures();
            setup3DGyroscope();
            initHistogramBars();"""

if old_init_neural in text:
    text = text.replace(old_init_neural, new_init_neural, 1)
    print("Hooked initMobileContainer, setupTouchGestures, setup3DGyroscope in initNeuralMindmap.")

# Sync mobile floating mic with mic state
old_deck_mic_toggle = "const deckMic = document.getElementById('deckMicBtn');\n            if (deckMic) deckMic.classList.toggle('active', listening);"
new_deck_mic_toggle = """const deckMic = document.getElementById('deckMicBtn');
            if (deckMic) deckMic.classList.toggle('active', listening);
            const mobMic = document.getElementById('mobileFloatingMicBtn');
            if (mobMic) mobMic.classList.toggle('active', listening);"""

if old_deck_mic_toggle in text:
    text = text.replace(old_deck_mic_toggle, new_deck_mic_toggle, 1)
    print("Synced mobileFloatingMicBtn in setMicrophoneUI.")

with open(VW_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved voice_wave.html successfully with 3D Effects and Phone UI Customization!")

