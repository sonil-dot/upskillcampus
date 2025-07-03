import pyodbc
import tkinter as tk
from tkinter import messagebox
import subject_select
import leaderboard

# Connect to DB
def connect_db():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=SNEHA-PC6;"
        "DATABASE=QuizGameDB;"
        "Trusted_Connection=yes;"
    )

# Load questions for a specific subject
def get_questions_by_subject(subject):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TOP 30 QuestionID, QuestionText, OptionA, OptionB, OptionC, OptionD, CorrectOption 
        FROM Questions
        WHERE Category = ?
    """, (subject,))
    questions = cursor.fetchall()
    conn.close()
    return questions

# Quiz GUI class
class QuizApp:
    def __init__(self, root, user_id, subject, user_name):
        self.root = root
        self.user_id = user_id
        self.user_name = user_name
        self.subject = subject
        self.root.title(f"Test your knowledge, {user_name}!")
        self.root.configure(bg="#DDE5B6")

        self.questions = get_questions_by_subject(subject)
        self.current_q = 0
        self.score = 0
        self.user_answers = []

        self.selected_option = tk.StringVar()

        # UI Layout
        self.question_label = tk.Label(root, text="", wraplength=1000, font=('Arial', 18, 'bold'), bg="#DDE5B6")
        self.question_label.pack(pady=40)

        self.options = []
        for val in ["A", "B", "C", "D"]:
            rb = tk.Radiobutton(root, text="", variable=self.selected_option, value=val,
                                font=("Arial", 15), bg="#DDE5B6", anchor="w", padx=20)
            rb.pack(fill='x', padx=60, pady=8)
            self.options.append(rb)

        self.next_btn = tk.Button(root, text="Next", command=self.next_question,
                                  font=("Arial", 13), bg="#A4C28D", width=14)
        self.next_btn.pack(pady=30)

        self.display_question()

    def display_question(self):
        q = self.questions[self.current_q]
        self.selected_option.set("")  # Clear selection
        self.question_label.config(text=f"Q{self.current_q + 1}. {q.QuestionText}")
        self.options[0].config(text="A. " + q.OptionA)
        self.options[1].config(text="B. " + q.OptionB)
        self.options[2].config(text="C. " + q.OptionC)
        self.options[3].config(text="D. " + q.OptionD)

    def next_question(self):
        selected = self.selected_option.get()

        if not selected:
            messagebox.showerror("No Answer Selected", "⚠️ You must select an answer before going to the next question!")
            return

        question = self.questions[self.current_q]
        correct = question.CorrectOption
        self.user_answers.append((question, selected, correct))

        if selected == correct:
            self.score += 1

        self.current_q += 1
        if self.current_q < len(self.questions):
            self.display_question()
        else:
            self.show_result_page()

    def show_result_page(self):
        self.save_score_to_db()

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Quiz Results")

        if self.score == 20:
            emoji, message = "😊", "Excellent!"
        elif self.score >= 11:
            emoji, message = "🙂", "Good job!"
        else:
            emoji, message = "😐", "Keep trying!"

        tk.Label(self.root, text=f"Your Quiz Results, {self.user_name}", font=("Arial", 22, "bold"), bg="#DDE5B6").pack(pady=20)
        tk.Label(self.root, text=f"{emoji} {message}", font=("Arial", 20), bg="#DDE5B6").pack(pady=10)
        tk.Label(self.root, text=f"You scored {self.score} out of {len(self.questions)}",
                 font=("Arial", 18), bg="#DDE5B6").pack(pady=10)

        # Action buttons
        tk.Button(self.root, text="Retry Quiz", command=self.retry_quiz, font=("Arial", 13), bg="#A4C28D", width=16).pack(pady=10)
        tk.Button(self.root, text="Choose Another Subject", command=self.choose_subject, font=("Arial", 13), bg="#A4C28D", width=20).pack(pady=5)
        tk.Button(self.root, text="View Leaderboard", command=lambda: leaderboard.show_leaderboard(self.subject),
                  font=("Arial", 13), bg="#A4C28D", width=20).pack(pady=5)
        tk.Button(self.root, text="Show Answers", command=self.show_answers_page,
                  font=("Arial", 13), bg="#A4C28D", width=20).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.logout,
                  font=("Arial", 13), bg="#F1B24A", width=16).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.destroy,
          font=("Arial", 13), bg="#E57373", width=16).pack(pady=5)


    def show_answers_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Answer Review")

        canvas = tk.Canvas(self.root, bg="#F1F3E8")
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#F1F3E8")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for idx, (q, selected, correct) in enumerate(self.user_answers):
            option_map = {"A": q.OptionA, "B": q.OptionB, "C": q.OptionC, "D": q.OptionD}
            selected_text = option_map.get(selected, "Not answered")
            correct_text = option_map.get(correct, "Unavailable")
            is_correct = selected == correct
            result_text = "✅ Correct" if is_correct else f"❌ Wrong (Correct: {correct}. {correct_text})"
            color = "green" if is_correct else "red"

            tk.Label(scroll_frame, text=f"Q{idx + 1}. {q.QuestionText}", wraplength=900, justify="left",
                     bg="#F1F3E8", font=("Arial", 13, "bold")).pack(anchor="w", pady=2)
            tk.Label(scroll_frame, text=f"Your answer: {selected}. {selected_text}", fg=color,
                     bg="#F1F3E8", font=("Arial", 12)).pack(anchor="w")
            tk.Label(scroll_frame, text=result_text, fg=color,
                     bg="#F1F3E8", font=("Arial", 11, "italic")).pack(anchor="w", pady=(0, 10))

        tk.Button(scroll_frame, text="Back to Results", command=self.show_result_page,
                  font=("Arial", 13), bg="#A4C28D", width=18).pack(pady=10)

    def retry_quiz(self):
        self.current_q = 0
        self.score = 0
        self.user_answers = []
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root, self.user_id, self.subject, self.user_name)

    def choose_subject(self):
        self.root.destroy()
        subject_select.start_subject_selection(self.user_id, self.user_name)

    def logout(self):
        self.root.destroy()
        try:
            import homepage
            homepage.show_homepage()
        except Exception as e:
            print("Could not return to homepage:", e)

    def save_score_to_db(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Scores (UserID, Subject, Score, TotalQuestions)
                VALUES (?, ?, ?, ?)
            """, (self.user_id, self.subject, self.score, len(self.questions)))
            conn.commit()
            conn.close()
        except Exception as e:
            print("Failed to save score:", e)

# Entry point
def start_quiz_gui(user_id, subject, user_name):
    root = tk.Tk()
    root.state('zoomed')  # Open in maximized mode
    app = QuizApp(root, user_id, subject, user_name)
    root.mainloop()
