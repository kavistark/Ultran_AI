# scratch/update_ultron_content.py
import re
import os

TEMPLATES_DIR = r"c:\Users\MrHat\app\ai_ultran\templates"
VW_PATH = os.path.join(TEMPLATES_DIR, "voice_wave.html")

with open(VW_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update HTML Markup
old_html_pattern = re.compile(
    r'<!-- Master Central AI Policy Platform Viewport.*?<!-- Right Inspector & Intelligent AI Assistant Deck -->',
    re.DOTALL
)

new_header_and_canvas = """<!-- Master Central AI Policy Platform Viewport (Exact High-Precision UI) -->
    <div class="central-platform-container" id="centralPlatformContainer">
        <!-- Top Global HUD Bar -->
        <header class="platform-top-bar" id="platformTopBar">
            <div class="brand-group" onclick="resetCanvasTransform()">
                <div class="brand-logo-icon">
                    <svg viewBox="0 0 40 40" width="34" height="34" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="20" cy="20" r="17" stroke="rgba(56, 189, 248, 0.4)" stroke-width="1.5" stroke-dasharray="3 3"/>
                        <circle cx="20" cy="20" r="12" stroke="#38bdf8" stroke-width="2"/>
                        <circle cx="20" cy="20" r="5" fill="#38bdf8"/>
                        <line x1="20" y1="2" x2="20" y2="8" stroke="#38bdf8" stroke-width="2"/>
                        <line x1="20" y1="32" x2="20" y2="38" stroke="#38bdf8" stroke-width="2"/>
                        <line x1="2" y1="20" x2="8" y2="20" stroke="#38bdf8" stroke-width="2"/>
                        <line x1="32" y1="20" x2="38" y2="20" stroke="#38bdf8" stroke-width="2"/>
                    </svg>
                </div>
                <div class="brand-text-col">
                    <div class="brand-title" id="platformMainTitle">AI ULTRON // Master Autonomous Core</div>
                    <div class="brand-subtitle"><span class="live-dot"></span> VOICE INTELLIGENCE &bull; DUAL-CORE ONLINE</div>
                </div>
            </div>

            <!-- Floating Dark Glass Toolbar (Center) -->
            <div class="floating-toolbar" id="canvasToolbar">
                <button class="toolbar-pill-btn active" id="btnModeGraph" title="Mindmap Pipeline View" onclick="switchGraphMode('radial')">
                    <i class="fas fa-network-wired"></i>
                </button>
                <button class="toolbar-pill-btn" id="btnModeHierarchy" title="Execution Hierarchy View" onclick="switchGraphMode('hierarchy')">
                    <i class="fas fa-sitemap"></i>
                </button>
                <div class="toolbar-divider"></div>
                <button class="toolbar-pill-btn" id="btnZoomIn" title="Zoom In (+)" onclick="zoomCanvas(0.18)">
                    <i class="fas fa-plus"></i>
                </button>
                <button class="toolbar-pill-btn" id="btnZoomOut" title="Zoom Out (-)" onclick="zoomCanvas(-0.18)">
                    <i class="fas fa-minus"></i>
                </button>
                <div class="toolbar-divider"></div>
                <button class="toolbar-pill-btn" id="btnFilterToggle" title="Filter Subsystems (All / Nominal / Armed)" onclick="cycleNodeFilter()">
                    <i class="fas fa-filter"></i>
                </button>
                <button class="toolbar-pill-btn" id="btnAiSynapse" title="Trigger Synapse Energy Surge" onclick="toggleSynapseSurge()">
                    <i class="fas fa-bolt"></i>
                </button>
                <button class="toolbar-pill-btn" id="btnFitView" title="Reset / Fit Pipeline View" onclick="resetCanvasTransform()">
                    <i class="fas fa-expand"></i>
                </button>
            </div>

            <!-- Top Actions Group (Right) -->
            <div class="top-actions-group">
                <button class="btn-new-simulation" id="btnNewSimulation" onclick="openNewSimulationModal()">
                    <i class="fas fa-plus"></i> <span>New Directive</span>
                </button>
                <button class="dataset-switch-pill" id="btnSwitchPreset" onclick="triggerQuickDiagnostic()" title="Run System Diagnostics">
                    <i class="fas fa-microchip"></i> <span id="presetLabelText">⚡ Diagnostics</span>
                </button>
                <div class="user-avatar-pill" title="Master Authority: Kavi Stark" onclick="resetCanvasTransform()">
                    <div class="avatar-circle">
                        <span class="avatar-text">KS</span>
                        <span class="online-indicator"></span>
                    </div>
                </div>
                <button class="icon-action-btn" id="btnSearchNodes" title="Search Voice Subroutines" onclick="openSearchModal()">
                    <i class="fas fa-magnifying-glass"></i>
                </button>
                <button class="icon-action-btn" id="btnSettingsMenu" title="Ultron Control Manual & Settings" onclick="toggleControlMenu()">
                    <i class="fas fa-bars-staggered"></i>
                </button>
            </div>
        </header>

        <!-- Context Breadcrumb Pill -->
        <div class="breadcrumb-kpi-pill" id="breadcrumbKpiPill">
            <i class="fas fa-satellite-dish"></i> <span id="breadcrumbKpiText">Active Pipeline: Acoustic Input ➔ Dual-Core Cognitive Matrix ➔ Device Automation &amp; Cellular Call Gateway</span>
        </div>

        <!-- Interactive Neural Canvas Viewport (Pannable & Zoomable) -->
        <div class="neural-canvas-viewport" id="canvasViewport" onmousedown="handleCanvasMouseDown(event)" onwheel="handleCanvasWheel(event)">
            <!-- Transformable Canvas World Layer -->
            <div class="neural-canvas-world" id="canvasWorld">
                
                <!-- SVG Layer for Smooth Cubic Bézier Spline Curves -->
                <svg class="canvas-svg-layer" id="canvasSvgLayer">
                    <defs>
                        <linearGradient id="curveGradientNormal" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.3"/>
                            <stop offset="60%" stop-color="#06b6d4" stop-opacity="0.55"/>
                            <stop offset="100%" stop-color="#14b8a6" stop-opacity="0.75"/>
                        </linearGradient>
                        <linearGradient id="curveGradientActive" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#fbbf24" stop-opacity="0.75"/>
                            <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.95"/>
                            <stop offset="100%" stop-color="#22d3ee" stop-opacity="1"/>
                        </linearGradient>
                        <filter id="glowFilter" x="-20%" y="-20%" width="140%" height="140%">
                            <feGaussianBlur stdDeviation="3" result="blur"/>
                            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
                        </filter>
                    </defs>
                    <g id="svgCurvesGroup"></g>
                </svg>

                <!-- Canvas Layer for Real-Time Traveling Photon Light Sparks -->
                <canvas class="canvas-photon-layer" id="photonCanvas" width="2500" height="2000"></canvas>

                <!-- Interactive HTML Nodes Layer -->
                <div class="canvas-nodes-layer" id="canvasNodesLayer">
                    
                    <!-- Root Planetary Core Node (Left) -->
                    <div class="root-core-container" id="rootCoreNode" onclick="handleRootNodeClick()">
                        <div class="core-aura-glow"></div>
                        <div class="core-orbit-ring ring-dashed"></div>
                        <div class="core-orbit-ring ring-solid"></div>
                        <div class="core-planet-sphere"></div>
                        <div class="core-node-label" id="rootNodeLabel">AI ULTRON PRIME<br><strong>AUTONOMOUS VOICE CORE</strong></div>
                        <div class="core-status-tag" id="rootNodeStatusTag">
                            <span class="status-dot green"></span>
                            <span class="status-text">SAFE: ARMED</span>
                        </div>
                    </div>

                    <!-- Level 1 Category Cards Column -->
                    <div class="category-cards-col" id="categoryCardsCol">
                        <!-- Rendered by JS -->
                    </div>

                    <!-- Level 2 Fanning Child Nodes Column -->
                    <div class="child-nodes-col" id="childNodesCol">
                        <!-- Rendered by JS -->
                    </div>

                </div>
            </div>
        </div>

        <!-- Right Inspector & Intelligent AI Assistant Deck -->"""

html = old_html_pattern.sub(new_header_and_canvas, html)
print("Updated header and canvas section.")

# 2. Update Deck Markup
old_deck_pattern = re.compile(
    r'<aside class="inspector-deck-panel".*?<!-- Modal: \+ New Simulation -->',
    re.DOTALL
)

new_deck = """<aside class="inspector-deck-panel" id="inspectorDeckPanel" onclick="event.stopPropagation()">
            <!-- Deck Header -->
            <div class="deck-header">
                <div class="deck-domain-chip" id="deckDomainChip">
                    <i class="fas fa-robot"></i> <span id="deckDomainText">Voice Assistant Subsystem</span>
                </div>
                <a href="javascript:void(0)" class="deck-explore-btn" onclick="openDetailsModal()">
                    Explore details <i class="fas fa-angle-right"></i>
                </a>
            </div>

            <!-- Node Main Title & Metadata -->
            <div class="deck-title-wrapper">
                <h2 class="deck-main-title" id="deckMainTitle">Autonomous Phone Reminder & Voice Dispatch System</h2>
                <div class="deck-meta-row">
                    <span class="badge-status-active" id="deckStatusBadge">ACTIVE // REAL-TIME</span>
                    <span class="deck-date-text" id="deckDateText">Pipeline Latency: 24ms &bull; Dual-Core Armed</span>
                </div>
            </div>

            <!-- Sentiment Rate / Efficiency Card with Equalizer Histogram -->
            <div class="deck-card sentiment-card">
                <div class="sentiment-card-header">
                    <span class="card-kicker">Subsystem Health & Availability</span>
                    <span class="sentiment-tag" id="deckSentimentTag">Optimal</span>
                </div>
                <div class="sentiment-val-row">
                    <div class="sentiment-big-num" id="deckSentimentNum">98%</div>
                    <div class="sentiment-delta-pill positive" id="deckSentimentDelta">
                        <i class="fas fa-arrow-trend-up"></i> +4% <span>vs last cycle (Nominal)</span>
                    </div>
                    <!-- Dynamic Frequency Histogram Equalizer (34 bars) -->
                    <div class="histogram-container" id="sentimentHistogram"></div>
                </div>
            </div>

            <!-- 2x2 Quick KPI Metrics Grid -->
            <div class="deck-kpi-grid">
                <div class="kpi-mini-card">
                    <div class="kpi-icon-row"><i class="fas fa-bell"></i> <span class="kpi-num" id="kpiComplaints">12</span></div>
                    <div class="kpi-label">Pending Reminders & Triggers</div>
                </div>
                <div class="kpi-mini-card">
                    <div class="kpi-icon-row"><i class="fas fa-laptop-code"></i> <span class="kpi-num" id="kpiRegulations">2</span></div>
                    <div class="kpi-label">Active Client Devices</div>
                </div>
                <div class="kpi-mini-card">
                    <div class="kpi-icon-row"><i class="fas fa-bolt"></i> <span class="kpi-num" id="kpiServices">18</span></div>
                    <div class="kpi-label">Autonomous Subroutines</div>
                </div>
                <div class="kpi-mini-card">
                    <div class="kpi-icon-row"><i class="fas fa-microchip"></i> <span class="kpi-num" id="kpiEntities">4</span></div>
                    <div class="kpi-label">Armed Cognitive Pipelines</div>
                </div>
            </div>

            <!-- AI Analysis Deck -->
            <div class="deck-card ai-analysis-card">
                <div class="ai-analysis-header">
                    <div class="ai-spark-title"><i class="fas fa-wand-magic-sparkles"></i> AI Subsystem Reasoning</div>
                </div>
                <div class="ai-analysis-sub" id="deckAiSubheading">Autonomous Working Process</div>
                <p class="ai-analysis-body" id="deckAiBody">
                    Working Process: 1. Acoustic audio captured via low-power mic sentinel. 2. Speech-to-Text transcribed and routed to Dual-Core Gemini 3 + Claude 3.5. 3. System execution tool dispatched on Windows 10 host. 4. Christopher Neural voice delivers acoustic confirmation. 5. If task deadline is missed, outbound cellular call to +91 9092117397 is triggered automatically.
                </p>
            </div>

            <!-- Bottom Integrated Interactive Chat & Voice Dock -->
            <div class="deck-chat-dock" id="deckChatDock">
                <div class="chat-input-pill-wrapper">
                    <input type="text" id="deckChatInput" placeholder="Ask Ultron a question or issue a directive..." autocomplete="off" spellcheck="false" onkeydown="handleDeckChatKeyDown(event)">
                    <button type="button" class="deck-mic-btn" id="deckMicBtn" title="Voice Recognition" onclick="toggleVoiceRecognitionFromDeck()">
                        <i class="fas fa-microphone"></i>
                    </button>
                    <button type="button" class="deck-send-btn" id="deckSendBtn" title="Send Directive" onclick="submitDeckChat()">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
                <div class="chat-chips-row">
                    <div class="chip-item agent-chip" id="chipAgentSelect" onclick="cycleAgentMode()">
                        <i class="fas fa-robot"></i> <span id="chipAgentName">Ultron Prime (Dual-Core)</span>
                    </div>
                    <div class="chip-item badge-chip" title="Active Context Tags">+4 Tools</div>
                    <div class="chip-item action-chip" onclick="triggerQuickAiAnalysis()">
                        <i class="fas fa-wand-magic-sparkles"></i> AI Reasoning
                    </div>
                </div>
            </div>
        </aside>

        <!-- Modal: + New Simulation -->"""

html = old_deck_pattern.sub(new_deck, html)
print("Updated deck markup.")

# 3. Update Modal Title & Labels
html = html.replace('Create New Simulation / Directive', 'Create New Directive / Scheduled Reminder')
html = html.replace('Simulation Title', 'Directive / Task Title')
html = html.replace('Category Hub', 'Process Pipeline Stage')
html = html.replace('Generate Simulation Branch', 'Deploy Directive to Pipeline')

with open(VW_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved HTML changes successfully!")
