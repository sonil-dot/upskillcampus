import tkinter as tk
from tkinter import messagebox
import pyodbc
from datetime import datetime
import subprocess  # For launching login.py

# Database connection
def connect_db():
    return pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"
        "Database=QuizGameDB;"
        "Trusted_Connection=yes;"
    )

def save_user():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    email = entry_email.get()

    if not name or not age or not gender or not email:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Users (UserName, Age, Gender, Email)
            OUTPUT INSERTED.UserID
            VALUES (?, ?, ?, ?)
        """, (name, int(age), gender, email))

        user_id_row = cursor.fetchone()
        if user_id_row:
            user_id = user_id_row[0]
        else:
            messagebox.showerror("Database Error", "Could not retrieve User ID.")
            return

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Welcome {name}! Your User ID is {user_id}\nPlease proceed to login.")
        root.destroy()

        # ✅ Launch login page
        subprocess.Popen(["python", "login.py"])

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Tkinter form
root = tk.Tk()
root.title("Register - User Info")
root.state('zoomed')
root.configure(bg="#F1F3E8")

tk.Label(root, text="Enter your details to start the quiz", font=("Arial", 12, "bold"), bg="#F1F3E8").pack(pady=10)

tk.Label(root, text="Name", bg="#F1F3E8").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Age", bg="#F1F3E8").pack()
entry_age = tk.Entry(root)
entry_age.pack()

tk.Label(root, text="Gender", bg="#F1F3E8").pack()
gender_var = tk.StringVar()
gender_dropdown = tk.OptionMenu(root, gender_var, "Male", "Female", "Other")
gender_dropdown.pack()

tk.Label(root, text="Email", bg="#F1F3E8").pack()
entry_email = tk.Entry(root)
entry_email.pack()

tk.Button(root, text="Register", command=save_user, bg="#A4C28D", width=15).pack(pady=15)

if __name__ == "__main__":
    root.mainloop()
