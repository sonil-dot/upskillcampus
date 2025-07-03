import tkinter as tk
from tkinter import messagebox
import pyodbc
import subject_select

# DB Connection
def connect_db():
    return pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"  # Change if needed
        "Database=QuizGameDB;"
        "Trusted_Connection=yes;"
    )

def verify_login():
    name = entry_name.get().strip()
    email = entry_email.get().strip()

    if not name or not email:
        messagebox.showerror("Input Error", "Please enter both First Name and Email.")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT UserID FROM Users WHERE UserName = ? AND Email = ?", (name, email))
        row = cursor.fetchone()
        conn.close()

        if row:
            user_id = row[0]
            messagebox.showinfo("Login Successful", f"Welcome back, {name}!")
            root.destroy()
            subject_select.start_subject_selection(user_id, name)  # ✅ Passing name here
        else:
            messagebox.showerror("Login Failed", "No matching user found. Please register first.")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# GUI
root = tk.Tk()
root.title("Login - QuizMania")
root.state('zoomed')
root.configure(bg="#eaf6ff")  # Light pastel background

tk.Label(root, text="🔐 Login to QuizMania", font=("Helvetica", 16, "bold"), bg="#eaf6ff", fg="#2c3e50").pack(pady=20)

tk.Label(root, text="First Name", bg="#eaf6ff").pack()
entry_name = tk.Entry(root, width=30)
entry_name.pack(pady=5)

tk.Label(root, text="Email", bg="#eaf6ff").pack()
entry_email = tk.Entry(root, width=30)
entry_email.pack(pady=5)

tk.Button(root, text="Login", command=verify_login, bg="#556B2F", fg="white", font=("Arial", 11), width=15).pack(pady=20)

tk.Label(root, text="Don't have an account? Please Register", font=("Arial", 9), bg="#eaf6ff", fg="#7f8c8d").pack(pady=5)

root.mainloop()

