#!/usr/bin/env python3
"""
=============================================================================
AI ULTRON LAPTOP CLIENT NODE DAEMON
Supreme Creator & Master Authority: Kavi Stark
Role: Persistent local workstation sentinel, RPA actuator, & telemetry reporter
=============================================================================
"""

import os
import sys
import time
import json
import logging
import argparse
import urllib.request
import urllib.error

# Add parent directory to sys.path to allow imports from assistant
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [UltronNode] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("UltronNode")

# Import device controller modules
try:
    from assistant.device_controller import (
        get_system_telemetry,
        open_application,
        close_application,
        lock_workstation,
        type_text,
        press_keyboard_key,
        open_file_or_directory,
        inspect_screen_with_ai
    )
except ImportError as e:
    logger.error("Failed to import device_controller: %s", e)
    sys.exit(1)


class UltronLaptopNode:
    def __init__(self, server_url: str = "http://127.0.0.1:8000"):
        self.server_url = server_url.rstrip("/")
        self.node_id = f"laptop-node-{os.environ.get('COMPUTERNAME', 'pc').lower()}"
        self.is_running = False
        logger.info("Initializing Ultron Laptop Node for Kavi Stark. Target Brain: %s", self.server_url)

    def print_status(self):
        """Display immediate hardware telemetry and node status."""
        telem = get_system_telemetry()
        print("\n" + "=" * 60)
        print("          AI ULTRON // LAPTOP NODE SENTINEL")
        print("      Authorized Master Authority: KAVI STARK")
        print("=" * 60)
        print(f" Node Identifier  : {self.node_id}")
        print(f" Brain Server     : {self.server_url}")
        print(f" Platform         : {telem.get('platform')}")
        print(f" Active Window    : {telem.get('active_window')}")
        print(f" CPU Utilization  : {telem.get('cpu_percent')}%")
        print(f" Memory Usage     : {telem.get('ram_percent')}% ({telem.get('ram_used_gb', 0)} GB / {telem.get('ram_total_gb', 0)} GB)")
        bat = telem.get('battery_percent')
        bat_str = f"{bat}%" if bat is not None else "AC Station (No Battery)"
        charging = " [Charging]" if telem.get('power_plugged') else " [On Battery]"
        print(f" Battery Telemetry: {bat_str}{charging}")
        print("=" * 60 + "\n")

    def sync_heartbeat(self):
        """Send live telemetry heartbeat to the central Ultron brain."""
        telem = get_system_telemetry()
        url = f"{self.server_url}/api/device/status/"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    logger.debug("Heartbeat synchronized with Ultron Central.")
                    return True
        except Exception as e:
            logger.debug("Brain heartbeat notice: %s", e)
        return False

    def check_due_alerts(self):
        """Poll for due tasks or outbound alerts requiring laptop action."""
        url = f"{self.server_url}/api/reminders/due/"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    due = data.get('due_reminders', [])
                    for item in due:
                        title = item.get('title', 'Scheduled Task')
                        phone = item.get('formatted_phone') or item.get('phone_number')
                        logger.warning(
                            "ALERT TRIGGERED FOR KAVI STARK: '%s'. Phone dispatch bound: %s",
                            title, phone
                        )
        except Exception:
            pass

    def run_daemon(self, interval: int = 5):
        """Run persistent background loop monitoring workstation and executing directives."""
        self.is_running = True
        logger.info("Ultron Laptop Sentinel is now ACTIVE in background. Press Ctrl+C to stop.")
        self.print_status()

        try:
            while self.is_running:
                self.sync_heartbeat()
                self.check_due_alerts()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Daemon standby suspended by Kavi Stark.")
            self.is_running = False


def main():
    parser = argparse.ArgumentParser(description="AI ULTRON Laptop Node Sentinel")
    parser.add_argument("--server", default="http://127.0.0.1:8000", help="Ultron Central Server URL")
    parser.add_argument("--status", action="store_true", help="Print immediate system telemetry and exit")
    parser.add_argument("--lock", action="store_true", help="Execute immediate workstation lock")
    parser.add_argument("--open", type=str, help="Launch application by name")
    parser.add_argument("--type", type=str, help="Type text into active window")
    parser.add_argument("--inspect-screen", action="store_true", help="Capture and inspect current screen")
    parser.add_argument("--daemon", action="store_true", help="Run as persistent background sentinel daemon")

    args = parser.parse_args()
    node = UltronLaptopNode(server_url=args.server)

    if args.status:
        node.print_status()
    elif args.lock:
        res = lock_workstation()
        print(res.get("message", "Lock executed."))
    elif args.open:
        res = open_application(args.open)
        print(res.get("message", "Launch executed."))
    elif args.type:
        res = type_text(args.type)
        print(res.get("message", "Typing executed."))
    elif args.inspect_screen:
        res = inspect_screen_with_ai()
        print(res.get("message", "Inspection completed."))
    elif args.daemon:
        node.run_daemon()
    else:
        node.print_status()
        print("Tip: Run with --daemon to start the continuous background sentinel.")


if __name__ == "__main__":
    main()

