import pyodbc

# 🔁 Replace only the database name
server = 'SNEHA-PC6'      # or your server name
database = 'QuizGameDB'         # your database name

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
)

try:
    conn = pyodbc.connect(conn_str)
    print("✅ Connected to SQL Server!")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.tables")
    for row in cursor.fetchall():
        print("📄 Table:", row.name)
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)

