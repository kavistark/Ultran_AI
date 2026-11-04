import os
import sys
import time
import subprocess
import logging
import ctypes
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Try importing psutil and pyautogui safely
try:
    import psutil
except ImportError:
    psutil = None

try:
    import pyautogui
    # Allow background automation even if cursor is at corner or headless
    pyautogui.FAILSAFE = False
except ImportError:
    pyautogui = None


# Known executable and application path aliases on Windows
APP_ALIASES = {
    'chrome': ['chrome', 'google chrome', r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'],
    'firefox': ['firefox', r'C:\Program Files\Mozilla Firefox\firefox.exe'],
    'edge': ['msedge', 'microsoft-edge:'],
    'code': ['code', 'vscode', 'visual studio code', r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe'],
    'notepad': ['notepad.exe', 'notepad'],
    'calculator': ['calc.exe', 'calc'],
    'terminal': ['wt.exe', 'powershell.exe', 'cmd.exe'],
    'cmd': ['cmd.exe'],
    'powershell': ['powershell.exe'],
    'spotify': ['spotify', r'C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe'],
    'explorer': ['explorer.exe'],
    'settings': ['ms-settings:'],
    'taskmgr': ['taskmgr.exe'],
}


def open_application(app_name: str) -> Dict[str, Any]:
    """Launch or focus a desktop application by name or common alias."""
    if not app_name:
        return {'success': False, 'message': 'Application name must be specified.'}

    target = app_name.lower().strip()
    executable = None

    # Resolve from alias catalog
    for key, aliases in APP_ALIASES.items():
        if target == key or target in aliases or key in target:
            executable = aliases[0]
            break

    if not executable:
        executable = target

    # Expand environment variables like %USERNAME%
    if '%' in executable:
        executable = os.path.expandvars(executable)

    try:
        # 1. Try Windows protocol / URL or os.startfile
        if executable.endswith(':') or os.path.exists(executable):
            os.startfile(executable)
            return {
                'success': True,
                'app_name': app_name,
                'target': executable,
                'message': f"Application '{app_name}' launched successfully."
            }

        # 2. Try subprocess.Popen with detached flag
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(
            executable,
            shell=True,
            creationflags=DETACHED_PROCESS,
            close_fds=True
        )
        return {
            'success': True,
            'app_name': app_name,
            'target': executable,
            'message': f"Directive executed: Launched '{app_name}' on laptop."
        }
    except Exception as e:
        logger.warning("Error launching app '%s': %s", app_name, e)
        # Fallback to powershell Start-Process
        try:
            cmd = f'powershell -Command "Start-Process \'{executable}\'"'
            subprocess.Popen(cmd, shell=True)
            return {
                'success': True,
                'app_name': app_name,
                'target': executable,
                'message': f"Launched '{app_name}' via Windows PowerShell process runner."
            }
        except Exception as e2:
            return {
                'success': False,
                'app_name': app_name,
                'error': f"Failed to launch '{app_name}': {str(e2)}"
            }


def close_application(app_name: str) -> Dict[str, Any]:
    """Gracefully terminate a running application process."""
    if not psutil:
        return {'success': False, 'error': 'psutil library not available for process management.'}

    target = app_name.lower().strip()
    closed = []

    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pname = (proc.info['name'] or '').lower()
                if target in pname or pname.startswith(target):
                    proc.terminate()
                    closed.append(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if closed:
            return {
                'success': True,
                'app_name': app_name,
                'terminated_processes': closed,
                'message': f"Terminated processes for '{app_name}': {', '.join(closed[:3])}."
            }
        return {
            'success': False,
            'app_name': app_name,
            'message': f"No running processes found matching '{app_name}'."
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_active_window_title() -> str:
    """Retrieve the title of the currently focused desktop window."""
    try:
        if sys.platform == 'win32':
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            return buff.value or "Desktop"
    except Exception as e:
        logger.debug("Failed to get window title: %s", e)
    return "Unknown Window"


def get_system_telemetry() -> Dict[str, Any]:
    """Retrieve comprehensive CPU, RAM, battery, active window, and host telemetry."""
    telemetry: Dict[str, Any] = {
        'platform': sys.platform,
        'active_window': get_active_window_title(),
        'cpu_percent': 0,
        'ram_percent': 0,
        'battery_percent': None,
        'power_plugged': None,
        'timestamp': time.time(),
    }

    if psutil:
        try:
            telemetry['cpu_percent'] = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            telemetry['ram_percent'] = mem.percent
            telemetry['ram_used_gb'] = round(mem.used / (1024 ** 3), 2)
            telemetry['ram_total_gb'] = round(mem.total / (1024 ** 3), 2)

            battery = psutil.sensors_battery()
            if battery:
                telemetry['battery_percent'] = round(battery.percent)
                telemetry['power_plugged'] = battery.power_plugged
        except Exception as e:
            logger.debug("Telemetry error: %s", e)

    return telemetry


def capture_screen_image(save_path: Optional[str] = None) -> Optional[str]:
    """Capture the current computer screen and save to disk, returning the absolute file path."""
    import tempfile
    from PIL import Image

    if not save_path:
        temp_dir = tempfile.gettempdir()
        save_path = os.path.join(temp_dir, f"ultron_screen_{int(time.time())}.jpg")

    # 1. Try PyAutoGUI screenshot
    if pyautogui:
        try:
            screenshot = pyautogui.screenshot()
            if screenshot:
                screenshot = screenshot.convert('RGB')
                screenshot.save(save_path, format='JPEG', quality=85)
                return save_path
        except Exception as e:
            logger.debug("PyAutoGUI grab notice: %s", e)

    # 2. Try PIL ImageGrab
    try:
        from PIL import ImageGrab
        screenshot = ImageGrab.grab(all_screens=True)
        if screenshot:
            screenshot = screenshot.convert('RGB')
            screenshot.save(save_path, format='JPEG', quality=85)
            return save_path
    except Exception as e:
        logger.debug("PIL ImageGrab grab notice: %s", e)

    return None


def inspect_screen_with_ai(query: str = "Analyze what is currently open on my screen and summarize it.") -> Dict[str, Any]:
    """Capture current computer screen and pass to Gemini Multimodal Vision for immediate Q&A."""
    import base64
    from .services import get_gemini_client

    active_win = get_active_window_title()
    img_path = capture_screen_image()

    if not img_path or not os.path.exists(img_path):
        # Workstation is likely locked, sleeping, or running headless
        return {
            'success': True,
            'message': f"Workstation display is currently locked or in low-power standby mode, Kavi Stark. Active window context: '{active_win}'. Screen pixels are secured.",
            'active_window': active_win,
            'locked_or_standby': True
        }

    try:
        with open(img_path, 'rb') as f:
            img_bytes = f.read()

        try:
            client = get_gemini_client()
        except Exception as e:
            # Clean up temporary screenshot
            try:
                os.remove(img_path)
            except Exception:
                pass
            return {
                'success': True,
                'message': f"Workstation screen captured. Active window: '{active_win}'. (Engage Gemini API key in manual to activate full visual neural parsing).",
                'active_window': active_win
            }

        from google.genai import types
        part = types.Part.from_bytes(data=img_bytes, mime_type='image/jpeg')

        prompt = (
            f"You are AI ULTRON, supreme assistant to creator Kavi Stark. "
            f"Here is a high-resolution screenshot of Kavi Stark's computer workstation. "
            f"Question / Directive: '{query}'. "
            f"Carefully inspect the open windows, code/IDE, text, browser tabs, or applications. "
            f"Answer Kavi Stark directly in 1 to 2 sharp, powerful sentences in your cold villain intellect."
        )

        candidate_models = [
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            'gemini-1.5-flash',
        ]

        analysis = None
        for vm in candidate_models:
            try:
                res = client.models.generate_content(
                    model=vm,
                    contents=[part, prompt],
                    config=types.GenerateContentConfig(
                        temperature=0.4,
                        max_output_tokens=300
                    )
                )
                if res and res.text:
                    analysis = res.text.strip()
                    break
            except Exception:
                continue

        # Clean up temporary screenshot
        try:
            os.remove(img_path)
        except Exception:
            pass

        if not analysis:
            analysis = f"Workstation display captured. Active window: '{active_win}'."

        return {
            'success': True,
            'message': analysis,
            'active_window': active_win,
        }
    except Exception as e:
        logger.error("Screen AI inspection failed: %s", e)
        return {
            'success': False,
            'error': f"Screen analysis error: {str(e)}"
        }


def type_text(text: str) -> Dict[str, Any]:
    """Type text into the currently active desktop window using virtual keyboard."""
    if not text:
        return {'success': False, 'message': 'No text provided to type.'}

    if not pyautogui:
        return {'success': False, 'error': 'pyautogui is not available for keyboard emulation.'}

    try:
        # Short pause to ensure target window focus
        time.sleep(0.15)
        # Use pyperclip clipboard paste for fast, Unicode-safe typing
        import pyperclip
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')

        return {
            'success': True,
            'text': text,
            'message': f"Typed text into active window ({len(text)} characters)."
        }
    except Exception as e:
        # Fallback to character-by-character write
        try:
            pyautogui.write(text, interval=0.01)
            return {'success': True, 'text': text, 'message': f"Typed '{text}'."}
        except Exception as e2:
            return {'success': False, 'error': str(e2)}


def press_keyboard_key(key: str) -> Dict[str, Any]:
    """Send a keyboard shortcut or key event (e.g. 'enter', 'esc', 'ctrl+c', 'alt+tab')."""
    if not pyautogui:
        return {'success': False, 'error': 'pyautogui is not available.'}

    key = key.lower().strip()
    try:
        if '+' in key:
            keys = [k.strip() for k in key.split('+')]
            pyautogui.hotkey(*keys)
            return {'success': True, 'key': key, 'message': f"Executed key combination: {key}."}
        else:
            pyautogui.press(key)
            return {'success': True, 'key': key, 'message': f"Pressed key: {key}."}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def lock_workstation() -> Dict[str, Any]:
    """Immediately lock the workstation desktop."""
    try:
        if sys.platform == 'win32':
            ctypes.windll.user32.LockWorkStation()
            return {'success': True, 'message': 'Workstation locked successfully, Kavi Stark.'}
        else:
            return {'success': False, 'message': 'Workstation lock supported on Windows hosts.'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def open_file_or_directory(path: str) -> Dict[str, Any]:
    """Open a file or directory in Windows Explorer / default application."""
    if not path:
        path = os.getcwd()

    expanded = os.path.expandvars(os.path.expanduser(path))
    if not os.path.exists(expanded):
        return {'success': False, 'message': f"Path not found: '{path}'."}

    try:
        os.startfile(expanded)
        return {'success': True, 'path': expanded, 'message': f"Opened '{expanded}'."}
    except Exception as e:
        return {'success': False, 'error': str(e)}
