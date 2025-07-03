import tkinter as tk
from tkinter import messagebox
import subprocess

def open_register():
    try:
        import sys
        subprocess.Popen([sys.executable, "user_info.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Register page:\n{e}")


def open_login():
    try:
        import subprocess
        subprocess.Popen(["python", "login.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Login page:\n{e}")


def main():
    # --- Main Window ---
    root = tk.Tk()
    root.title("QuizMania")
    root.attributes('-fullscreen', True)  # Fullscreen mode
    root.configure(bg="#eaf6ff")  # Light pastel background

    # --- Fonts and Colors ---
    TITLE_FONT = ("Helvetica", 36, "bold")
    BUTTON_FONT = ("Helvetica", 18, "bold")
    BUTTON_COLOR = "#556B2F"      # Olive green
    BUTTON_HOVER = "#3e5220"      # Darker olive
    TEXT_COLOR = "#2c3e50"

    # --- Hover Effects ---
    def on_enter(e):
        e.widget["background"] = BUTTON_HOVER

    def on_leave(e):
        e.widget["background"] = BUTTON_COLOR

    def create_button(text, command):
        btn = tk.Button(
            frame,  # Put inside central frame
            text=text,
            command=command,
            font=BUTTON_FONT,
            width=20,
            height=2,
            bg=BUTTON_COLOR,
            fg="white",
            bd=0,
            relief="ridge",
            activeforeground="white",
            cursor="hand2"
        )
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    # --- Frame for Centered Layout ---
    frame = tk.Frame(root, bg="#eaf6ff")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # --- Title at the Top ---
    tk.Label(
        frame,
        text="🎯 Welcome to QuizMania!",
        font=TITLE_FONT,
        fg=TEXT_COLOR,
        bg="#eaf6ff"
    ).pack(pady=30)

    # --- Buttons Below Title ---
    create_button("📝 Register", open_register).pack(pady=15)
    create_button("🔐 Login", open_login).pack(pady=15)

    # --- Footer at Bottom ---
    tk.Label(
        root,
        text="Press ESC to Exit",
        font=("Helvetica", 12),
        fg="#7f8c8d",
        bg="#eaf6ff"
    ).pack(side="bottom", pady=20)

    # --- ESC Key to Close ---
    def exit_fullscreen(event):
        root.destroy()

    root.bind("<Escape>", exit_fullscreen)

    root.mainloop()

# ✅ Only run main window if this file is run directly
if __name__ == "__main__":
    main()



