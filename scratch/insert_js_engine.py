# scratch/insert_js_engine.py
import os
import sys

TEMPLATES_DIR = r"c:\Users\MrHat\app\ai_ultran\templates"
VW_PATH = os.path.join(TEMPLATES_DIR, "voice_wave.html")

print("Reading voice_wave.html...")
with open(VW_PATH, "r", encoding="utf-8") as f:
    html = f.read()

script_tag = "<script>"
idx = html.find(script_tag)
if idx == -1:
    print("Error: <script> tag not found")
    sys.exit(1)

js_engine = r"""
        /* ==========================================================================
           CENTRAL AI POLICY PLATFORM & NEURAL MINDMAP ENGINE
           ========================================================================== */

        // Preset Datasets
        const MINDMAP_DATASETS = {
            policy: {
                platformTitle: 'Central AI Policy Platform',
                breadcrumb: 'KPI overview: UAE law 42/2022 public complaints and AI analysis',
                root: {
                    id: 'root',
                    title: 'Federal Decree-Law',
                    subtitle: 'No. 41 of 2021',
                    status: 'SAFE: SET',
                    statusDot: 'green',
                    domain: 'Civil & Legislative Core',
                    analysis: 'Central legislative anchor establishing sovereign judicial standards, civil obligations, and digital arbitration protocols across all corporate entities.'
                },
                categories: [
                    { id: 'services', count: 18, label: 'Services', icon: 'fas fa-cubes', domain: 'Public Services & Registry' },
                    { id: 'entities', count: 3, label: 'Entities', icon: 'fas fa-shield-halved', domain: 'Sovereign Authorities' },
                    { id: 'laws', count: 24, label: 'Related Federal Laws', icon: 'fas fa-scale-balanced', active: true, domain: 'Healthcare & Civil Code' },
                    { id: 'kpis', count: 32, label: 'KPIs', icon: 'fas fa-chart-pie', domain: 'Compliance Metrics' },
                    { id: 'procedural', count: 12, label: 'Related Federal Laws', icon: 'fas fa-book-bookmark', domain: 'Procedural Codes' }
                ],
                childNodes: {
                    laws: [
                        { id: 'n1', title: 'Bank of New York Mellon Corp.', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Banking & Securities', sentiment: 82, delta: '+6% this quarter', complaints: 4, regulations: 6, services: 14, entities: 9, analysis: 'Institutional custody clearings operating within standardized compliance boundaries with zero active regulatory infractions.' },
                        { id: 'n2', title: 'Federal Law No. (32) of 2021 Promulgating Commercial Companies', statusText: 'DISPUTED', status: 'disputed', dot: 'red', domain: 'Commercial Law', sentiment: 38, delta: '-12% this month', complaints: 26, regulations: 8, services: 22, entities: 15, analysis: 'Article 14 dispute flagged regarding cross-border capital repatriation quotas. Legal advisory recommends deregulation of equity holding restrictions.' },
                        { id: 'n3', title: 'Bank of New York Mellon Corp. - Escrow Registry', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Banking & Securities', sentiment: 76, delta: '+2% last cycle', complaints: 2, regulations: 3, services: 11, entities: 5, analysis: 'Escrow verification protocols verified. Compliance index nominal across institutional clearing vaults.' },
                        { id: 'n4', title: 'Bank of New York Mellon Corp. - Custody Clearing', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Custody Services', sentiment: 91, delta: '+4% last month', complaints: 1, regulations: 4, services: 8, entities: 4, analysis: 'High asset liquidity guarantees recognized under sovereign tier-1 banking standards.' },
                        { id: 'n5', title: 'Emirates Citizens Affairs Office - Civil Rights', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Civil Rights', sentiment: 88, delta: '+8% this month', complaints: 5, regulations: 2, services: 19, entities: 11, analysis: 'Citizen dispute arbitration turnaround reduced by 34% following digitalization of procedural filings.' },
                        { id: 'n6', title: 'Bank of New York Mellon Corp. - Settlement Hub', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Banking & Securities', sentiment: 84, delta: '+1% last week', complaints: 3, regulations: 5, services: 12, entities: 7, analysis: 'Automated settlement batches operating without liquidity settlement delays.' },
                        { id: 'n7', title: 'Capital One Entities - Credit Governance', statusText: 'SAFE:SET', status: 'safe', dot: 'yellow', domain: 'Credit Regulation', sentiment: 62, delta: '-3% last quarter', complaints: 14, regulations: 3, services: 16, entities: 8, analysis: 'Moderate volatility detected in unsecured debt securitizations. Regulatory review pending.' },
                        { id: 'n8', title: 'Bank of New York Mellon Corp. - Asset Securitization', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Asset Management', sentiment: 79, delta: '+3% last month', complaints: 2, regulations: 4, services: 10, entities: 6, analysis: 'Asset-backed instruments compliant with international ESG and Basel III standards.' },
                        { id: 'n9', title: 'Bank of New York Mellon Corp. - Global Clearing', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Global Clearing', sentiment: 85, delta: '+5% this month', complaints: 6, regulations: 5, services: 15, entities: 8, analysis: 'FX clearing pipelines active across Middle Eastern and European trading windows.' },
                        { id: 'n10', title: 'East West Group Holding Ltd.', statusText: 'SAFE:SET', status: 'safe', dot: 'orange', domain: 'Corporate Holdings', sentiment: 58, delta: '-5% last month', complaints: 11, regulations: 4, services: 14, entities: 7, analysis: 'Corporate governance restructuring underway following transnational acquisition.' },
                        { id: 'n11', title: 'Emirates Citizens Affairs Office - Legal Aid', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Legal Aid', sentiment: 92, delta: '+10% this year', complaints: 3, regulations: 2, services: 16, entities: 12, analysis: 'Pro-bono legal consultation automated dispatch operating at 98% resolution velocity.' },
                        { id: 'n12', title: 'Bank of New York Mellon Corp. - Risk Desk', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Risk Desk', sentiment: 81, delta: '+2% last cycle', complaints: 4, regulations: 3, services: 9, entities: 5, analysis: 'Value-at-risk (VaR) matrices within sovereign regulatory stress-test limits.' },
                        { id: 'n13', title: 'Bank of New York Mellon Corp. - Compliance Node', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Compliance Node', sentiment: 87, delta: '+7% last month', complaints: 1, regulations: 6, services: 13, entities: 6, analysis: 'AML/KYC artificial intelligence heuristic audits verified with zero non-conformances.' },
                        { id: 'n14', title: 'Capital One Entities - Liquidity Protocol', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Capital Governance', sentiment: 74, delta: '+1% last week', complaints: 8, regulations: 2, services: 11, entities: 6, analysis: 'Tier-1 capital adequacy ratio maintained at 14.2% against prescribed 10.5% benchmark.' },
                        { id: 'n15', title: 'Bank of New York Mellon Corp. - FX Gate', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'FX Operations', sentiment: 83, delta: '+4% last month', complaints: 2, regulations: 4, services: 7, entities: 4, analysis: 'Cross-currency peg verification executed in microsecond latency cycles.' },
                        { id: 'n16', title: 'East West Enterprises - Corporate Division', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Corporate Division', sentiment: 71, delta: '-2% last month', complaints: 7, regulations: 3, services: 12, entities: 9, analysis: 'Corporate division filings synchronized with national commercial registry.' },
                        { id: 'n17', title: 'Federal Decree-Law No. (42) of 2022 Promulgating the Civil Procedure Code', statusText: 'DISPUTED', status: 'disputed', dot: 'red', domain: 'Healthcare & Civil Procedure', sentiment: 45, delta: '-4% last month', complaints: 12, regulations: 2, services: 18, entities: 12, selected: true, analysis: 'Multiple regulations were found to be out of date in the following domains. Automated legal cross-referencing indicates compliance friction across legacy banking and citizen procedural codes.' }
                    ],
                    services: [
                        { id: 's1', title: 'Digital Sovereign Escrow Clearance Hub', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Registry', sentiment: 94, delta: '+5% this month', complaints: 2, regulations: 3, services: 28, entities: 14, analysis: 'Unified public registry service for rapid escrow issuance and digital asset custody validation.' },
                        { id: 's2', title: 'Automated Citizen Mediation Gateway', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Judicial', sentiment: 89, delta: '+9% this month', complaints: 4, regulations: 2, services: 18, entities: 8, analysis: 'Online mediation gateway resolving civil disputes in under 48 hours without court backlog.' },
                        { id: 's3', title: 'Interbank Real-Time Gross Settlement (RTGS)', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Finance', sentiment: 98, delta: '+1% last cycle', complaints: 0, regulations: 5, services: 12, entities: 6, analysis: 'High-availability clearing node maintaining continuous interbank settlement readiness.' }
                    ],
                    entities: [
                        { id: 'e1', title: 'Central Bank of the United Arab Emirates (CBUAE)', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Monetary Authority', sentiment: 96, delta: '+3% this quarter', complaints: 1, regulations: 18, services: 42, entities: 1, analysis: 'Apex regulatory oversight entity managing liquidity ratios and digital currency standards.' },
                        { id: 'e2', title: 'Ministry of Justice - Judicial Council', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Judicial Authority', sentiment: 91, delta: '+6% this month', complaints: 3, regulations: 14, services: 36, entities: 1, analysis: 'Sovereign legislative body governing the implementation of Civil Procedure Decree-Laws.' },
                        { id: 'e3', title: 'Federal Authority for Identity & Citizenship', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Civil Authority', sentiment: 95, delta: '+4% this month', complaints: 2, regulations: 11, services: 50, entities: 1, analysis: 'Centralized biometric identity matrix verifying corporate signatory powers.' }
                    ],
                    kpis: [
                        { id: 'k1', title: 'Public Dispute Resolution Velocity (Index 92.4)', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Performance', sentiment: 92, delta: '+14% this year', complaints: 5, regulations: 2, services: 12, entities: 4, analysis: 'Time-to-settlement across commercial contracts decreased by 62% in the current fiscal period.' },
                        { id: 'k2', title: 'Regulatory Friction & Cross-Referencing Metric', statusText: 'DISPUTED', status: 'disputed', dot: 'red', domain: 'Compliance Stress', sentiment: 48, delta: '-9% last month', complaints: 32, regulations: 12, services: 24, entities: 18, analysis: 'Identified 18 overlapping legal stipulations causing friction in cross-border entity registration.' }
                    ],
                    procedural: [
                        { id: 'p1', title: 'Federal Decree-Law No. (14) on Commercial Transactions', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Commercial', sentiment: 87, delta: '+3% last month', complaints: 4, regulations: 3, services: 16, entities: 8, analysis: 'Codifies electronic negotiable instruments and sovereign commercial arbitration rights.' },
                        { id: 'p2', title: 'Cabinet Resolution No. (75) on Anti-Money Laundering', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Financial Security', sentiment: 95, delta: '+5% this month', complaints: 1, regulations: 9, services: 20, entities: 12, analysis: 'Strict financial intelligence reporting frameworks enforcing ultimate beneficial ownership transparency.' }
                    ]
                }
            },
            ultron: {
                platformTitle: 'AI ULTRON // Master Autonomous Core',
                breadcrumb: 'Live Telemetry: Host System & Outbound Phone Gateway Synchronized',
                root: {
                    id: 'root',
                    title: 'AI ULTRON PRIME',
                    subtitle: 'MASTER CORE v4.2',
                    status: 'ONLINE',
                    statusDot: 'green',
                    domain: 'Autonomous Sovereign Intelligence',
                    analysis: 'Ultron core system running continuously with zero latency. Dual-core Gemini 3 + Claude 3.5 armed. Master authority Kavi Stark.'
                },
                categories: [
                    { id: 'workstations', count: 4, label: 'Workstations & Cloud', icon: 'fas fa-laptop-code', domain: 'Endpoints' },
                    { id: 'telephony', count: 2, label: 'Phone Call Gateways', icon: 'fas fa-phone-volume', domain: 'Outbound Reminders' },
                    { id: 'automations', count: 16, label: 'Active Automations', icon: 'fas fa-bolt', active: true, domain: 'Continuous Sentinels' },
                    { id: 'vision', count: 8, label: 'Computer Vision Nodes', icon: 'fas fa-eye', domain: 'Optical Intelligence' },
                    { id: 'memories', count: 24, label: 'Context Synapses', icon: 'fas fa-brain', domain: 'Master Kavi Memory' }
                ],
                childNodes: {
                    automations: [
                        { id: 'u1', title: 'Workstation Battery & Power Sentinel', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Power Systems', sentiment: 96, delta: '+2% nominal', complaints: 0, regulations: 1, services: 8, entities: 2, analysis: 'Monitors laptop standby, AC charge status, and CPU throttle state with autonomous keepalive.' },
                        { id: 'u2', title: 'Direct Cellular Voice Call to +91 9092117397', statusText: 'DISPUTED', status: 'disputed', dot: 'red', domain: 'Telephony Dispatch', sentiment: 88, delta: 'Armed & Ready', complaints: 2, regulations: 1, services: 12, entities: 2, selected: true, analysis: 'Dispatches real outbound phone calls to Kavi Stark whenever urgent reminders or task deadlines elapse without verbal confirmation.' },
                        { id: 'u3', title: 'Dual-Core Gemini 3 + Claude 3.5 Engine', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Neural Engine', sentiment: 99, delta: '0ms Latency', complaints: 0, regulations: 2, services: 24, entities: 4, analysis: 'Google Gemini Flash-Lite paired with Anthropic Claude Sonnet with instant fallback and zero failure rate.' },
                        { id: 'u4', title: 'Optical Screen & Document Vision Inspector', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Computer Vision', sentiment: 93, delta: '+5% clarity', complaints: 1, regulations: 1, services: 10, entities: 2, analysis: 'Captures and analyzes workstation display or camera stream to extract tables, text, and visual context.' },
                        { id: 'u5', title: 'Autonomous Scheduled Reminder Dispatcher', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Scheduler', sentiment: 95, delta: '100% On-Time', complaints: 0, regulations: 1, services: 15, entities: 3, analysis: 'Background reminder polling service with ringtone dispatch and automated voice delivery.' },
                        { id: 'u6', title: 'Christopher Neural Voice Resonator (-14Hz)', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Acoustic Synthesizer', sentiment: 97, delta: 'Cinematic Deep', complaints: 0, regulations: 1, services: 6, entities: 2, analysis: 'Edge-TTS Christopher deep synthetic voice engine calibrated to -14Hz pitch and -8% cadence.' }
                    ],
                    workstations: [
                        { id: 'w1', title: 'Master Workstation (Windows 10 / Host PC)', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Host Device', sentiment: 98, delta: 'Online', complaints: 0, regulations: 1, services: 14, entities: 1, analysis: 'Primary execution terminal. Free disk: 17.8 GB of 237.4 GB. All diagnostic sweeps nominal.' }
                    ],
                    telephony: [
                        { id: 't1', title: 'Cellular Gateway Node (+91 9092117397)', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Cellular Voice', sentiment: 94, delta: 'Linked', complaints: 0, regulations: 1, services: 8, entities: 2, analysis: 'Primary phone destination for high-priority voice reminders and emergency wake alerts.' }
                    ],
                    vision: [
                        { id: 'v1', title: 'Primary Display Frame Grabber', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Optical Capture', sentiment: 92, delta: 'Ready', complaints: 0, regulations: 1, services: 5, entities: 1, analysis: 'Multimodal optical vision sensor enabling live visual Q&A on open windows.' }
                    ],
                    memories: [
                        { id: 'm1', title: 'Kavi Stark Master Profile & Authority Directives', statusText: 'SAFE:SET', status: 'safe', dot: 'green', domain: 'Master Protocol', sentiment: 100, delta: 'Absolute Master', complaints: 0, regulations: 1, services: 30, entities: 1, analysis: 'Permanent rule: Kavi Stark is the supreme master authority and creator. Ultron yields to no other.' }
                    ]
                }
            }
        };

        let currentDatasetKey = 'policy';
        let activeCategoryKey = 'laws';
        let selectedNodeId = 'n17';
        let activeFilterMode = 'all'; // 'all', 'safe', 'disputed'
        let currentGraphMode = 'radial'; // 'radial', 'hierarchy'
        let synapseSpeedMultiplier = 1.0;
        let isSynapseSurging = false;

        // Canvas Pan & Zoom State
        let canvasPanX = 0;
        let canvasPanY = 0;
        let canvasScale = 1.0;
        let isPanningCanvas = false;
        let startPanMouseX = 0;
        let startPanMouseY = 0;

        // Traveling Photon Animation State
        let photonParticles = [];
        let splinePathsData = [];
        let animationFrameId = null;

        // DOM Elements
        const canvasViewport = document.getElementById('canvasViewport');
        const canvasWorld = document.getElementById('canvasWorld');
        const svgCurvesGroup = document.getElementById('svgCurvesGroup');
        const photonCanvas = document.getElementById('photonCanvas');
        const photonCtx = photonCanvas ? photonCanvas.getContext('2d') : null;
        const categoryCardsCol = document.getElementById('categoryCardsCol');
        const childNodesCol = document.getElementById('childNodesCol');

        // Initialize Mindmap
        function initNeuralMindmap() {
            initHistogramBars();
            loadDataset(currentDatasetKey);
            setupCanvasPanZoom();
            startPhotonSparkEngine();
            syncDeckChatWithCore();
        }

        // Initialize 36 Histogram Bars
        function initHistogramBars() {
            const container = document.getElementById('sentimentHistogram');
            if (!container) return;
            container.innerHTML = '';
            for (let i = 0; i < 34; i++) {
                const bar = document.createElement('div');
                bar.className = 'hist-bar';
                // initial distribution curve
                const factor = Math.sin((i / 34) * Math.PI);
                const height = Math.max(4, Math.floor(factor * 28 + Math.random() * 8));
                bar.style.height = height + 'px';
                container.appendChild(bar);
            }
        }

        // Animate Histogram with Sound or Procedural Pulse
        function animateHistogramLoop() {
            const container = document.getElementById('sentimentHistogram');
            if (!container) return;
            const bars = container.children;
            const hasAudioData = freqArray && (isSpeaking || isListening);

            for (let i = 0; i < bars.length; i++) {
                if (hasAudioData && audioAnalyser) {
                    audioAnalyser.getByteFrequencyData(freqArray);
                    const idx = Math.floor((i / bars.length) * (freqArray.length / 2));
                    const val = freqArray[idx] || 0;
                    const h = Math.max(4, Math.floor((val / 255) * 36));
                    bars[i].style.height = h + 'px';
                } else {
                    // gentle organic idle breathing
                    const time = Date.now() * 0.003;
                    const sine = Math.sin(time + i * 0.28);
                    const h = Math.max(4, Math.floor(14 + sine * 10 + (i % 3) * 3));
                    bars[i].style.height = h + 'px';
                }
            }
            requestAnimationFrame(animateHistogramLoop);
        }
        requestAnimationFrame(animateHistogramLoop);

        // Load & Render Dataset
        function loadDataset(key) {
            currentDatasetKey = key;
            const data = MINDMAP_DATASETS[key];
            if (!data) return;

            // Update Top Bar & Breadcrumb
            const titleEl = document.getElementById('platformMainTitle');
            if (titleEl) titleEl.textContent = data.platformTitle;
            const breadcrumbEl = document.getElementById('breadcrumbKpiText');
            if (breadcrumbEl) breadcrumbEl.textContent = data.breadcrumb;
            const presetLabel = document.getElementById('presetLabelText');
            if (presetLabel) presetLabel.textContent = key === 'policy' ? 'Preset: Policy' : 'Preset: Ultron OS';

            // Root Node
            const rootLabel = document.getElementById('rootNodeLabel');
            if (rootLabel) {
                rootLabel.innerHTML = `${data.root.title}<br><strong>${data.root.subtitle}</strong>`;
            }
            const rootStatus = document.getElementById('rootNodeStatusTag');
            if (rootStatus) {
                rootStatus.innerHTML = `<span class="status-dot ${data.root.statusDot}"></span><span class="status-text">${data.root.status}</span>`;
            }

            // Find default active category
            const activeCat = data.categories.find(c => c.active) || data.categories[0];
            activeCategoryKey = activeCat.id;

            // Pick default selected node
            const nodes = data.childNodes[activeCategoryKey] || [];
            const selNode = nodes.find(n => n.selected) || nodes[0] || null;
            if (selNode) {
                selectedNodeId = selNode.id;
            }

            renderCategoryCards();
            renderChildNodes();
            updateRightDeckDetails();
            recalculateSplines();
        }

        // Render Level 1 Category Cards
        function renderCategoryCards() {
            if (!categoryCardsCol) return;
            const data = MINDMAP_DATASETS[currentDatasetKey];
            categoryCardsCol.innerHTML = '';

            data.categories.forEach(cat => {
                const card = document.createElement('div');
                card.className = `category-card ${cat.id === activeCategoryKey ? 'active' : ''}`;
                card.id = `catCard_${cat.id}`;
                card.onclick = (e) => {
                    e.stopPropagation();
                    selectCategory(cat.id);
                };

                card.innerHTML = `
                    <div class="cat-icon-box"><i class="${cat.icon}"></i></div>
                    <div class="cat-text-group">
                        <div class="cat-number">${cat.count}</div>
                        <div class="cat-label">${cat.label}</div>
                    </div>
                `;
                categoryCardsCol.appendChild(card);
            });
        }

        // Switch Active Category
        function selectCategory(catId) {
            if (activeCategoryKey === catId) return;
            activeCategoryKey = catId;
            const data = MINDMAP_DATASETS[currentDatasetKey];
            data.categories.forEach(c => c.active = (c.id === catId));

            // Select first node in this category
            const nodes = data.childNodes[catId] || [];
            if (nodes.length > 0) {
                selectedNodeId = nodes[0].id;
            }

            renderCategoryCards();
            renderChildNodes();
            updateRightDeckDetails();
            recalculateSplines();
            triggerSynapseSurge(1.6);
        }

        // Render Level 2 Child Nodes (Peacock Fan Bundle)
        function renderChildNodes() {
            if (!childNodesCol) return;
            const data = MINDMAP_DATASETS[currentDatasetKey];
            const nodes = data.childNodes[activeCategoryKey] || [];
            childNodesCol.innerHTML = '';

            // Filter nodes if activeFilterMode is set
            const filtered = nodes.filter(n => {
                if (activeFilterMode === 'all') return true;
                return n.status === activeFilterMode;
            });

            filtered.forEach((node, idx) => {
                const item = document.createElement('div');
                item.className = `child-node-item ${node.id === selectedNodeId ? 'selected' : ''}`;
                item.id = `childNode_${node.id}`;
                item.onclick = (e) => {
                    e.stopPropagation();
                    selectChildNode(node.id);
                };

                const isDisputed = node.status === 'disputed';
                const badgeClass = isDisputed ? 'disputed' : 'safe';

                item.innerHTML = `
                    <span class="node-pin-dot"></span>
                    <span class="node-title-text" title="${node.title}">${node.title}</span>
                    <span class="node-status-badge ${badgeClass}">
                        <span class="status-dot ${node.dot}"></span>
                        <span>${node.statusText}</span>
                    </span>
                `;
                childNodesCol.appendChild(item);
            });
        }

        // Select Child Node
        function selectChildNode(nodeId) {
            selectedNodeId = nodeId;
            const items = childNodesCol ? childNodesCol.querySelectorAll('.child-node-item') : [];
            items.forEach(el => el.classList.remove('selected'));
            const activeEl = document.getElementById(`childNode_${nodeId}`);
            if (activeEl) activeEl.classList.add('selected');

            updateRightDeckDetails();
            recalculateSplines();
            triggerSynapseSurge(2.0);
        }

        // Update Right Inspector Deck with Selected Node Data
        function updateRightDeckDetails() {
            const data = MINDMAP_DATASETS[currentDatasetKey];
            let activeNode = null;

            // Search in active category first
            const list = data.childNodes[activeCategoryKey] || [];
            activeNode = list.find(n => n.id === selectedNodeId);

            // Fallback: search all categories
            if (!activeNode) {
                for (const catKey in data.childNodes) {
                    const match = data.childNodes[catKey].find(n => n.id === selectedNodeId);
                    if (match) { activeNode = match; break; }
                }
            }
            if (!activeNode) return;

            // Update DOM Elements in Deck
            const domainEl = document.getElementById('deckDomainText');
            if (domainEl) domainEl.textContent = activeNode.domain || 'Core System';

            const titleEl = document.getElementById('deckMainTitle');
            if (titleEl) titleEl.textContent = activeNode.title;

            const statusBadge = document.getElementById('deckStatusBadge');
            if (statusBadge) {
                statusBadge.textContent = activeNode.statusText || 'ACTIVE';
                statusBadge.className = `badge-status-active ${activeNode.status === 'disputed' ? 'disputed' : 'safe'}`;
            }

            const sentNum = document.getElementById('deckSentimentNum');
            if (sentNum) sentNum.textContent = (activeNode.sentiment || 45) + '%';

            const sentTag = document.getElementById('deckSentimentTag');
            if (sentTag) {
                const s = activeNode.sentiment || 45;
                sentTag.textContent = s >= 80 ? 'Optimal' : (s >= 50 ? 'Moderate' : 'Critical');
            }

            const sentDelta = document.getElementById('deckSentimentDelta');
            if (sentDelta) {
                const deltaText = activeNode.delta || '-4% last month';
                const isPos = deltaText.includes('+');
                sentDelta.className = `sentiment-delta-pill ${isPos ? 'positive' : 'negative'}`;
                sentDelta.innerHTML = `<i class="fas fa-arrow-trend-${isPos ? 'up' : 'down'}"></i> ${deltaText}`;
            }

            // 2x2 KPI Grid
            const kpiComplaints = document.getElementById('kpiComplaints');
            if (kpiComplaints) kpiComplaints.textContent = activeNode.complaints !== undefined ? activeNode.complaints : 12;

            const kpiRegs = document.getElementById('kpiRegulations');
            if (kpiRegs) kpiRegs.textContent = activeNode.regulations !== undefined ? activeNode.regulations : 2;

            const kpiServ = document.getElementById('kpiServices');
            if (kpiServ) kpiServ.textContent = activeNode.services !== undefined ? activeNode.services : 18;

            const kpiEnt = document.getElementById('kpiEntities');
            if (kpiEnt) kpiEnt.textContent = activeNode.entities !== undefined ? activeNode.entities : 12;

            // AI Analysis
            const aiSub = document.getElementById('deckAiSubheading');
            if (aiSub) {
                aiSub.textContent = activeNode.status === 'disputed' ? 'Propose De-regulation' : 'Compliance & Operational Analysis';
            }
            const aiBody = document.getElementById('deckAiBody');
            if (aiBody) {
                aiBody.textContent = activeNode.analysis || 'Autonomous legal cross-referencing indicates compliance friction across legacy banking and citizen procedural codes.';
            }

            // Sync Context Breadcrumb
            const breadcrumbEl = document.getElementById('breadcrumbKpiText');
            if (breadcrumbEl) {
                breadcrumbEl.textContent = `KPI overview: ${activeNode.title.substring(0, 50)}... [${activeNode.statusText}]`;
            }
        }

        // Recalculate Smooth Cubic Bézier Splines
        function recalculateSplines() {
            if (!svgCurvesGroup) return;
            svgCurvesGroup.innerHTML = '';
            splinePathsData = [];

            const rootEl = document.getElementById('rootCoreNode');
            if (!rootEl) return;

            // Root coordinates relative to canvasWorld
            const rootX = 120 + 38; // right edge of core sphere
            const rootY = 480;

            const data = MINDMAP_DATASETS[currentDatasetKey];
            const categories = data.categories;

            // 1. Splines from Root to each Category Card
            categories.forEach(cat => {
                const cardEl = document.getElementById(`catCard_${cat.id}`);
                if (!cardEl) return;
                const cardX = 380;
                const cardY = cardEl.offsetTop + cardEl.offsetHeight / 2;

                const dx = Math.max(60, (cardX - rootX) * 0.55);
                const d = `M ${rootX} ${rootY} C ${rootX + dx} ${rootY}, ${cardX - dx} ${cardY}, ${cardX} ${cardY}`;

                const pathEl = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                pathEl.setAttribute('d', d);
                pathEl.setAttribute('class', `spline-curve ${cat.id === activeCategoryKey ? 'selected-path' : ''}`);
                svgCurvesGroup.appendChild(pathEl);

                splinePathsData.push({
                    p0: { x: rootX, y: rootY },
                    p1: { x: rootX + dx, y: rootY },
                    p2: { x: cardX - dx, y: cardY },
                    p3: { x: cardX, y: cardY },
                    isActive: cat.id === activeCategoryKey
                });
            });

            // 2. Splines from Active Category Card to all Child Nodes
            const activeCardEl = document.getElementById(`catCard_${activeCategoryKey}`);
            if (!activeCardEl) return;

            const startX = 380 + activeCardEl.offsetWidth;
            const startY = activeCardEl.offsetTop + activeCardEl.offsetHeight / 2;

            const childItems = childNodesCol ? childNodesCol.querySelectorAll('.child-node-item') : [];
            childItems.forEach(item => {
                const isSelected = item.id === `childNode_${selectedNodeId}`;
                const endX = 720;
                const endY = item.offsetTop + item.offsetHeight / 2;

                const dx = Math.max(80, (endX - startX) * 0.55);
                const d = `M ${startX} ${startY} C ${startX + dx} ${startY}, ${endX - dx} ${endY}, ${endX} ${endY}`;

                const pathEl = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                pathEl.setAttribute('d', d);
                pathEl.setAttribute('class', `spline-curve ${isSelected ? 'selected-path' : 'active-branch'}`);
                svgCurvesGroup.appendChild(pathEl);

                splinePathsData.push({
                    p0: { x: startX, y: startY },
                    p1: { x: startX + dx, y: startY },
                    p2: { x: endX - dx, y: endY },
                    p3: { x: endX, y: endY },
                    isActive: isSelected
                });
            });

            // Reset & seed photon particles
            initPhotonParticles();
        }

        // Initialize Traveling Photon Light Sparks
        function initPhotonParticles() {
            photonParticles = [];
            const count = Math.min(60, splinePathsData.length * 2);

            for (let i = 0; i < count; i++) {
                const pathIndex = Math.floor(Math.random() * splinePathsData.length);
                const path = splinePathsData[pathIndex];
                if (!path) continue;

                photonParticles.push({
                    pathIndex: pathIndex,
                    t: Math.random(),
                    speed: 0.003 + Math.random() * 0.004,
                    size: path.isActive ? 2.8 : 2.0,
                    color: path.isActive ? '#fbbf24' : '#38bdf8'
                });
            }
        }

        // Evaluate Cubic Bézier Point
        function getBezierPoint(p0, p1, p2, p3, t) {
            const mt = 1 - t;
            const mt2 = mt * mt;
            const mt3 = mt2 * mt;
            const t2 = t * t;
            const t3 = t2 * t;

            return {
                x: mt3 * p0.x + 3 * mt2 * t * p1.x + 3 * mt * t2 * p2.x + t3 * p3.x,
                y: mt3 * p0.y + 3 * mt2 * t * p1.y + 3 * mt * t2 * p2.y + t3 * p3.y
            };
        }

        // 60FPS Photon Spark Engine
        function startPhotonSparkEngine() {
            if (!photonCanvas || !photonCtx) return;

            function renderPhotons() {
                photonCtx.clearRect(0, 0, photonCanvas.width, photonCanvas.height);

                const currentMultiplier = (isSpeaking || isListening || isThinking) ? 2.5 : synapseSpeedMultiplier;

                photonParticles.forEach(particle => {
                    const path = splinePathsData[particle.pathIndex];
                    if (!path) return;

                    particle.t += particle.speed * currentMultiplier;
                    if (particle.t >= 1) {
                        particle.t = 0;
                        particle.pathIndex = Math.floor(Math.random() * splinePathsData.length);
                    }

                    const pt = getBezierPoint(path.p0, path.p1, path.p2, path.p3, particle.t);

                    // Draw glowing photon spark
                    photonCtx.save();
                    photonCtx.beginPath();
                    photonCtx.arc(pt.x, pt.y, particle.size, 0, Math.PI * 2);
                    photonCtx.fillStyle = path.isActive ? '#fde047' : '#38bdf8';
                    photonCtx.shadowColor = path.isActive ? '#fbbf24' : '#06b6d4';
                    photonCtx.shadowBlur = path.isActive ? 12 : 8;
                    photonCtx.fill();
                    photonCtx.restore();
                });

                requestAnimationFrame(renderPhotons);
            }
            requestAnimationFrame(renderPhotons);
        }

        // Trigger Temporary Synapse Surge
        function triggerSynapseSurge(multiplier = 2.0) {
            synapseSpeedMultiplier = multiplier;
            if (isSynapseSurging) return;
            isSynapseSurging = true;
            setTimeout(() => {
                synapseSpeedMultiplier = 1.0;
                isSynapseSurging = false;
            }, 1800);
        }

        // Canvas Pan & Zoom Setup
        function setupCanvasPanZoom() {
            if (!canvasViewport) return;

            window.addEventListener('resize', () => {
                recalculateSplines();
            });
        }

        function handleCanvasMouseDown(e) {
            // Don't drag if clicking buttons or cards
            if (e.target.closest('.category-card') || e.target.closest('.child-node-item') || e.target.closest('.root-core-container') || e.target.closest('button')) {
                return;
            }
            isPanningCanvas = true;
            canvasViewport.classList.add('is-dragging');
            startPanMouseX = e.clientX - canvasPanX;
            startPanMouseY = e.clientY - canvasPanY;

            function onMouseMove(moveEvent) {
                if (!isPanningCanvas) return;
                canvasPanX = moveEvent.clientX - startPanMouseX;
                canvasPanY = moveEvent.clientY - startPanMouseY;
                applyCanvasTransform();
            }

            function onMouseUp() {
                isPanningCanvas = false;
                canvasViewport.classList.remove('is-dragging');
                window.removeEventListener('mousemove', onMouseMove);
                window.removeEventListener('mouseup', onMouseUp);
            }

            window.addEventListener('mousemove', onMouseMove);
            window.addEventListener('mouseup', onMouseUp);
        }

        function handleCanvasWheel(e) {
            e.preventDefault();
            const rect = canvasViewport.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            const zoomFactor = e.deltaY < 0 ? 1.12 : 0.88;
            const newScale = Math.min(2.2, Math.max(0.4, canvasScale * zoomFactor));

            // Zoom centered on cursor
            canvasPanX -= (mouseX - canvasPanX) * (newScale / canvasScale - 1);
            canvasPanY -= (mouseY - canvasPanY) * (newScale / canvasScale - 1);
            canvasScale = newScale;

            applyCanvasTransform();
        }

        function zoomCanvas(delta) {
            const newScale = Math.min(2.2, Math.max(0.4, canvasScale + delta));
            canvasScale = newScale;
            applyCanvasTransform();
        }

        function resetCanvasTransform() {
            canvasScale = 1.0;
            canvasPanX = 0;
            canvasPanY = 0;
            applyCanvasTransform();
        }

        function applyCanvasTransform() {
            if (!canvasWorld) return;
            canvasWorld.style.transform = `translate(${canvasPanX}px, ${canvasPanY}px) scale(${canvasScale})`;
        }

        // Toolbar Mode Switches
        function switchGraphMode(mode) {
            currentGraphMode = mode;
            const btnRadial = document.getElementById('btnModeGraph');
            const btnHierarchy = document.getElementById('btnModeHierarchy');
            if (btnRadial) btnRadial.classList.toggle('active', mode === 'radial');
            if (btnHierarchy) btnHierarchy.classList.toggle('active', mode === 'hierarchy');

            if (mode === 'hierarchy') {
                // Adjust layout spacing slightly for structured hierarchical feel
                if (categoryCardsCol) categoryCardsCol.style.gap = '28px';
            } else {
                if (categoryCardsCol) categoryCardsCol.style.gap = '20px';
            }
            recalculateSplines();
        }

        function cycleNodeFilter() {
            const modes = ['all', 'safe', 'disputed'];
            const curIdx = modes.indexOf(activeFilterMode);
            activeFilterMode = modes[(curIdx + 1) % modes.length];
            const filterBtn = document.getElementById('btnFilterToggle');
            if (filterBtn) {
                filterBtn.title = `Filter: ${activeFilterMode.toUpperCase()}`;
                filterBtn.classList.toggle('active', activeFilterMode !== 'all');
            }
            renderChildNodes();
            recalculateSplines();
        }

        function toggleDatasetPreset() {
            const nextKey = currentDatasetKey === 'policy' ? 'ultron' : 'policy';
            loadDataset(nextKey);
            triggerSynapseSurge(2.2);
        }

        function handleRootNodeClick() {
            resetCanvasTransform();
            triggerSynapseSurge(2.0);
            const data = MINDMAP_DATASETS[currentDatasetKey];
            const aiBody = document.getElementById('deckAiBody');
            if (aiBody) {
                aiBody.textContent = data.root.analysis;
            }
        }

        // Sync Deck Chat & Voice with Ultron Core
        function syncDeckChatWithCore() {
            const deckInput = document.getElementById('deckChatInput');
            const coreInput = document.getElementById('agentDirectiveInput');

            if (deckInput && coreInput) {
                deckInput.addEventListener('input', () => {
                    coreInput.value = deckInput.value;
                });
            }
        }

        function handleDeckChatKeyDown(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                submitDeckChat();
            }
        }

        function submitDeckChat() {
            const deckInput = document.getElementById('deckChatInput');
            if (!deckInput) return;
            const text = deckInput.value.trim();
            if (!text) return;

            deckInput.value = '';
            triggerSynapseSurge(2.5);

            // Update AI analysis box to show thinking state
            const aiBody = document.getElementById('deckAiBody');
            if (aiBody) {
                aiBody.textContent = `Processing directive: "${text}" through Dual-Core Intelligence...`;
            }

            // Route through existing sendAgentDirective
            if (typeof sendAgentDirective === 'function') {
                sendAgentDirective(text);
            }
        }

        function toggleVoiceRecognitionFromDeck() {
            const deckMicBtn = document.getElementById('deckMicBtn');
            if (isListening) {
                stopListening();
                if (deckMicBtn) deckMicBtn.classList.remove('active');
            } else {
                startListening();
                if (deckMicBtn) deckMicBtn.classList.add('active');
            }
        }

        function cycleAgentMode() {
            const chipName = document.getElementById('chipAgentName');
            if (!chipName) return;
            const agents = ['My agent (Dual-Core)', 'Gemini 3 Flash-Lite', 'Claude 3.5 Sonnet', 'Autonomous Ultron'];
            const cur = chipName.textContent;
            const next = agents[(agents.indexOf(cur) + 1) % agents.length];
            chipName.textContent = next;
        }

        function triggerQuickAiAnalysis() {
            const data = MINDMAP_DATASETS[currentDatasetKey];
            let activeNode = null;
            const list = data.childNodes[activeCategoryKey] || [];
            activeNode = list.find(n => n.id === selectedNodeId) || list[0];
            if (!activeNode) return;

            const prompt = `Analyze compliance risk and operational efficiency for: ${activeNode.title}`;
            const deckInput = document.getElementById('deckChatInput');
            if (deckInput) deckInput.value = prompt;
            submitDeckChat();
        }

        // Modals Logic
        function openNewSimulationModal() {
            const modal = document.getElementById('newSimulationModal');
            if (modal) modal.style.display = 'flex';
        }

        function openSearchModal() {
            const modal = document.getElementById('searchNodesModal');
            if (modal) {
                modal.style.display = 'flex';
                const input = document.getElementById('mindmapSearchInput');
                if (input) {
                    input.value = '';
                    input.focus();
                    handleSearchNodesInput('');
                }
            }
        }

        function openDetailsModal() {
            const data = MINDMAP_DATASETS[currentDatasetKey];
            let activeNode = null;
            const list = data.childNodes[activeCategoryKey] || [];
            activeNode = list.find(n => n.id === selectedNodeId) || list[0];
            if (!activeNode) return;

            const modal = document.getElementById('nodeDetailsModal');
            const titleEl = document.getElementById('detailsModalTitle');
            const bodyEl = document.getElementById('detailsModalBody');

            if (titleEl) titleEl.innerHTML = `<i class="fas fa-file-contract"></i> ${activeNode.title}`;
            if (bodyEl) {
                bodyEl.innerHTML = `
                    <div style="margin-bottom:12px;"><strong>Domain Category:</strong> <span style="color:#38bdf8;">${activeNode.domain}</span></div>
                    <div style="margin-bottom:12px;"><strong>Current Status:</strong> <span style="color:${activeNode.status === 'disputed' ? '#f87171' : '#34d399'}; font-weight:700;">${activeNode.statusText}</span></div>
                    <div style="margin-bottom:12px;"><strong>Sentiment / Performance Score:</strong> <strong>${activeNode.sentiment}%</strong> (${activeNode.delta || 'Nominal'})</div>
                    <div style="margin-bottom:14px; padding:12px; background:rgba(15,23,42,0.6); border:1px solid rgba(56,189,248,0.2); border-radius:12px;">
                        <div style="color:#38bdf8; font-size:0.75rem; font-weight:700; margin-bottom:6px;"><i class="fas fa-wand-magic-sparkles"></i> AI Deep Heuristic Synthesis:</div>
                        <p style="margin:0; line-height:1.5;">${activeNode.analysis}</p>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:0.78rem;">
                        <div style="padding:10px; background:rgba(255,255,255,0.03); border-radius:8px;">Public Recommendations: <strong>${activeNode.complaints}</strong></div>
                        <div style="padding:10px; background:rgba(255,255,255,0.03); border-radius:8px;">Related Regulations: <strong>${activeNode.regulations}</strong></div>
                        <div style="padding:10px; background:rgba(255,255,255,0.03); border-radius:8px;">Linked Services: <strong>${activeNode.services}</strong></div>
                        <div style="padding:10px; background:rgba(255,255,255,0.03); border-radius:8px;">Entities Involved: <strong>${activeNode.entities}</strong></div>
                    </div>
                `;
            }
            if (modal) modal.style.display = 'flex';
        }

        function closeModal(id) {
            const modal = document.getElementById(id);
            if (modal) modal.style.display = 'none';
        }

        function closeModalOnOverlay(e, id) {
            if (e.target.id === id) {
                closeModal(id);
            }
        }

        function submitNewSimulation() {
            const title = (document.getElementById('simTitleInput').value || '').trim();
            const cat = document.getElementById('simCategorySelect').value || 'laws';
            const status = document.getElementById('simStatusSelect').value || 'safe';
            const sentiment = parseInt(document.getElementById('simSentimentInput').value || '75', 10);
            const entities = parseInt(document.getElementById('simEntitiesInput').value || '6', 10);
            const notes = (document.getElementById('simNotesInput').value || '').trim();

            if (!title) {
                alert('Please enter a simulation directive title.');
                return;
            }

            const data = MINDMAP_DATASETS[currentDatasetKey];
            if (!data.childNodes[cat]) data.childNodes[cat] = [];

            const newId = 'sim_' + Date.now();
            const isDisputed = status === 'disputed';
            const newNode = {
                id: newId,
                title: title,
                statusText: isDisputed ? 'DISPUTED' : (status === 'pending' ? 'PENDING' : 'SAFE:SET'),
                status: status,
                dot: isDisputed ? 'red' : (status === 'pending' ? 'yellow' : 'green'),
                domain: 'Custom Simulation',
                sentiment: sentiment,
                delta: '+1% simulated',
                complaints: Math.floor(Math.random() * 8),
                regulations: 2,
                services: 12,
                entities: entities,
                analysis: notes || `Custom simulation created for ${title}. Cross-jurisdiction heuristic checks passed with ${sentiment}% compliance confidence.`
            };

            data.childNodes[cat].unshift(newNode);
            selectCategory(cat);
            selectChildNode(newId);
            closeModal('newSimulationModal');
            triggerSynapseSurge(3.0);
        }

        function handleSearchNodesInput(val) {
            const list = document.getElementById('searchResultsList');
            if (!list) return;
            list.innerHTML = '';
            const q = val.toLowerCase().trim();

            const data = MINDMAP_DATASETS[currentDatasetKey];
            const allNodes = [];
            for (const catKey in data.childNodes) {
                data.childNodes[catKey].forEach(n => allNodes.push({ ...n, catKey }));
            }

            const matches = allNodes.filter(n => {
                if (!q) return true;
                return n.title.toLowerCase().includes(q) || n.domain.toLowerCase().includes(q) || n.statusText.toLowerCase().includes(q);
            });

            if (matches.length === 0) {
                list.innerHTML = '<div style="padding:12px; color:#94a3b8; font-size:0.8rem; text-align:center;">No matching nodes located.</div>';
                return;
            }

            matches.slice(0, 10).forEach(node => {
                const item = document.createElement('div');
                item.className = 'search-result-item';
                item.onclick = () => {
                    selectCategory(node.catKey);
                    selectChildNode(node.id);
                    closeModal('searchNodesModal');
                };
                item.innerHTML = `
                    <div class="search-item-left">
                        <span class="search-item-title">${node.title}</span>
                        <span class="search-item-domain">${node.domain}</span>
                    </div>
                    <span class="node-status-badge ${node.status === 'disputed' ? 'disputed' : 'safe'}">
                        <span class="status-dot ${node.dot}"></span>
                        <span>${node.statusText}</span>
                    </span>
                `;
                list.appendChild(item);
            });
        }

        // Initialize on DOMContentLoaded
        document.addEventListener('DOMContentLoaded', () => {
            initNeuralMindmap();
        });
"""

# Insert js_engine right after <script> tag
html = html[:idx + len(script_tag)] + "\n" + js_engine + "\n" + html[idx + len(script_tag):]
print("JS engine inserted.")

# Let's save the modified voice_wave.html
with open(VW_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved voice_wave.html successfully!")

