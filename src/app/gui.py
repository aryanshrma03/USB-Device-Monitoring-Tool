import json
import platform
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from components.controls import create_controls
from components.event_log import EventLog
from components.header import create_header
from components.risk_meter import RiskMeter
from config.theme import load_theme
from monitor.collector import collect_usb_devices
from monitor.comparer import compare_devices
from monitor.models import USBDevice
from monitor.scoring import report_score
from simulator.scenarios import demo_baseline, demo_current

load_theme()

class USBMonitorApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("USB Device Monitoring Tool")
        self.root.geometry("1100x820")
        self.root.minsize(900, 700)

        self.baseline = []
        self.current = []

        create_header(self.root)

        self.status = ctk.CTkLabel(
            self.root,
            text="Status: Ready",
            anchor="w",
            height=42,
            corner_radius=10,
            fg_color="#20242b",
            text_color="#b8c0cc",
        )
        self.status.pack(fill="x", padx=30, pady=(4, 4))

        create_controls(
            self.root,
            self.refresh_devices,
            self.create_baseline,
            self.check_changes,
            self.safe_demo,
            self.reset,
        )

        self.risk = RiskMeter(self.root)

        self.stats = ctk.CTkLabel(
            self.root,
            text="Devices: 0 | Added: 0 | Removed: 0",
            text_color="#9aa4b2",
            font=("Segoe UI", 11),
        )
        self.stats.pack(anchor="w", padx=30, pady=(2, 5))

        self.log = EventLog(self.root)

        ctk.CTkButton(
            self.root,
            text="Export JSON Report",
            command=self.export_report,
            width=150,
            height=38,
        ).pack(anchor="w", padx=30, pady=(0, 6))

        ctk.CTkLabel(
            self.root,
            text="⚠ New USB hardware is not automatically malicious. Investigate unexpected devices before taking action.",
            text_color="#9aa4b2",
            font=("Segoe UI", 11),
        ).pack(anchor="w", padx=30, pady=(0, 18))

        self.reset()

    def refresh_devices(self):
        try:
            self.current = collect_usb_devices()
        except Exception as exc:
            messagebox.showerror("USB Collection Error", str(exc))
            return

        self._display_inventory(self.current)
        self.status.configure(
            text=f"Status: Inventory refreshed • {len(self.current)} USB device(s)"
        )

    def create_baseline(self):
        try:
            devices = collect_usb_devices()
        except Exception as exc:
            messagebox.showerror("USB Collection Error", str(exc))
            return

        self.baseline = devices
        self.current = devices
        self._display_inventory(devices)

        self.log.add(
            f"[BASELINE] Trusted baseline created with {len(devices)} device(s)."
        )
        self.status.configure(text="Status: Baseline created")

    def check_changes(self):
        if not self.baseline:
            messagebox.showwarning(
                "Baseline Required",
                "Create a baseline before checking for USB changes.",
            )
            return

        try:
            current = collect_usb_devices()
        except Exception as exc:
            messagebox.showerror("USB Collection Error", str(exc))
            return

        self.current = current
        report = compare_devices(self.baseline, current)
        self._display_inventory(current)
        self._display_changes(report.added, report.removed)

    def safe_demo(self):
        self.baseline = demo_baseline()
        self.current = demo_current()

        report = compare_devices(self.baseline, self.current)
        self._display_inventory(self.current)
        self._display_changes(report.added, report.removed)

        self.log.add("[DEMO] Synthetic devices only.")
        self.log.add("[DEMO] No USB hardware or Windows configuration was changed.")
        self.status.configure(text="Status: Safe demonstration")

    def _display_inventory(self, devices):
        self.log.clear()
        self.log.add(f"[INVENTORY] {len(devices)} USB device(s) detected.")
        self.log.add("")

        for device in devices:
            removable = "removable" if device.removable else "standard"
            self.log.add(
                f"[DEVICE] {device.name} | "
                f"Vendor: {device.vendor} | "
                f"VID: {device.vid or '-'} | "
                f"PID: {device.pid or '-'} | "
                f"Serial: {device.serial or '-'} | {removable}"
            )

        self.stats.configure(
            text=f"Devices: {len(devices)} | Added: 0 | Removed: 0"
        )

        self.risk.update(0, "NORMAL")

    def _display_changes(self, added, removed):
        score, severity = report_score(added, removed)
        self.risk.update(score, severity)

        self.stats.configure(
            text=(
                f"Devices: {len(self.current)} | "
                f"Added: {len(added)} | Removed: {len(removed)}"
            )
        )

        self.log.add("")
        self.log.add(f"[ANALYSIS] Risk: {score}/100 ({severity})")

        for device in added:
            self.log.add(
                f"[ADDED] {device.name} | "
                f"VID={device.vid or '-'} PID={device.pid or '-'} | "
                f"Vendor={device.vendor}"
            )

        for device in removed:
            self.log.add(
                f"[REMOVED] {device.name} | "
                f"VID={device.vid or '-'} PID={device.pid or '-'} | "
                f"Vendor={device.vendor}"
            )

        if not added and not removed:
            self.log.add("[OK] No USB inventory changes detected.")
            self.status.configure(text="Status: No changes detected")
        else:
            self.status.configure(
                text=f"Status: Changes detected • {len(added)} added • {len(removed)} removed"
            )

    def export_report(self):
        if not self.current:
            messagebox.showwarning("No Data", "Refresh or simulate the USB inventory first.")
            return

        path = filedialog.asksaveasfilename(
            title="Export USB Monitoring Report",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialfile="usb-monitor-report.json",
        )

        if not path:
            return

        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "platform": platform.system(),
            "devices": [asdict(device) for device in self.current],
        }

        try:
            Path(path).write_text(
                json.dumps(payload, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            messagebox.showerror("Export Error", str(exc))
            return

        self.log.add(f"[REPORT] Exported: {path}")

    def reset(self):
        self.baseline = []
        self.current = []
        self.status.configure(text="Status: Ready")
        self.stats.configure(text="Devices: 0 | Added: 0 | Removed: 0")
        self.risk.update(0, "NORMAL")
        self.log.clear()
        self.log.add("[INFO] USB Device Monitoring Tool ready.")

    def run(self):
        self.root.mainloop()
