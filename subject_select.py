import tkinter as tk
from tkinter import messagebox
import quiz_gui  # Make sure this is in the same folder

def start_subject_selection(user_id, user_name):
    def start_quiz():
        selected_subject = subject_var.get()
        if not selected_subject:
            messagebox.showwarning("Selection Required", "Please choose a subject.")
            return
        window.destroy()
        quiz_gui.start_quiz_gui(user_id, selected_subject, user_name)

    window = tk.Tk()
    window.title("Select Subject")
    window.state('zoomed')
    window.configure(bg="#DDE5B6")  # Olive green background to match quiz screen

    # Personalized greeting
    tk.Label(window, text=f"Test your knowledge, {user_name}!", font=("Arial", 14, "bold"),
             bg="#DDE5B6", fg="#333").pack(pady=10)

    tk.Label(window, text="Choose a subject to begin:", font=("Arial", 12),
             bg="#DDE5B6").pack(pady=5)

    subject_var = tk.StringVar()
    subjects = ["Math", "Geography", "Science", "History", "General Knowledge", "Computer"]
    subject_var.set(subjects[0])  # Default

    for sub in subjects:
        tk.Radiobutton(window, text=sub, variable=subject_var, value=sub,
                       font=("Arial", 11), bg="#DDE5B6", anchor="w").pack(anchor="w", padx=30)

    tk.Button(window, text="Start Quiz", command=start_quiz, bg="#A4C28D", fg="black",
              font=("Arial", 11), width=15).pack(pady=20)

    window.mainloop()

# Testing example
if __name__ == "__main__":
    start_subject_selection(user_id=1, user_name="Sneha")


