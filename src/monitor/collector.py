import json
import platform
import subprocess

from monitor.models import USBDevice

POWERSHELL_SCRIPT = r"""
$devices = Get-CimInstance Win32_PnPEntity |
    Where-Object { $_.PNPDeviceID -like 'USB*' } |
    Select-Object Name, Manufacturer, PNPDeviceID, Service

$devices | ConvertTo-Json -Depth 3 -Compress
"""

def _extract_id_fields(pnp_id: str) -> tuple[str, str, str]:
    upper = (pnp_id or "").upper()

    vid = ""
    pid = ""
    serial = ""

    for part in upper.split("\\"):
        if part.startswith("VID_"):
            vid = part[4:8]
        elif part.startswith("PID_"):
            pid = part[4:8]

    parts = (pnp_id or "").split("\\")
    if len(parts) >= 3:
        serial = parts[-1]

    return vid, pid, serial

def collect_usb_devices() -> list[USBDevice]:
    """Collect USB PnP metadata using Windows PowerShell/CIM."""
    if platform.system().lower() != "windows":
        raise RuntimeError("Live USB collection is currently supported on Windows only.")

    completed = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy", "Bypass",
            "-Command", POWERSHELL_SCRIPT,
        ],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )

    if completed.returncode != 0:
        raise RuntimeError(
            completed.stderr.strip() or "PowerShell device query failed."
        )

    raw = completed.stdout.strip()
    if not raw:
        return []

    parsed = json.loads(raw)
    if isinstance(parsed, dict):
        parsed = [parsed]

    devices = []

    for item in parsed:
        pnp_id = str(item.get("PNPDeviceID") or "")
        name = str(item.get("Name") or "Unknown USB Device")
        vendor = str(item.get("Manufacturer") or "Unknown")

        vid, pid, serial = _extract_id_fields(pnp_id)

        devices.append(
            USBDevice(
                device_id=pnp_id,
                name=name,
                vendor=vendor,
                vid=vid,
                pid=pid,
                serial=serial,
                removable=False,
            )
        )

    return sorted(devices, key=lambda device: device.fingerprint)
