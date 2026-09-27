import pymysql
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


def student_report():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        cur.execute("""
            SELECT s.student_id,s.name,s.roll_no,s.branch,s.cgpa,
                   c.company_name,p.package,p.status
            FROM students s
            LEFT JOIN placements p ON s.student_id=p.student_id
            LEFT JOIN companies c ON p.company_id=c.company_id
            ORDER BY s.student_id
        """)

        records = cur.fetchall()

        if not records:
            print("No student records found.")
            return

        print("========== STUDENT REPORT ==========")

        for r in records:
            print("Student ID :", r[0])
            print("Name       :", r[1])
            print("Roll No    :", r[2])
            print("Branch     :", r[3])
            print("CGPA       :", r[4])
            print("Company    :", r[5] if r[5] else "Not Placed")
            print("Package    :", str(r[6]) + " LPA" if r[6] else "N/A")
            print("Status     :", r[7] if r[7] else "Not Placed")
            print("-" * 40)

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def placement_report():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        cur.execute("""
            SELECT c.company_name,
                   COUNT(p.placement_id),
                   MAX(p.package),
                   AVG(p.package)
            FROM companies c
            LEFT JOIN placements p ON c.company_id=p.company_id
            GROUP BY c.company_id,c.company_name
            ORDER BY COUNT(p.placement_id) DESC
        """)

        records = cur.fetchall()

        if not records:
            print("No placement records found.")
            return

        print("========== PLACEMENT REPORT ==========")

        for r in records:
            print("Company        :", r[0])
            print("Students Placed:", r[1])
            print("Highest Package:", r[2] if r[2] else "N/A")
            print("Average Package:", round(r[3], 2) if r[3] else "N/A")
            print("-" * 40)

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def application_report():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        cur.execute("""
            SELECT status,COUNT(*)
            FROM applications
            GROUP BY status
        """)

        records = cur.fetchall()

        if not records:
            print("No application records found.")
            return

        print("========== APPLICATION REPORT ==========")

        for r in records:
            print(r[0], ":", r[1])

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def company_report():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        cur.execute("""
            SELECT c.company_name,c.job_role,c.package,
                   COUNT(d.drive_id)
            FROM companies c
            LEFT JOIN drives d ON c.company_id=d.company_id
            GROUP BY c.company_id,c.company_name,c.job_role,c.package
        """)

        records = cur.fetchall()

        if not records:
            print("No company records found.")
            return

        print("\n========== COMPANY REPORT ==========")

        for r in records:
            print("Company   :", r[0])
            print("Job Role  :", r[1])
            print("Package   :", r[2], "LPA")
            print("Drives    :", r[3])
            print("-" * 40)

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def report_menu():
    while True:
        print("========== REPORT MANAGEMENT ==========")
        print("1. Student Report")
        print("2. Placement Report")
        print("3. Application Report")
        print("4. Company Report")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            student_report()
        elif choice == "2":
            placement_report()
        elif choice == "3":
            application_report()
        elif choice == "4":
            company_report()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter 1-5.")