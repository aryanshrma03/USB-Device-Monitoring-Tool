from monitor.models import USBDevice

def device_risk(device: USBDevice, is_new: bool = True) -> int:
    score = 20 if is_new else 0

    if device.removable:
        score += 25

    if not device.vendor or device.vendor.lower() == "unknown":
        score += 15

    if not device.serial:
        score += 5

    return min(100, score)

def report_score(added: list[USBDevice], removed: list[USBDevice]) -> tuple[int, str]:
    score = sum(device_risk(device, is_new=True) for device in added)

    if removed:
        score += min(10, len(removed) * 2)

    score = min(100, score)

    if score >= 80:
        severity = "CRITICAL"
    elif score >= 60:
        severity = "HIGH"
    elif score >= 40:
        severity = "MEDIUM"
    elif score >= 20:
        severity = "LOW"
    else:
        severity = "NORMAL"

    return score, severity
