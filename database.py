import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

con = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = con.cursor()

# Create database
cur.execute("CREATE DATABASE IF NOT EXISTS placement_management")

# Use the database
cur.execute("USE placement_management")

# ---------------- STUDENTS TABLE ----------------

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    branch VARCHAR(100),
    cgpa FLOAT,
    graduation_year INT
)
""")

# ---------------- COMPANIES TABLE ----------------

cur.execute("""
CREATE TABLE IF NOT EXISTS companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    job_role VARCHAR(100),
    package FLOAT
)
""")

# ---------------- DRIVES TABLE ----------------

cur.execute("""
CREATE TABLE IF NOT EXISTS drives (
    drive_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    eligibility_cgpa FLOAT,
    eligibility_branch VARCHAR(100),
    drive_date DATE,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
)
""")

# ---------------- APPLICATIONS TABLE ----------------

cur.execute("""
CREATE TABLE IF NOT EXISTS applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    drive_id INT,
    application_date DATE,
    status VARCHAR(50) DEFAULT 'Applied',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (drive_id) REFERENCES drives(drive_id)
)
""")

# ---------------- PLACEMENTS TABLE ----------------

cur.execute("""
CREATE TABLE IF NOT EXISTS placements (
    placement_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    company_id INT,
    package FLOAT,
    joining_date DATE,
    status VARCHAR(50) DEFAULT 'Selected',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
)
""")

con.commit()

print("Placement Management Database Connected Successfully")