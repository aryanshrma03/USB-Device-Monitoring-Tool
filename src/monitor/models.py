from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class USBDevice:
    device_id: str
    name: str
    vendor: str
    vid: str
    pid: str
    serial: str
    removable: bool

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def fingerprint(self) -> str:
        # Prefer a stable device identifier; fall back to VID/PID/serial.
        return self.device_id or f"{self.vid}:{self.pid}:{self.serial}"
