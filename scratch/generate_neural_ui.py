# scratch/generate_neural_ui.py
import os
import re

TEMPLATES_DIR = r"c:\Users\MrHat\app\ai_ultran\templates"
VW_PATH = os.path.join(TEMPLATES_DIR, "voice_wave.html")

print("Building Neural Mindmap UI...")

css_code = """
        /* ==========================================================================
           CENTRAL AI POLICY PLATFORM & NEURAL MINDMAP INTERFACE (HIGH-PRECISION UI)
           ========================================================================== */
        :root {
            --plat-bg: #04070d;
            --plat-card-bg: rgba(9, 16, 28, 0.88);
            --plat-card-border: rgba(56, 189, 248, 0.22);
            --plat-teal: #06b6d4;
            --plat-cyan: #38bdf8;
            --plat-gold: #f59e0b;
            --plat-rose: #f43f5e;
            --plat-emerald: #10b981;
            --plat-text-main: #f8fafc;
            --plat-text-muted: #94a3b8;
            --plat-text-sub: #64748b;
        }

        /* Master Container */
        .central-platform-container {
            position: absolute;
            inset: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background: var(--plat-bg);
            background-image: 
                radial-gradient(circle at 18% 50%, rgba(6, 182, 212, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 55%),
                radial-gradient(circle at 85% 30%, rgba(139, 92, 246, 0.08) 0%, transparent 45%);
            z-index: 5;
            display: flex;
            user-select: none;
            -webkit-user-select: none;
            cursor: default;
        }

        /* Subtle High-Tech Neural Grid */
        .central-platform-container::before {
            content: '';
            position: absolute;
            inset: 0;
            background-size: 40px 40px;
            background-image: 
                linear-gradient(to right, rgba(56, 189, 248, 0.025) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(56, 189, 248, 0.025) 1px, transparent 1px);
            pointer-events: none;
            z-index: 1;
        }

        /* Top Global HUD Bar */
        .platform-top-bar {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 68px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 32px;
            z-index: 100;
            pointer-events: auto;
        }

        .brand-group {
            display: flex;
            align-items: center;
            gap: 14px;
            cursor: pointer;
            transition: opacity 0.2s ease;
        }
        .brand-group:hover {
            opacity: 0.9;
        }

        .brand-logo-icon {
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.6));
            animation: logoGlowPulse 4s infinite ease-in-out;
        }
        @keyframes logoGlowPulse {
            0%, 100% { filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.5)); transform: scale(1); }
            50% { filter: drop-shadow(0 0 16px rgba(6, 182, 212, 0.85)); transform: scale(1.03); }
        }

        .brand-text-col {
            display: flex;
            flex-direction: column;
        }
        .brand-title {
            font-size: 0.96rem;
            font-weight: 700;
            letter-spacing: 0.3px;
            color: #ffffff;
            line-height: 1.2;
        }
        .brand-subtitle {
            font-size: 0.65rem;
            font-weight: 800;
            letter-spacing: 1.2px;
            color: var(--plat-teal);
            display: flex;
            align-items: center;
            gap: 6px;
            margin-top: 2px;
            text-transform: uppercase;
        }
        .live-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--plat-teal);
            box-shadow: 0 0 8px var(--plat-teal);
            animation: liveDotPulse 1.8s infinite;
        }
        @keyframes liveDotPulse {
            0%, 100% { opacity: 0.5; transform: scale(0.9); }
            50% { opacity: 1; transform: scale(1.3); }
        }

        /* Floating Dark Glass Toolbar (Center) */
        .floating-toolbar {
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 5px 12px;
            background: rgba(10, 18, 30, 0.82);
            border: 1px solid rgba(56, 189, 248, 0.22);
            border-radius: 9999px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.1);
            z-index: 105;
        }

        .toolbar-pill-btn {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: none;
            background: transparent;
            color: var(--plat-text-muted);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .toolbar-pill-btn:hover {
            color: #ffffff;
            background: rgba(56, 189, 248, 0.15);
            transform: scale(1.08);
        }
        .toolbar-pill-btn.active {
            color: var(--plat-teal);
            background: rgba(6, 182, 212, 0.2);
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.4);
        }

        .toolbar-divider {
            width: 1px;
            height: 16px;
            background: rgba(255, 255, 255, 0.12);
            margin: 0 4px;
        }

        /* Top Actions Group (Right) */
        .top-actions-group {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .btn-new-simulation {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.22);
            color: #ffffff;
            padding: 7px 18px;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.25s ease;
            backdrop-filter: blur(10px);
        }
        .btn-new-simulation:hover {
            background: rgba(255, 255, 255, 0.16);
            border-color: rgba(255, 255, 255, 0.4);
            transform: translateY(-1px);
            box-shadow: 0 4px 16px rgba(255, 255, 255, 0.15);
        }

        .dataset-switch-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(6, 182, 212, 0.12);
            border: 1px solid rgba(6, 182, 212, 0.35);
            color: var(--plat-cyan);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.76rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .dataset-switch-pill:hover {
            background: rgba(6, 182, 212, 0.25);
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.4);
        }

        .user-avatar-pill {
            display: flex;
            align-items: center;
            cursor: pointer;
        }
        .avatar-circle {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0284c7, #4f46e5);
            border: 1.5px solid rgba(56, 189, 248, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
        }
        .avatar-text {
            font-size: 0.72rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 0.5px;
        }
        .online-indicator {
            position: absolute;
            bottom: -1px;
            right: -1px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--plat-emerald);
            border: 1.5px solid #04070d;
            box-shadow: 0 0 6px var(--plat-emerald);
        }

        .icon-action-btn {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(255, 255, 255, 0.04);
            color: var(--plat-text-muted);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .icon-action-btn:hover {
            color: #ffffff;
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }

        /* Context Breadcrumb Pill (Beneath Top Bar) */
        .breadcrumb-kpi-pill {
            position: absolute;
            top: 76px;
            right: 470px;
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            background: rgba(10, 18, 30, 0.75);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            color: #cbd5e1;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            z-index: 50;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
            max-width: 520px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .breadcrumb-kpi-pill i {
            color: var(--plat-cyan);
            font-size: 0.8rem;
        }

        /* Interactive Neural Canvas Viewport (Pannable & Zoomable) */
        .neural-canvas-viewport {
            position: absolute;
            top: 0;
            left: 0;
            right: 450px;
            bottom: 0;
            overflow: hidden;
            z-index: 10;
            cursor: grab;
        }
        .neural-canvas-viewport.is-dragging {
            cursor: grabbing;
        }

        .neural-canvas-world {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            transform-origin: 0 0;
            will-change: transform;
        }

        /* SVG Spline Curves Layer */
        .canvas-svg-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 2500px;
            height: 2000px;
            pointer-events: none;
            z-index: 12;
            overflow: visible;
        }

        .spline-curve {
            fill: none;
            stroke: rgba(38, 92, 114, 0.45);
            stroke-width: 1.2;
            transition: stroke 0.3s ease, stroke-width 0.3s ease, opacity 0.3s ease;
        }
        .spline-curve.active-branch {
            stroke: url(#curveGradientNormal);
            stroke-width: 1.6;
            opacity: 0.9;
        }
        .spline-curve.selected-path {
            stroke: url(#curveGradientActive);
            stroke-width: 2.4;
            filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));
            opacity: 1;
        }

        /* Canvas Photon Layer */
        .canvas-photon-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 2500px;
            height: 2000px;
            pointer-events: none;
            z-index: 13;
        }

        /* HTML Nodes Layer */
        .canvas-nodes-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 2500px;
            height: 2000px;
            z-index: 15;
            pointer-events: none;
        }
        .canvas-nodes-layer * {
            pointer-events: auto;
        }

        /* Root Planetary Core Node (Left) */
        .root-core-container {
            position: absolute;
            left: 120px;
            top: 480px;
            transform: translate(-50%, -50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 25;
            width: 260px;
            height: 260px;
        }

        .core-aura-glow {
            position: absolute;
            width: 240px;
            height: 240px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(124, 58, 237, 0.28) 0%, rgba(6, 182, 212, 0.15) 45%, transparent 72%);
            filter: blur(12px);
            pointer-events: none;
            animation: coreAuraBreathe 4s infinite ease-in-out;
        }
        @keyframes coreAuraBreathe {
            0%, 100% { transform: scale(0.92); opacity: 0.7; }
            50% { transform: scale(1.1); opacity: 1; }
        }

        .core-orbit-ring {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
        }
        .ring-dashed {
            width: 140px;
            height: 140px;
            border: 1px dashed rgba(56, 189, 248, 0.35);
            animation: spinOrbitCW 24s linear infinite;
        }
        .ring-solid {
            width: 170px;
            height: 170px;
            border: 1px solid rgba(139, 92, 246, 0.2);
            animation: spinOrbitCCW 32s linear infinite;
        }
        @keyframes spinOrbitCW {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        @keyframes spinOrbitCCW {
            from { transform: rotate(360deg); }
            to { transform: rotate(0deg); }
        }

        .core-planet-sphere {
            width: 76px;
            height: 76px;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #a78bfa 0%, #6366f1 35%, #1e1b4b 85%, #050814 100%);
            box-shadow: 
                0 0 35px rgba(139, 92, 246, 0.65),
                0 0 70px rgba(6, 182, 212, 0.3),
                inset -8px -8px 20px rgba(0, 0, 0, 0.8),
                inset 6px 6px 14px rgba(255, 255, 255, 0.6);
            position: relative;
            z-index: 5;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease;
        }
        .root-core-container:hover .core-planet-sphere {
            transform: scale(1.08);
            box-shadow: 0 0 50px rgba(139, 92, 246, 0.9), 0 0 90px rgba(6, 182, 212, 0.5);
        }

        .core-node-label {
            margin-top: 14px;
            font-size: 0.72rem;
            color: rgba(255, 255, 255, 0.9);
            text-align: center;
            line-height: 1.3;
            letter-spacing: 0.2px;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.9);
            z-index: 10;
        }
        .core-node-label strong {
            color: #ffffff;
            font-weight: 800;
        }

        .core-status-tag {
            margin-top: 6px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 2px 8px;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 9999px;
            font-size: 0.62rem;
            font-weight: 700;
            color: #94a3b8;
            letter-spacing: 0.8px;
            z-index: 10;
        }
        .status-dot {
            width: 5px;
            height: 5px;
            border-radius: 50%;
        }
        .status-dot.green { background: #10b981; box-shadow: 0 0 6px #10b981; }
        .status-dot.red { background: #ef4444; box-shadow: 0 0 6px #ef4444; }
        .status-dot.yellow { background: #f59e0b; box-shadow: 0 0 6px #f59e0b; }
        .status-dot.orange { background: #f97316; box-shadow: 0 0 6px #f97316; }

        /* Level 1 Category Cards Column */
        .category-cards-col {
            position: absolute;
            left: 380px;
            top: 260px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            z-index: 20;
        }

        .category-card {
            min-width: 150px;
            padding: 10px 16px;
            background: rgba(12, 20, 32, 0.82);
            border: 1px solid rgba(56, 189, 248, 0.22);
            border-radius: 12px;
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            position: relative;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }
        .category-card:hover {
            border-color: rgba(56, 189, 248, 0.5);
            background: rgba(16, 28, 46, 0.92);
            transform: translateX(4px);
            box-shadow: 0 6px 24px rgba(6, 182, 212, 0.25);
        }
        .category-card.active {
            border-color: rgba(251, 191, 36, 0.95);
            background: rgba(18, 30, 48, 0.95);
            box-shadow: 
                0 0 30px rgba(245, 158, 11, 0.35),
                0 0 15px rgba(6, 182, 212, 0.3),
                inset 0 0 12px rgba(251, 191, 36, 0.15);
            transform: translateX(8px);
        }

        .category-card.active::after {
            content: '';
            position: absolute;
            right: -6px;
            top: 50%;
            transform: translateY(-50%);
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #fbbf24;
            box-shadow: 0 0 14px #fbbf24;
            border: 2px solid #04070d;
        }

        .cat-icon-box {
            font-size: 0.95rem;
            color: var(--plat-cyan);
            width: 24px;
            text-align: center;
        }
        .category-card.active .cat-icon-box {
            color: #fbbf24;
        }

        .cat-text-group {
            display: flex;
            flex-direction: column;
        }
        .cat-number {
            font-size: 1.05rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.1;
        }
        .cat-label {
            font-size: 0.65rem;
            color: var(--plat-text-muted);
            letter-spacing: 0.2px;
            margin-top: 2px;
        }

        /* Level 2 Fanning Child Nodes Column */
        .child-nodes-col {
            position: absolute;
            left: 720px;
            top: 80px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            z-index: 20;
            min-width: 320px;
        }

        .child-node-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 4px 10px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
        }
        .child-node-item:hover {
            background: rgba(56, 189, 248, 0.1);
            transform: translateX(4px);
        }
        .child-node-item.selected {
            background: rgba(56, 189, 248, 0.18);
            border: 1px solid rgba(56, 189, 248, 0.4);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.3);
            transform: translateX(6px);
        }

        .node-pin-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--plat-cyan);
            box-shadow: 0 0 8px var(--plat-cyan);
            border: 1px solid #04070d;
            flex-shrink: 0;
            transition: transform 0.2s ease;
        }
        .child-node-item:hover .node-pin-dot,
        .child-node-item.selected .node-pin-dot {
            transform: scale(1.4);
            background: #ffffff;
            box-shadow: 0 0 12px var(--plat-cyan);
        }

        .node-title-text {
            font-size: 0.76rem;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.88);
            letter-spacing: 0.15px;
            white-space: nowrap;
            max-width: 260px;
            overflow: hidden;
            text-overflow: ellipsis;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.8);
        }
        .child-node-item.selected .node-title-text {
            color: #ffffff;
            font-weight: 700;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.7);
        }

        .node-status-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 1px 6px;
            border-radius: 4px;
            font-size: 0.58rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #94a3b8;
            flex-shrink: 0;
        }
        .node-status-badge.disputed {
            border-color: rgba(239, 68, 68, 0.4);
            color: #f87171;
            background: rgba(239, 68, 68, 0.15);
        }
        .node-status-badge.safe {
            border-color: rgba(16, 185, 129, 0.4);
            color: #34d399;
            background: rgba(16, 185, 129, 0.12);
        }

        /* Right Inspector & Intelligent AI Assistant Deck */
        .inspector-deck-panel {
            position: absolute;
            top: 76px;
            right: 24px;
            width: 420px;
            bottom: 24px;
            background: var(--plat-card-bg);
            border: 1px solid var(--plat-card-border);
            border-radius: 26px;
            backdrop-filter: blur(28px);
            -webkit-backdrop-filter: blur(28px);
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85), 0 0 40px rgba(6, 182, 212, 0.1);
            display: flex;
            flex-direction: column;
            padding: 22px;
            gap: 16px;
            z-index: 40;
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: rgba(56, 189, 248, 0.25) transparent;
        }
        .inspector-deck-panel::-webkit-scrollbar {
            width: 5px;
        }
        .inspector-deck-panel::-webkit-scrollbar-thumb {
            background: rgba(56, 189, 248, 0.25);
            border-radius: 4px;
        }

        /* Deck Header */
        .deck-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .deck-domain-chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--plat-cyan);
            letter-spacing: 0.3px;
        }
        .deck-domain-chip i {
            font-size: 0.85rem;
        }

        .deck-explore-btn {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--plat-text-muted);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: all 0.2s ease;
        }
        .deck-explore-btn:hover {
            color: #ffffff;
            transform: translateX(2px);
        }

        /* Title Wrapper */
        .deck-title-wrapper {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .deck-main-title {
            font-size: 1.08rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.35;
            letter-spacing: -0.2px;
        }

        .deck-meta-row {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        .badge-status-active {
            font-size: 0.62rem;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 4px;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #34d399;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }
        .deck-date-text {
            font-size: 0.68rem;
            color: var(--plat-text-sub);
        }

        /* Deck Cards General */
        .deck-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(56, 189, 248, 0.15);
            border-radius: 16px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        /* Sentiment Rate Card */
        .sentiment-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .card-kicker {
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--plat-text-muted);
            letter-spacing: 0.5px;
        }
        .sentiment-tag {
            font-size: 0.62rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 9999px;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.35);
            color: #fbbf24;
            letter-spacing: 0.5px;
        }

        .sentiment-val-row {
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .sentiment-big-num {
            font-size: 1.85rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1;
            letter-spacing: -0.5px;
        }
        .sentiment-delta-pill {
            font-size: 0.72rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        .sentiment-delta-pill.negative {
            color: var(--plat-rose);
        }
        .sentiment-delta-pill.positive {
            color: var(--plat-emerald);
        }
        .sentiment-delta-pill span {
            font-size: 0.62rem;
            color: var(--plat-text-sub);
            font-weight: 500;
        }

        /* Dynamic Equalizer Histogram */
        .histogram-container {
            flex: 1;
            height: 38px;
            display: flex;
            align-items: flex-end;
            gap: 2.5px;
            padding: 2px 4px;
            overflow: hidden;
        }
        .hist-bar {
            width: 3.2px;
            min-height: 4px;
            border-radius: 2px;
            background: linear-gradient(to top, rgba(245, 158, 11, 0.25), rgba(251, 191, 36, 0.95));
            transition: height 0.08s ease;
        }

        /* 2x2 Quick KPI Grid */
        .deck-kpi-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .kpi-mini-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(56, 189, 248, 0.14);
            border-radius: 14px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            transition: all 0.2s ease;
        }
        .kpi-mini-card:hover {
            border-color: rgba(56, 189, 248, 0.35);
            background: rgba(18, 28, 48, 0.75);
            transform: translateY(-2px);
        }

        .kpi-icon-row {
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--plat-cyan);
        }
        .kpi-icon-row i {
            font-size: 0.85rem;
            color: var(--plat-cyan);
        }
        .kpi-num {
            font-size: 1.15rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1;
        }
        .kpi-label {
            font-size: 0.65rem;
            font-weight: 600;
            color: var(--plat-text-muted);
            line-height: 1.25;
        }

        /* AI Analysis Card */
        .ai-analysis-card {
            background: rgba(12, 22, 38, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.25);
            position: relative;
            overflow: hidden;
        }
        .ai-analysis-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--plat-teal), #8b5cf6, var(--plat-cyan));
        }

        .ai-analysis-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .ai-spark-title {
            font-size: 0.76rem;
            font-weight: 800;
            color: var(--plat-cyan);
            display: flex;
            align-items: center;
            gap: 6px;
            letter-spacing: 0.5px;
        }
        .ai-analysis-sub {
            font-size: 0.85rem;
            font-weight: 700;
            color: #ffffff;
            margin-top: 2px;
        }
        .ai-analysis-body {
            font-size: 0.73rem;
            color: #cbd5e1;
            line-height: 1.45;
            user-select: text !important;
            -webkit-user-select: text !important;
            max-height: 140px;
            overflow-y: auto;
            scrollbar-width: thin;
        }

        /* Bottom Integrated Chat & Voice Dock */
        .deck-chat-dock {
            margin-top: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
            background: rgba(10, 18, 30, 0.95);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 18px;
            padding: 10px 12px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
        }

        .chat-input-pill-wrapper {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        #deckChatInput {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: #ffffff;
            font-size: 0.85rem;
            font-family: inherit;
            user-select: text !important;
            -webkit-user-select: text !important;
            cursor: text;
        }
        #deckChatInput::placeholder {
            color: rgba(148, 163, 184, 0.65);
            font-size: 0.82rem;
        }

        .deck-mic-btn {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 1px solid rgba(56, 189, 248, 0.35);
            background: rgba(15, 23, 42, 0.85);
            color: var(--plat-cyan);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.78rem;
        }
        .deck-mic-btn:hover {
            color: #ffffff;
            border-color: var(--plat-cyan);
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
            transform: scale(1.08);
        }
        .deck-mic-btn.active {
            background: rgba(239, 68, 68, 0.25);
            border-color: #ef4444;
            color: #ef4444;
            animation: pulseMic 1.4s infinite;
        }
        @keyframes pulseMic {
            0%, 100% { box-shadow: 0 0 8px rgba(239, 68, 68, 0.4); transform: scale(1); }
            50% { box-shadow: 0 0 16px rgba(239, 68, 68, 0.9); transform: scale(1.1); }
        }

        .deck-send-btn {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: none;
            background: linear-gradient(135deg, var(--plat-teal), #2563eb);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.78rem;
            box-shadow: 0 2px 10px rgba(6, 182, 212, 0.3);
        }
        .deck-send-btn:hover {
            transform: scale(1.08);
            box-shadow: 0 0 14px rgba(37, 99, 235, 0.7);
        }

        .chat-chips-row {
            display: flex;
            align-items: center;
            gap: 6px;
            padding-top: 4px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
        }
        .chip-item {
            padding: 3px 9px;
            border-radius: 9999px;
            font-size: 0.64rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .agent-chip {
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.3);
            color: var(--plat-cyan);
        }
        .agent-chip:hover {
            background: rgba(56, 189, 248, 0.22);
        }
        .badge-chip {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: var(--plat-text-muted);
        }
        .action-chip {
            margin-left: auto;
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #34d399;
        }
        .action-chip:hover {
            background: rgba(16, 185, 129, 0.22);
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
        }

        /* Modals */
        .platform-modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(2, 6, 14, 0.85);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            z-index: 200;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            animation: modalFadeIn 0.25s ease;
        }
        @keyframes modalFadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .platform-modal-card {
            width: min(94vw, 540px);
            background: rgba(12, 20, 34, 0.96);
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 22px;
            padding: 24px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85), 0 0 35px rgba(6, 182, 212, 0.2);
            display: flex;
            flex-direction: column;
            gap: 18px;
            user-select: text !important;
            -webkit-user-select: text !important;
        }

        .modal-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .modal-title {
            font-size: 1.05rem;
            font-weight: 800;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .modal-title i {
            color: var(--plat-cyan);
        }
        .modal-close-btn {
            background: transparent;
            border: none;
            color: var(--plat-text-muted);
            font-size: 1.1rem;
            cursor: pointer;
            transition: color 0.2s ease;
        }
        .modal-close-btn:hover {
            color: #ffffff;
        }

        .modal-body {
            display: flex;
            flex-direction: column;
            gap: 14px;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .form-group label {
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--plat-text-muted);
            letter-spacing: 0.5px;
        }
        .form-group input,
        .form-group select,
        .form-group textarea {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 10px;
            padding: 9px 12px;
            color: #ffffff;
            font-size: 0.85rem;
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s ease;
        }
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            border-color: var(--plat-cyan);
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.3);
        }

        .modal-footer {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 6px;
        }
        .modal-btn {
            padding: 9px 20px;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .modal-btn.secondary {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #cbd5e1;
        }
        .modal-btn.secondary:hover {
            background: rgba(255, 255, 255, 0.14);
            color: #ffffff;
        }
        .modal-btn.primary {
            background: linear-gradient(135deg, var(--plat-teal), #2563eb);
            border: none;
            color: #ffffff;
            box-shadow: 0 4px 16px rgba(6, 182, 212, 0.35);
        }
        .modal-btn.primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 22px rgba(37, 99, 235, 0.6);
        }

        /* Search Modal List */
        .search-card {
            width: min(94vw, 560px);
        }
        .search-input-box {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 14px;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 12px;
        }
        .search-input-box i {
            color: var(--plat-cyan);
            font-size: 0.95rem;
        }
        #mindmapSearchInput {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: #ffffff;
            font-size: 0.9rem;
            font-family: inherit;
        }
        .search-results-list {
            max-height: 280px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-top: 8px;
        }
        .search-result-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 12px;
            border-radius: 8px;
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.08);
            cursor: pointer;
            transition: all 0.18s ease;
        }
        .search-result-item:hover {
            background: rgba(56, 189, 248, 0.15);
            border-color: rgba(56, 189, 248, 0.4);
            transform: translateX(4px);
        }
        .search-item-left {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .search-item-title {
            font-size: 0.8rem;
            font-weight: 700;
            color: #ffffff;
        }
        .search-item-domain {
            font-size: 0.65rem;
            color: var(--plat-cyan);
        }

        /* Responsive Breakpoints */
        @media (max-width: 1200px) {
            .inspector-deck-panel {
                width: 360px;
                right: 16px;
            }
            .neural-canvas-viewport {
                right: 380px;
            }
            .breadcrumb-kpi-pill {
                right: 400px;
                max-width: 340px;
            }
        }

        @media (max-width: 860px) {
            .inspector-deck-panel {
                position: fixed;
                bottom: 0;
                top: auto;
                left: 0;
                right: 0;
                width: 100%;
                height: 52vh;
                border-radius: 24px 24px 0 0;
            }
            .neural-canvas-viewport {
                right: 0;
                bottom: 52vh;
            }
            .breadcrumb-kpi-pill {
                display: none;
            }
            .floating-toolbar {
                display: none;
            }
        }
"""

print(f"CSS length: {len(css_code)} chars")

