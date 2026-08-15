from dataclasses import dataclass

from monitor.models import USBDevice

@dataclass
class USBChangeReport:
    added: list[USBDevice]
    removed: list[USBDevice]

    @property
    def changed(self) -> bool:
        return bool(self.added or self.removed)

def compare_devices(
    baseline: list[USBDevice],
    current: list[USBDevice],
) -> USBChangeReport:
    old = {device.fingerprint: device for device in baseline}
    new = {device.fingerprint: device for device in current}

    added = [new[key] for key in sorted(new.keys() - old.keys())]
    removed = [old[key] for key in sorted(old.keys() - new.keys())]

    return USBChangeReport(added=added, removed=removed)
