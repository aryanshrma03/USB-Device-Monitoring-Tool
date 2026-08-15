# 🔌 USB Device Monitoring Tool

A defensive Python desktop utility for monitoring USB device connection and removal events on a local Windows system.

## 🎯 Features

- USB device inventory
- Connect/disconnect event monitoring
- Device name, vendor, VID/PID and serial indicators when available
- Windows WMI/PowerShell discovery
- Baseline creation
- New/removed device detection
- Risk scoring for unfamiliar devices
- Event history
- CustomTkinter dashboard
- Safe simulation mode
- JSON report export
- Unit tests
- Modular architecture

## 🛡️ Security Purpose

USB devices can introduce risks such as:

- Unauthorized removable media
- Unknown peripherals
- Rogue USB hardware
- Unapproved storage devices
- Unexpected device changes

This project is designed as a **local defensive monitoring tool**. It does not block devices, install drivers, capture keystrokes, copy files, or inspect USB contents.

## 🧠 Architecture

```text
Windows USB Device Inventory
           │
           ▼
     Device Collector
           │
           ▼
    Normalized Device Data
           │
     ┌─────┴─────┐
     ▼           ▼
 Baseline      Current
     │           │
     └─────┬─────┘
           ▼
      Comparison
           │
     ┌─────┴────────────┐
     ▼                  ▼
   ADDED              REMOVED
     │                  │
     └────────┬─────────┘
              ▼
        Risk Assessment
              │
              ▼
         GUI / JSON
```

## 🖥️ Platform

The full USB inventory collector is designed for **Windows**, using PowerShell/WMI-compatible system information.

The application can still be opened on other operating systems, but live device collection is unavailable there.

## 📦 Installation

```bash
git clone https://github.com/aryanshrma03/USB-Device-Monitoring-Tool.git
cd USB-Device-Monitoring-Tool

python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
```

## ▶️ Run

```bash
python src/main.py
```

## 🔍 Workflow

### 1. Refresh Devices

The application queries Windows for USB-related device information.

### 2. Create Baseline

The current inventory can be saved as a trusted baseline.

### 3. Monitor

Refresh the inventory again to identify:

```text
ADDED
REMOVED
UNCHANGED
```

### 4. Investigate

New devices should be reviewed before being considered trusted.

## 📊 Risk Scoring

The score is an **exposure indicator**, not proof of malicious behavior.

Example weights:

| Indicator | Weight |
|---|---:|
| New device | 20 |
| Removable storage indicator | 25 |
| Unknown vendor/device metadata | 15 |
| Missing serial identifier | 5 |

Score is capped at 100.

```text
0–19     NORMAL
20–39    LOW
40–59    MEDIUM
60–79    HIGH
80–100   CRITICAL
```

A new USB device is not automatically malicious. Legitimate keyboards, mice, phones, storage devices, and adapters can trigger alerts.

## 🧪 Safe Demo

The **Simulation** function creates synthetic USB events in memory.

It does not:

- connect USB hardware
- disconnect USB hardware
- install drivers
- modify registry settings
- alter Windows device configuration

## 📄 JSON Reports

Reports can be exported in a structure similar to:

```json
{
  "generated_at": "2026-08-15T00:00:00Z",
  "platform": "Windows",
  "devices": [],
  "events": []
}
```

## 📂 Project Structure

```text
USB-Device-Monitoring-Tool/
│
├── src/
│   ├── main.py
│   ├── app/
│   │   ├── __init__.py
│   │   └── gui.py
│   ├── monitor/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── collector.py
│   │   ├── comparer.py
│   │   └── scoring.py
│   ├── simulator/
│   │   ├── __init__.py
│   │   └── scenarios.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── header.py
│   │   ├── controls.py
│   │   ├── risk_meter.py
│   │   └── event_log.py
│   └── config/
│       ├── __init__.py
│       └── theme.py
│
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔮 Future Improvements

- [ ] Real-time Windows device notifications
- [ ] Windows service mode
- [ ] Device allowlist/blocklist
- [ ] Digital-signature inspection
- [ ] Device classification
- [ ] Windows Event Log integration
- [ ] SIEM forwarding
- [ ] Email/webhook alerts
- [ ] Persistent SQLite history
- [ ] YARA-based file inspection for approved removable media
- [ ] Administrator policy integration

## 👨‍💻 Author

**Aryan Sharma**

Cybersecurity-focused Python project demonstrating defensive USB device inventory, change detection, and local endpoint monitoring.
