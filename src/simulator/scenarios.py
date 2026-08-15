from monitor.models import USBDevice

def demo_baseline() -> list[USBDevice]:
    return [
        USBDevice(
            device_id="USB\\VID_046D&PID_C52B\\DEMO-MOUSE",
            name="USB Optical Mouse",
            vendor="Demo Vendor",
            vid="046D",
            pid="C52B",
            serial="DEMO-MOUSE",
            removable=False,
        ),
        USBDevice(
            device_id="USB\\VID_046D&PID_C31C\\DEMO-KBD",
            name="USB Keyboard",
            vendor="Demo Vendor",
            vid="046D",
            pid="C31C",
            serial="DEMO-KBD",
            removable=False,
        ),
    ]

def demo_current() -> list[USBDevice]:
    return [
        demo_baseline()[0],
        USBDevice(
            device_id="USB\\VID_0781&PID_558A\\DEMO-STORAGE",
            name="USB Mass Storage Device",
            vendor="Demo Storage",
            vid="0781",
            pid="558A",
            serial="DEMO-STORAGE",
            removable=True,
        ),
    ]
