import customtkinter as ctk

def create_controls(parent, refresh_command, baseline_command,
                    monitor_command, demo_command, reset_command):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=30, pady=8)

    ctk.CTkButton(
        frame, text="Refresh Devices", command=refresh_command,
        width=135, height=42, corner_radius=10
    ).pack(side="left")

    ctk.CTkButton(
        frame, text="Create Baseline", command=baseline_command,
        width=135, height=42, corner_radius=10
    ).pack(side="left", padx=8)

    ctk.CTkButton(
        frame, text="Check Changes", command=monitor_command,
        width=130, height=42, corner_radius=10
    ).pack(side="left")

    ctk.CTkButton(
        frame, text="Safe Demo", command=demo_command,
        width=110, height=42, corner_radius=10
    ).pack(side="left", padx=8)

    ctk.CTkButton(
        frame, text="Reset", command=reset_command,
        width=90, height=42, corner_radius=10,
        fg_color="#3b3f46", hover_color="#4b5058"
    ).pack(side="right")
