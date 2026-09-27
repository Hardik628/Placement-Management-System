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


def company_exists(company_id):
    con = get_connection()
    if con is None:
        return False

    try:
        cur = con.cursor()
        cur.execute(
            "SELECT company_name FROM companies WHERE company_id=%s",
            (company_id,)
        )
        company = cur.fetchone()

        if company:
            return company[0]

        return False

    except pymysql.MySQLError as e:
        print("Database error:", e)
        return False

    finally:
        con.close()


def add_drive():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== ADD PLACEMENT DRIVE ==========")

        while True:
            try:
                company_id = int(input("Enter company ID: "))
                company_name = company_exists(company_id)

                if not company_name:
                    print("Company ID does not exist.")
                else:
                    print("Company:", company_name)
                    break

            except ValueError:
                print("Please enter a valid company ID.")

        while True:
            try:
                eligibility_cgpa = float(
                    input("Enter minimum eligible CGPA: ")
                )

                if 0 <= eligibility_cgpa <= 10:
                    break
                print("CGPA must be between 0 and 10.")

            except ValueError:
                print("Please enter a valid CGPA.")

        while True:
            eligibility_branch = input(
                "Enter eligible branch: "
            ).strip()

            if eligibility_branch:
                break

            print("Branch cannot be empty.")

        while True:
            drive_date = input(
                "Enter drive date (YYYY-MM-DD): "
            ).strip()

            try:
                datetime.strptime(drive_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")

        cur.execute("""
            INSERT INTO drives
            (company_id,eligibility_cgpa,eligibility_branch,drive_date)
            VALUES (%s,%s,%s,%s)
        """, (
            company_id,
            eligibility_cgpa,
            eligibility_branch,
            drive_date
        ))

        con.commit()
        print("Placement drive added successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def view_drives():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        cur.execute("""
            SELECT d.drive_id,c.company_name,c.job_role,c.package,
                   d.eligibility_cgpa,d.eligibility_branch,d.drive_date
            FROM drives d
            JOIN companies c ON d.company_id=c.company_id
            ORDER BY d.drive_date
        """)

        drives = cur.fetchall()

        if not drives:
            print("No placement drives found.")
            return

        print("================ PLACEMENT DRIVES ================")

        for drive in drives:
            print("Drive ID          :", drive[0])
            print("Company           :", drive[1])
            print("Job Role          :", drive[2])
            print("Package           :", drive[3], "LPA")
            print("Minimum CGPA      :", drive[4])
            print("Eligible Branch   :", drive[5])
            print("Drive Date        :", drive[6])
            print("-" * 55)

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def search_drive():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== SEARCH PLACEMENT DRIVE ==========")

        search = input(
            "Enter company name or job role: "
        ).strip()

        if not search:
            print("Search value cannot be empty.")
            return

        value = "%" + search + "%"

        cur.execute("""
            SELECT d.drive_id,c.company_name,c.job_role,c.package,
                   d.eligibility_cgpa,d.eligibility_branch,d.drive_date
            FROM drives d
            JOIN companies c ON d.company_id=c.company_id
            WHERE c.company_name LIKE %s
               OR c.job_role LIKE %s
            ORDER BY d.drive_date
        """, (value, value))

        drives = cur.fetchall()

        if not drives:
            print("No matching placement drive found.")
            return

        print("Matching Drives")
        print("-" * 55)

        for drive in drives:
            print("Drive ID        :", drive[0])
            print("Company         :", drive[1])
            print("Job Role        :", drive[2])
            print("Package         :", drive[3], "LPA")
            print("Minimum CGPA    :", drive[4])
            print("Eligible Branch :", drive[5])
            print("Drive Date      :", drive[6])
            print("-" * 55)

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def update_drive():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== UPDATE PLACEMENT DRIVE ==========")

        try:
            drive_id = int(input("Enter drive ID: "))
        except ValueError:
            print("Please enter a valid drive ID.")
            return

        cur.execute(
            "SELECT drive_id FROM drives WHERE drive_id=%s",
            (drive_id,)
        )

        if not cur.fetchone():
            print("Placement drive not found.")
            return

        while True:
            try:
                company_id = int(input("Enter new company ID: "))
                company_name = company_exists(company_id)

                if not company_name:
                    print("Company ID does not exist.")
                else:
                    print("Company:", company_name)
                    break

            except ValueError:
                print("Please enter a valid company ID.")

        while True:
            try:
                eligibility_cgpa = float(
                    input("Enter new minimum eligible CGPA: ")
                )

                if 0 <= eligibility_cgpa <= 10:
                    break

                print("CGPA must be between 0 and 10.")

            except ValueError:
                print("Please enter a valid CGPA.")

        while True:
            eligibility_branch = input(
                "Enter new eligible branch: "
            ).strip()

            if eligibility_branch:
                break

            print("Branch cannot be empty.")

        while True:
            drive_date = input(
                "Enter new drive date (YYYY-MM-DD): "
            ).strip()

            try:
                datetime.strptime(drive_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")

        cur.execute("""
            UPDATE drives
            SET company_id=%s,
                eligibility_cgpa=%s,
                eligibility_branch=%s,
                drive_date=%s
            WHERE drive_id=%s
        """, (
            company_id,
            eligibility_cgpa,
            eligibility_branch,
            drive_date,
            drive_id
        ))

        con.commit()
        print("Placement drive updated successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def delete_drive():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== DELETE PLACEMENT DRIVE ==========")

        try:
            drive_id = int(input("Enter drive ID: "))
        except ValueError:
            print("Please enter a valid drive ID.")
            return

        cur.execute("""
            SELECT d.drive_id,c.company_name,c.job_role,d.drive_date
            FROM drives d
            JOIN companies c ON d.company_id=c.company_id
            WHERE d.drive_id=%s
        """, (drive_id,))

        drive = cur.fetchone()

        if not drive:
            print("Placement drive not found.")
            return

        print("\nDrive Details")
        print("Company  :", drive[1])
        print("Job Role :", drive[2])
        print("Date     :", drive[3])

        confirmation = input(
            "Are you sure you want to delete this drive? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print("Delete operation cancelled.")
            return

        cur.execute(
            "DELETE FROM drives WHERE drive_id=%s",
            (drive_id,)
        )

        con.commit()
        print("Placement drive deleted successfully.")

    except pymysql.IntegrityError:
        con.rollback()
        print(
            "Cannot delete this drive because "
            "students have applications for this drive."
        )

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def drive_menu():
    while True:
        print("=" * 50)
        print("       PLACEMENT DRIVE MANAGEMENT")
        print("=" * 50)
        print("1. Add Placement Drive")
        print("2. View Placement Drives")
        print("3. Search Placement Drive")
        print("4. Update Placement Drive")
        print("5. Delete Placement Drive")
        print("6. Back to Main Menu")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_drive()
        elif choice == "2":
            view_drives()
        elif choice == "3":
            search_drive()
        elif choice == "4":
            update_drive()
        elif choice == "5":
            delete_drive()
        elif choice == "6":
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice. Please enter 1-6.")