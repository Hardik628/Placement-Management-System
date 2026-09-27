import pymysql
import os
from datetime import datetime
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


def add_placement():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        try:
            student_id = int(input("Enter student ID: "))
            company_id = int(input("Enter company ID: "))
            package = float(input("Enter package (LPA): "))
        except ValueError:
            print("Please enter valid numbers.")
            return

        if package <= 0:
            print("Package must be greater than 0.")
            return

        joining_date = input("Enter joining date (YYYY-MM-DD): ").strip()

        try:
            joining_date = datetime.strptime(
                joining_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            print("Invalid date format.")
            return

        cur.execute(
            "SELECT name FROM students WHERE student_id=%s",
            (student_id,)
        )
        student = cur.fetchone()

        if not student:
            print("Student not found.")
            return

        cur.execute(
            "SELECT company_name FROM companies WHERE company_id=%s",
            (company_id,)
        )
        company = cur.fetchone()

        if not company:
            print("Company not found.")
            return

        cur.execute("""
            SELECT a.application_id
            FROM applications a
            JOIN drives d ON a.drive_id=d.drive_id
            WHERE a.student_id=%s
            AND d.company_id=%s
            AND a.status='Selected'
        """, (student_id, company_id))

        if not cur.fetchone():
            print("Student is not selected for this company.")
            return

        cur.execute(
            "SELECT placement_id FROM placements WHERE student_id=%s",
            (student_id,)
        )

        if cur.fetchone():
            print("Placement already exists for this student.")
            return

        cur.execute("""
            INSERT INTO placements
            (student_id,company_id,package,joining_date,status)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            student_id,
            company_id,
            package,
            joining_date,
            "Selected"
        ))

        con.commit()
        print("Placement added successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def view_placements():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        cur.execute("""
            SELECT p.placement_id,s.name,s.roll_no,
                   c.company_name,p.package,
                   p.joining_date,p.status
            FROM placements p
            JOIN students s ON p.student_id=s.student_id
            JOIN companies c ON p.company_id=c.company_id
            ORDER BY p.placement_id
        """)

        records = cur.fetchall()

        if not records:
            print("No placement records found.")
            return

        print("========== PLACEMENTS ==========")

        for r in records:
            print("Placement ID :", r[0])
            print("Student      :", r[1])
            print("Roll No      :", r[2])
            print("Company      :", r[3])
            print("Package      :", r[4], "LPA")
            print("Joining Date :", r[5])
            print("Status       :", r[6])
            print("-" * 35)

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def search_placement():
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
            SELECT p.placement_id,s.name,s.roll_no,
                   c.company_name,p.package,
                   p.joining_date,p.status
            FROM placements p
            JOIN students s ON p.student_id=s.student_id
            JOIN companies c ON p.company_id=c.company_id
            WHERE p.student_id=%s
        """, (student_id,))

        records = cur.fetchall()

        if not records:
            print("No placement found for this student.")
            return

        for r in records:
            print("Placement ID :", r[0])
            print("Student      :", r[1])
            print("Roll No      :", r[2])
            print("Company      :", r[3])
            print("Package      :", r[4], "LPA")
            print("Joining Date :", r[5])
            print("Status       :", r[6])

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def update_placement():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        try:
            placement_id = int(input("Enter placement ID: "))
        except ValueError:
            print("Please enter a valid placement ID.")
            return

        cur.execute(
            "SELECT placement_id FROM placements WHERE placement_id=%s",
            (placement_id,)
        )

        if not cur.fetchone():
            print("Placement not found.")
            return

        print("1. Selected")
        print("2. Joined")
        print("3. Not Joined")

        choice = input("Enter status choice: ").strip()

        statuses = {
            "1": "Selected",
            "2": "Joined",
            "3": "Not Joined"
        }

        if choice not in statuses:
            print("Invalid status choice.")
            return

        cur.execute("""
            UPDATE placements
            SET status=%s
            WHERE placement_id=%s
        """, (statuses[choice], placement_id))

        con.commit()
        print("Placement status updated successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def delete_placement():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        try:
            placement_id = int(input("Enter placement ID: "))
        except ValueError:
            print("Please enter a valid placement ID.")
            return

        cur.execute(
            "SELECT placement_id FROM placements WHERE placement_id=%s",
            (placement_id,)
        )

        if not cur.fetchone():
            print("Placement not found.")
            return

        confirm = input(
            "Are you sure you want to delete this placement? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Delete operation cancelled.")
            return

        cur.execute(
            "DELETE FROM placements WHERE placement_id=%s",
            (placement_id,)
        )

        con.commit()
        print("Placement deleted successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def placement_menu():
    while True:
        print("========== PLACEMENT MANAGEMENT ==========")
        print("1. Add Placement")
        print("2. View Placements")
        print("3. Search Placement")
        print("4. Update Placement Status")
        print("5. Delete Placement")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_placement()
        elif choice == "2":
            view_placements()
        elif choice == "3":
            search_placement()
        elif choice == "4":
            update_placement()
        elif choice == "5":
            delete_placement()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please enter 1-6.")