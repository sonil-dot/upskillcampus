-- Create the database
CREATE DATABASE QuizGameDB;
GO

-- Use the database
USE QuizGameDB;
GO

-- Create Users table
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    UserName NVARCHAR(100) NOT NULL,
    Age INT,
    Gender NVARCHAR(10),
    Email NVARCHAR(100),
    CreatedAt DATETIME DEFAULT GETDATE()
);
GO

-- Create Questions table
CREATE TABLE Questions (
    QuestionID INT IDENTITY(1,1) PRIMARY KEY,
    QuestionText NVARCHAR(MAX) NOT NULL,
    OptionA NVARCHAR(255),
    OptionB NVARCHAR(255),
    OptionC NVARCHAR(255),
    OptionD NVARCHAR(255),
    CorrectOption NVARCHAR(1),
    Category NVARCHAR(50)
);
GO

-- Create Scores table
CREATE TABLE Scores (
    ScoreID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    Subject NVARCHAR(50),
    Score INT,
    TotalQuestions INT,
    TakenAt DATETIME DEFAULT GETDATE()
);
GO

