import pymysql
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        return pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    except pymysql.MySQLError as e:
        print("Database connection error:", e)
        return None


def apply_for_drive():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        try:
            student_id = int(input("Enter student ID: "))
            drive_id = int(input("Enter drive ID: "))
        except ValueError:
            print("Student ID and Drive ID must be numbers.")
            return

        cur.execute("""
            SELECT student_id,name,roll_no,branch,cgpa
            FROM students
            WHERE student_id=%s
        """, (student_id,))
        student = cur.fetchone()

        if not student:
            print("Student not found.")
            return

        cur.execute("""
            SELECT d.drive_id,c.company_name,c.job_role,c.package,
                   d.eligibility_cgpa,d.eligibility_branch,d.drive_date
            FROM drives d
            JOIN companies c ON d.company_id=c.company_id
            WHERE d.drive_id=%s
        """, (drive_id,))
        drive = cur.fetchone()

        if not drive:
            print("Placement drive not found.")
            return

        if student[4] < drive[4]:
            print("Student is not eligible. Required CGPA:", drive[4])
            return

        if student[3].strip().lower() != drive[5].strip().lower():
            print("Student is not eligible for this branch.")
            return

        if datetime.now().date() > drive[6]:
            print("This placement drive has already passed.")
            return

        cur.execute("""
            SELECT application_id
            FROM applications
            WHERE student_id=%s AND drive_id=%s
        """, (student_id, drive_id))

        if cur.fetchone():
            print("Student has already applied for this drive.")
            return

        cur.execute("""
            INSERT INTO applications
            (student_id,drive_id,application_date,status)
            VALUES (%s,%s,%s,%s)
        """, (student_id, drive_id, datetime.now().date(), "Applied"))

        con.commit()
        print("Application submitted successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def view_applications():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        cur.execute("""
            SELECT a.application_id,s.name,s.roll_no,
                   c.company_name,c.job_role,
                   a.application_date,a.status
            FROM applications a
            JOIN students s ON a.student_id=s.student_id
            JOIN drives d ON a.drive_id=d.drive_id
            JOIN companies c ON d.company_id=c.company_id
            ORDER BY a.application_id
        """)

        records = cur.fetchall()

        if not records:
            print("No applications found.")
            return

        print("========== APPLICATIONS ==========")

        for r in records:
            print("Application ID :", r[0])
            print("Student         :", r[1])
            print("Roll No         :", r[2])
            print("Company         :", r[3])
            print("Job Role        :", r[4])
            print("Application Date:", r[5])
            print("Status          :", r[6])
            print("-" * 40)

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def search_application():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        try:
            student_id = int(input("Enter student ID: "))
        except ValueError:
            print("Please enter a valid student ID.")
            return

        cur.execute("""
            SELECT a.application_id,s.name,s.roll_no,
                   c.company_name,c.job_role,
                   a.application_date,a.status
            FROM applications a
            JOIN students s ON a.student_id=s.student_id
            JOIN drives d ON a.drive_id=d.drive_id
            JOIN companies c ON d.company_id=c.company_id
            WHERE a.student_id=%s
        """, (student_id,))

        records = cur.fetchall()

        if not records:
            print("No applications found for this student.")
            return

        for r in records:
            print("Application ID :", r[0])
            print("Student         :", r[1])
            print("Roll No         :", r[2])
            print("Company         :", r[3])
            print("Job Role        :", r[4])
            print("Application Date:", r[5])
            print("Status          :", r[6])
            print("-" * 40)

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def update_application():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        try:
            application_id = int(input("Enter application ID: "))
        except ValueError:
            print("Please enter a valid application ID.")
            return

        cur.execute("""
            SELECT application_id
            FROM applications
            WHERE application_id=%s
        """, (application_id,))

        if not cur.fetchone():
            print("Application not found.")
            return

        print("\n1. Applied")
        print("2. Shortlisted")
        print("3. Selected")
        print("4. Rejected")

        choice = input("Enter status choice: ").strip()

        statuses = {
            "1": "Applied",
            "2": "Shortlisted",
            "3": "Selected",
            "4": "Rejected"
        }

        if choice not in statuses:
            print("Invalid status choice.")
            return

        cur.execute("""
            UPDATE applications
            SET status=%s
            WHERE application_id=%s
        """, (statuses[choice], application_id))

        con.commit()
        print("Application status updated successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def delete_application():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        try:
            application_id = int(input("Enter application ID: "))
        except ValueError:
            print("Please enter a valid application ID.")
            return

        cur.execute("""
            SELECT application_id
            FROM applications
            WHERE application_id=%s
        """, (application_id,))

        if not cur.fetchone():
            print("Application not found.")
            return

        confirm = input(
            "Are you sure you want to delete this application? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Delete operation cancelled.")
            return

        cur.execute("""
            DELETE FROM applications
            WHERE application_id=%s
        """, (application_id,))

        con.commit()
        print("Application deleted successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def application_menu():
    while True:
        print("========== APPLICATION MANAGEMENT ==========")
        print("1. Apply for Placement Drive")
        print("2. View Applications")
        print("3. Search Student Applications")
        print("4. Update Application Status")
        print("5. Delete Application")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            apply_for_drive()
        elif choice == "2":
            view_applications()
        elif choice == "3":
            search_application()
        elif choice == "4":
            update_application()
        elif choice == "5":
            delete_application()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please enter 1-6.")