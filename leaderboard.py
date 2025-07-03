import pyodbc
import tkinter as tk
from tkinter import ttk

# Connect to database
def connect_db():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=SNEHA-PC6;"
        "DATABASE=QuizGameDB;"
        "Trusted_Connection=yes;"
    )
    return conn

# Fetch top scores for a given subject
def get_top_scores(subject):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TOP 10 U.UserName, S.Score, S.TotalQuestions, S.TakenAt
        FROM Scores S
        JOIN Users U ON S.UserID = U.UserID
        WHERE S.Subject = ?
        ORDER BY S.Score DESC, S.TakenAt ASC
    """, (subject,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Show leaderboard GUI
def show_leaderboard(subject):
    window = tk.Tk()
    window.title(f"{subject} Leaderboard - QuizMania")
    window.geometry("600x400")
    window.configure(bg="#F1F3E8")

    tk.Label(window, text=f"🏆 {subject} Leaderboard", font=("Arial", 18, "bold"), bg="#F1F3E8").pack(pady=10)

    # Table
    columns = ("UserName", "Score", "Out of", "Date")
    tree = ttk.Treeview(window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    top_scores = get_top_scores(subject)
    for row in top_scores:
        tree.insert("", tk.END, values=(row.UserName, row.Score, row.TotalQuestions, row.TakenAt.strftime("%Y-%m-%d %H:%M")))

    tree.pack(pady=20, padx=20, fill="both", expand=True)

    tk.Button(window, text="Close", command=window.destroy, font=("Arial", 12), bg="#A4C28D", width=10).pack(pady=10)

    window.mainloop()

# For testing directly
if __name__ == "__main__":
    show_leaderboard("Math")  # Try any subject here
