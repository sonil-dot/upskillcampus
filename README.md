# upskillcampus
Project for Upskill Campus Internship – Quiz Game Project
This is a Python-based quiz game application developed as part of the internship at UpskillCampus.

Features Included are:
-Homepage.py
-User_info.py and login.py form
-Subject_select.py(choose any subject to attempt the quiz)
-load_questions (from the DB)
-quiz_gui.py (20 questions for each subject with options)
-leaderboard.py (leaderboard logic)
-Retry Quiz/choose another subject/Check answers/Logout/exit button 

How to run the Project
Make sure you have the following installed:-
Python 3.10+
Microsoft SQL Server(SSMS)
-Python libraries 
pip install pyodbc
pip install tk

Open SSMS. Run the SQL script from quizgamedb.sql to create the database and tables. (You can create it using the SQL file given below)
-(https://github.com/sonil-dot/upskillcampus/blob/main/quizgamedb.sql)

Clone the repo-
git clone https://github.com/sonil-dot/upskillcampus.git
cd upskillcampus

-Run the project 
python homepage.py
