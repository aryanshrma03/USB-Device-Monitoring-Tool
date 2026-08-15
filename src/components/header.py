import customtkinter as ctk

def create_header(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=30, pady=(24, 8))

    ctk.CTkLabel(
        frame,
        text="🔌 USB Device Monitoring Tool",
        font=("Segoe UI", 28, "bold"),
    ).pack(anchor="w")

    ctk.CTkLabel(
        frame,
        text="Defensive endpoint monitoring for USB device inventory and changes.",
        text_color="#9aa4b2",
        font=("Segoe UI", 13),
    ).pack(anchor="w", pady=(5, 0))
