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


def add_company():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== ADD COMPANY ==========")

        while True:
            company_name = input("Enter company name: ").strip()
            if company_name:
                break
            print("Company name cannot be empty.")

        while True:
            location = input("Enter company location: ").strip()
            if location:
                break
            print("Location cannot be empty.")

        while True:
            job_role = input("Enter job role: ").strip()
            if job_role:
                break
            print("Job role cannot be empty.")

        while True:
            try:
                package = float(input("Enter package (LPA): "))
                if package > 0:
                    break
                print("Package must be greater than 0.")
            except ValueError:
                print("Please enter a valid package.")

        cur.execute("""
            INSERT INTO companies
            (company_name,location,job_role,package)
            VALUES (%s,%s,%s,%s)
        """, (company_name, location, job_role, package))

        con.commit()
        print("Company added successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def view_companies():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        cur.execute("""
            SELECT company_id,company_name,location,job_role,package
            FROM companies
            ORDER BY company_id
        """)

        companies = cur.fetchall()

        if not companies:
            print("No company records found.")
            return

        print("================ COMPANY RECORDS ================")

        for company in companies:
            print("Company ID :", company[0])
            print("Company    :", company[1])
            print("Location   :", company[2])
            print("Job Role   :", company[3])
            print("Package    :", company[4], "LPA")
            print("-" * 50)

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def search_company():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== SEARCH COMPANY ==========")

        company_name = input("Enter company name: ").strip()

        if not company_name:
            print("Company name cannot be empty.")
            return

        cur.execute("""
            SELECT company_id,company_name,location,job_role,package
            FROM companies
            WHERE company_name LIKE %s
        """, ("%" + company_name + "%",))

        companies = cur.fetchall()

        if not companies:
            print("Company not found.")
            return

        print("Companies Found")
        print("-" * 50)

        for company in companies:
            print("Company ID :", company[0])
            print("Company    :", company[1])
            print("Location   :", company[2])
            print("Job Role   :", company[3])
            print("Package    :", company[4], "LPA")
            print("-" * 50)

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


def update_company():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== UPDATE COMPANY ==========")

        try:
            company_id = int(input("Enter company ID: "))
        except ValueError:
            print("Please enter a valid company ID.")
            return

        cur.execute(
            "SELECT company_id FROM companies WHERE company_id=%s",
            (company_id,)
        )

        if not cur.fetchone():
            print("Company not found.")
            return

        print("Enter new company details.")

        while True:
            company_name = input("Enter new company name: ").strip()
            if company_name:
                break
            print("Company name cannot be empty.")

        while True:
            location = input("Enter new location: ").strip()
            if location:
                break
            print("Location cannot be empty.")

        while True:
            job_role = input("Enter new job role: ").strip()
            if job_role:
                break
            print("Job role cannot be empty.")

        while True:
            try:
                package = float(input("Enter new package (LPA): "))
                if package > 0:
                    break
                print("Package must be greater than 0.")
            except ValueError:
                print("Please enter a valid package.")

        cur.execute("""
            UPDATE companies
            SET company_name=%s,
                location=%s,
                job_role=%s,
                package=%s
            WHERE company_id=%s
        """, (company_name, location, job_role, package, company_id))

        con.commit()
        print("Company updated successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def delete_company():
    con = get_connection()
    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== DELETE COMPANY ==========")

        try:
            company_id = int(input("Enter company ID: "))
        except ValueError:
            print("Please enter a valid company ID.")
            return

        cur.execute(
            "SELECT company_name FROM companies WHERE company_id=%s",
            (company_id,)
        )

        company = cur.fetchone()

        if not company:
            print("Company not found.")
            return

        print("Company:", company[0])

        confirmation = input(
            "Are you sure you want to delete this company? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print("Delete operation cancelled.")
            return

        cur.execute(
            "DELETE FROM companies WHERE company_id=%s",
            (company_id,)
        )

        con.commit()
        print("Company deleted successfully.")

    except pymysql.IntegrityError:
        con.rollback()
        print(
            "Cannot delete this company because it has "
            "related placement drive or placement records."
        )

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


def company_menu():
    while True:
        print("=" * 45)
        print("       COMPANY MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. Add Company")
        print("2. View Companies")
        print("3. Search Company")
        print("4. Update Company")
        print("5. Delete Company")
        print("6. Back to Main Menu")
        print("=" * 45)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_company()
        elif choice == "2":
            view_companies()
        elif choice == "3":
            search_company()
        elif choice == "4":
            update_company()
        elif choice == "5":
            delete_company()
        elif choice == "6":
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice. Please enter 1-6.")