# AI ULTRAN — Intelligent Voice Assistant

**AI ULTRAN** is a web-based personal AI assistant that understands natural language, interacts via voice and text, remembers user preferences, summarizes documents, and executes approved productivity tasks with strict security controls.

Built with **Python**, **Django**, **Web Technologies (HTML5/CSS3/JavaScript)**, and **Google Gemini LLM**.

---

## 🏛️ System Architecture

```
[ User Browser / Microphone / Audio ]
              │ (Voice / Text commands)
              ▼
    [ Django Web Layer ]
    • Authentication & CSRF
    • Session Isolation
    • REST API Endpoints
              │
              ├──► [ AI Reasoning Layer ]
              │    • Google Gemini API (google-genai)
              │    • Contextual multi-turn history
              │    • Structured JSON action extraction
              │    • Local offline fallback intelligence
              │
              └──► [ Action Controller ]
                   • Security Allowlist validation
                   • Blocks arbitrary shell/code execution
                   • Audit trail logging (ActionLog)
                   • Reminders & Task scheduling
```

---

## ✨ Implemented Features by Module

### Module 1 — AI Chat Assistant
- Natural conversational interactions powered by Google Gemini (`gemini-2.0-flash`).
- Multi-turn conversation awareness with past history context.
- Copy answers with one-click code formatting.
- Clear conversations and review historical dialogues.

### Module 2 — Two-Way Voice Interaction
- **Speech-to-Text (STT)**: Real-time microphone capture via Web Speech API (`webkitSpeechRecognition`).
- **Text-to-Speech (TTS)**: Spoken voice responses via the browser's `SpeechSynthesis` engine.
- Configurable speech rate (speed), pitch, and gender preference (Male / Female / Default).
- One-click mute/unmute toggle in the chat header.

### Module 3 — Personal Productivity & Reminders
- Natural language reminder scheduling (e.g., *"Remind me to study Python tomorrow at 7 PM"*).
- Automatic date/time parsing and task priority assignment.
- Dedicated dashboard with upcoming agenda and completed task tracking.
- Full CRUD: Create, View, Complete, Edit, and Delete reminders.

### Module 4 — Document Intelligence
- Secure document upload supporting **PDF**, **Markdown (.md)**, and **Plain Text (.txt)** up to 10 MB.
- Extracted text analysis powered by Gemini LLM and `PyPDF2`.
- Interactive interrogation page: Ask questions, request executive summaries, and extract key action items.
- Strict per-user file isolation.

### Module 5 — Personalization & AI Memory
- Personalized response style preferences: **Concise**, **Detailed**, **Casual**, or **Formal**.
- Timezone configuration for accurate date/time scheduling.
- Privacy toggle to disable conversation history or purge past dialogues.
- Complete data removal ("Delete Account") in Danger Zone.

### Module 6 — Device Integration & Action Controller
- Strict allowlist governing permissible operations (`create_reminder`, `list_reminders`, etc.).
- Prohibits arbitrary shell commands, code execution (`eval`), and unauthorized hardware probing.
- Immutable `ActionLog` auditing all requested, approved, and rejected tasks.
- Architecture ready for Android companion integration via clean REST API endpoints.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Google Chrome, Microsoft Edge, or Safari (for native Web Speech API support)

### 2. Installation

Navigate to the project directory:
```bash
cd C:\Users\MrHat\app\ai_ultran
```

Install requirements:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Inspect or edit `.env` in the root folder:
```env
DJANGO_SECRET_KEY=ai-ultran-super-secret-key-change-in-production-2026
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash
```

> **Note on Offline / Local Mode**: If `GEMINI_API_KEY` is not provided or quota is exceeded, AI ULTRAN automatically switches to its local fallback engine. Reminders, dashboard productivity, and voice recognition remain functional!

### 4. Database Setup & Demo Account
Apply database migrations:
```bash
python manage.py migrate
```

A demo user is ready to use:
- **Username**: `demo`
- **Password**: `ultran123`

### 5. Start the Server
```bash
python manage.py runserver
```
Open your browser to: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧪 Testing Suite
To execute the automated test suite covering all security, voice, isolation, and reminder scenarios:
```bash
python manage.py test assistant
```


