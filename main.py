import customtkinter as ctk
import os
import webbrowser
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, simpledialog

ctk.set_appearance_mode("dark")

TITLE_FONT = ("Segoe UI", 28, "bold")
BUTTON_FONT = ("Segoe UI", 14, "bold")

mc_path = ""
managed_versions = []


app = ctk.CTk()
app.title("XIVs Mod Manager")
app.geometry("400x500")
app.resizable(False, False)

def open_folder():
    global mc_path
    folder_path = filedialog.askdirectory(title="Select Minecraft Folder")
    if folder_path:
        mc_path = folder_path
        path_label.configure(text=mc_path)
        reload_versions_from_disk()
        create_version_buttons()

def add_version():
    if not mc_path:
        messagebox.showwarning("No folder", "Select Minecraft folder first!")
        return
    version = simpledialog.askstring("Add Version", "Enter version (e.g. 1.21.11):")
    if not version:
        return
    folder_path = os.path.join(mc_path, f"mods{version}")
    if os.path.exists(folder_path):
        messagebox.showinfo("Exists", "This version already exists.")
        return
    os.makedirs(folder_path)
    reload_versions_from_disk()
    create_version_buttons()

def reload_versions_from_disk():
    global managed_versions
    if not mc_path:
        return
    managed_versions[:] = sorted([
        f.replace("mods", "")
        for f in os.listdir(mc_path)
        if os.path.isdir(os.path.join(mc_path, f))
        and f.startswith("mods")
        and f != "mods"
    ])

def open_falcon_website():
    webbrowser.open("https://thexivproject.netlify.app/")

def create_version_buttons():
    if not mc_path:
        return
    for widget in versions_frame.winfo_children():
        widget.destroy()
    for version in managed_versions:
        btn = ctk.CTkButton(
            versions_frame,
            text=version,
            command=lambda v=version: switch_mods(v)
        )
        btn.configure(fg_color="darkred", hover_color="black")
        btn.pack(pady=5, fill="x")

def switch_mods(version):
    if not mc_path:
        messagebox.showwarning("No folder", "Select Minecraft folder first!")
        return
    mods_path = os.path.join(mc_path, "mods")
    target_path = os.path.join(mc_path, f"mods{version}")
    active_file = os.path.join(mc_path, "active_version.txt")
    if not os.path.exists(target_path):
        messagebox.showerror("Error", f"Folder mods{version} does not exist!")
        return
    if os.path.exists(active_file):
        with open(active_file, "r") as f:
            current_version = f.read().strip()
    else:
        current_version = None
    if current_version == version:
        messagebox.showinfo("Already active", f"Version {version} is already active.")
        return
    if current_version and os.path.exists(mods_path):
        old_mods_path = os.path.join(mc_path, f"mods{current_version}")
        if not os.path.exists(old_mods_path):
            os.rename(mods_path, old_mods_path)
    if os.path.exists(mods_path):
        messagebox.showerror(
            "Error",
            "mods folder already exists but no active_version.txt match.\n"
            "Delete or rename it manually once."
        )
        return
    os.rename(target_path, mods_path)
    with open(active_file, "w") as f:
        f.write(version)
    reload_versions_from_disk()
    create_version_buttons()
    messagebox.showinfo("Success", f"Switched to version {version}")

def auto_scan():
    global mc_path
    default_path = os.path.join(os.getenv("APPDATA"), ".minecraft")
    if os.path.exists(default_path):
        mc_path = default_path
        path_label.configure(text=mc_path)
        reload_versions_from_disk()
        create_version_buttons()
        messagebox.showinfo("Auto Scan", "Minecraft folder found!")
    else:
        messagebox.showerror("Auto Scan", "Could not find .minecraft folder.")

def open_add_version_window():
    if not mc_path:
        messagebox.showwarning("No folder", "Select Minecraft folder first!")
        return
    popup = ctk.CTkToplevel(app)
    popup.title("Add Version")
    popup.geometry("300x150")
    popup.resizable(False, False)

    label = ctk.CTkLabel(popup, text="Enter version (e.g. 1.21.11):", font=("Inter", 12))
    label.pack(pady=(20, 5))

    version_entry = ctk.CTkEntry(popup, placeholder_text="Version")
    version_entry.pack(pady=5, padx=20, fill="x")

    def confirm():
        version = version_entry.get().strip()
        if not version:
            messagebox.showwarning("Empty", "Please enter a version.")
            return
        folder_path = os.path.join(mc_path, f"mods{version}")
        if os.path.exists(folder_path):
            messagebox.showinfo("Exists", "This version already exists.")
            return
        os.makedirs(folder_path)
        reload_versions_from_disk()
        create_version_buttons()
        popup.destroy()

    buttons_frame = ctk.CTkFrame(popup)
    buttons_frame.pack(pady=10)

    confirm_btn = ctk.CTkButton(buttons_frame, text="Add Version", command=confirm)
    confirm_btn.configure(fg_color="darkred", hover_color="black")
    confirm_btn.pack(side="left", padx=5)

    cancel_btn = ctk.CTkButton(buttons_frame, text="Cancel", command=popup.destroy)
    cancel_btn.configure(fg_color="darkred", hover_color="black")
    cancel_btn.pack(side="left", padx=5)



title_label = ctk.CTkLabel(app, text="XIV's MOD MANAGER", font=TITLE_FONT)
title_label.pack(pady=20)

buttons_frame = ctk.CTkFrame(app)
buttons_frame.pack(pady=10)

choose_button = ctk.CTkButton(
    buttons_frame,
    text="Choose Minecraft Folder",
    command=open_folder,
    font=BUTTON_FONT
)
choose_button.configure(fg_color="darkred", hover_color="black")
choose_button.pack(side="left", padx=5)

auto_button = ctk.CTkButton(
    buttons_frame,
    text="Auto Scan",
    command=auto_scan,
    font=BUTTON_FONT
)
auto_button.configure(fg_color="darkred", hover_color="black")
auto_button.pack(side="left", padx=5)

path_label = ctk.CTkLabel(app, text="No folder selected", wraplength=350)
path_label.pack(pady=10)

versions_frame = ctk.CTkScrollableFrame(app, height=200)
versions_frame.pack(pady=10, fill="x", padx=20)

add_button = ctk.CTkButton(app, text="Add Version", font=BUTTON_FONT, command=open_add_version_window)
add_button.configure(fg_color="darkred", hover_color="black")
add_button.pack(pady=5)

footer_label = ctk.CTkLabel(app, text="by F4LCON", font=("Mozer", 10))
footer_label.pack(pady=5)
footer_label.bind("<Button-1>", lambda e: open_falcon_website())
footer_label.bind("<Enter>", lambda e: footer_label.configure(cursor="hand2"))

app.mainloop()
