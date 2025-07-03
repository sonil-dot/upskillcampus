import pyodbc

# Database connection details
server = 'SNEHA-PC6'
database = 'QuizGameDB'

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Fetch questions
    cursor.execute("SELECT QuestionID, QuestionText, OptionA, OptionB, OptionC, OptionD, CorrectOption, Category FROM Questions")
    
    questions = cursor.fetchall()

    # Display questions
    for q in questions:
        print(f"\nQuestion {q.QuestionID}: {q.QuestionText}")
        print(f"A. {q.OptionA}")
        print(f"B. {q.OptionB}")
        print(f"C. {q.OptionC}")
        print(f"D. {q.OptionD}")
        print(f"Category: {q.Category}")

    conn.close()
except Exception as e:
    print("Error:", e)
