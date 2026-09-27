import pymysql
import os
from dotenv import load_dotenv

load_dotenv()


# DATABASE CONNECTION
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


# ADD STUDENT
def add_student():

    con = get_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== ADD STUDENT ==========")

        while True:
            name = input("Enter student name: ").strip()

            if name == "":
                print("Name cannot be empty.")
            elif not name.replace(" ", "").isalpha():
                print("Name should contain only letters.")
            else:
                break

        while True:
            roll_no = input("Enter roll number: ").strip()

            if roll_no == "":
                print("Roll number cannot be empty.")
                continue

            cur.execute(
                "SELECT student_id FROM students WHERE roll_no = %s",
                (roll_no,)
            )

            if cur.fetchone():
                print("Roll number already exists. Enter another roll number.")
            else:
                break

        while True:
            email = input("Enter email: ").strip()

            if "@" in email and "." in email:
                break
            else:
                print("Enter a valid email address.")

        while True:
            phone = input("Enter phone number: ").strip()

            if phone.isdigit() and len(phone) == 10:
                break
            else:
                print("Phone number must contain exactly 10 digits.")

        while True:
            branch = input("Enter branch: ").strip()

            if branch == "":
                print("Branch cannot be empty.")
            else:
                break

        while True:
            try:
                cgpa = float(input("Enter CGPA: "))

                if 0 <= cgpa <= 10:
                    break
                else:
                    print("CGPA must be between 0 and 10.")

            except ValueError:
                print("Please enter a valid number.")

        while True:
            try:
                graduation_year = int(
                    input("Enter graduation year: ")
                )

                if 2000 <= graduation_year <= 2100:
                    break
                else:
                    print("Enter a valid graduation year.")

            except ValueError:
                print("Please enter a valid year.")

        query = """
        INSERT INTO students
        (name, roll_no, email, phone, branch, cgpa, graduation_year)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            name,
            roll_no,
            email,
            phone,
            branch,
            cgpa,
            graduation_year
        )

        cur.execute(query, values)
        con.commit()

        print("Student added successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


# VIEW STUDENTS
def view_students():

    con = get_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        cur.execute("""
            SELECT student_id, name, roll_no, email,
                   phone, branch, cgpa, graduation_year
            FROM students
            ORDER BY student_id
        """)

        students = cur.fetchall()

        if not students:
            print("No student records found.")
            return

        print("================ STUDENT RECORDS ================")

        for student in students:
            print("Student ID       :", student[0])
            print("Name             :", student[1])
            print("Roll Number      :", student[2])
            print("Email            :", student[3])
            print("Phone            :", student[4])
            print("Branch           :", student[5])
            print("CGPA             :", student[6])
            print("Graduation Year  :", student[7])
            print("-" * 50)

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


# SEARCH STUDENT
def search_student():

    con = get_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== SEARCH STUDENT ==========")

        roll_no = input("Enter roll number: ").strip()

        if roll_no == "":
            print("Roll number cannot be empty.")
            return

        cur.execute("""
            SELECT student_id, name, roll_no, email,
                   phone, branch, cgpa, graduation_year
            FROM students
            WHERE roll_no = %s
        """, (roll_no,))

        student = cur.fetchone()

        if student is None:
            print("Student not found.")
            return

        print("Student Found")
        print("-" * 40)
        print("Student ID      :", student[0])
        print("Name            :", student[1])
        print("Roll Number     :", student[2])
        print("Email           :", student[3])
        print("Phone           :", student[4])
        print("Branch          :", student[5])
        print("CGPA            :", student[6])
        print("Graduation Year :", student[7])

    except pymysql.MySQLError as e:
        print("Database error:", e)

    finally:
        con.close()


# UPDATE STUDENT
def update_student():

    con = get_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== UPDATE STUDENT ==========")

        roll_no = input("Enter roll number: ").strip()

        cur.execute(
            "SELECT * FROM students WHERE roll_no = %s",
            (roll_no,)
        )

        student = cur.fetchone()

        if student is None:
            print("Student not found.")
            return

        print("Enter new student details.")

        while True:
            name = input("Enter new name: ").strip()

            if name == "":
                print("Name cannot be empty.")
            elif not name.replace(" ", "").isalpha():
                print("Name should contain only letters.")
            else:
                break

        while True:
            email = input("Enter new email: ").strip()

            if "@" in email and "." in email:
                break
            else:
                print("Enter a valid email.")

        while True:
            phone = input("Enter new phone number: ").strip()

            if phone.isdigit() and len(phone) == 10:
                break
            else:
                print("Phone number must contain exactly 10 digits.")

        while True:
            branch = input("Enter new branch: ").strip()

            if branch == "":
                print("Branch cannot be empty.")
            else:
                break

        while True:
            try:
                cgpa = float(input("Enter new CGPA: "))

                if 0 <= cgpa <= 10:
                    break
                else:
                    print("CGPA must be between 0 and 10.")

            except ValueError:
                print("Please enter a valid number.")

        while True:
            try:
                graduation_year = int(
                    input("Enter new graduation year: ")
                )

                if 2000 <= graduation_year <= 2100:
                    break
                else:
                    print("Enter a valid graduation year.")

            except ValueError:
                print("Please enter a valid year.")

        query = """
        UPDATE students
        SET name = %s,
            email = %s,
            phone = %s,
            branch = %s,
            cgpa = %s,
            graduation_year = %s
        WHERE roll_no = %s
        """

        values = (
            name,
            email,
            phone,
            branch,
            cgpa,
            graduation_year,
            roll_no
        )

        cur.execute(query, values)
        con.commit()

        print("Student updated successfully.")

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


# DELETE STUDENT
def delete_student():

    con = get_connection()

    if con is None:
        return

    try:
        cur = con.cursor()

        print("========== DELETE STUDENT ==========")

        roll_no = input("Enter roll number: ").strip()

        cur.execute(
            "SELECT name FROM students WHERE roll_no = %s",
            (roll_no,)
        )

        student = cur.fetchone()

        if student is None:
            print("Student not found.")
            return

        print("Student Name:", student[0])

        confirmation = input(
            "Are you sure you want to delete this student? (yes/no): "
        ).lower().strip()

        if confirmation != "yes":
            print("Delete operation cancelled.")
            return

        cur.execute(
            "DELETE FROM students WHERE roll_no = %s",
            (roll_no,)
        )

        con.commit()

        print("Student deleted successfully.")

    except pymysql.IntegrityError:
        con.rollback()

        print(
            "Cannot delete this student because "
            "the student has related placement/application records."
        )

    except pymysql.MySQLError as e:
        con.rollback()
        print("Database error:", e)

    finally:
        con.close()


# STUDENT MENU
def student_menu():

    while True:
        print("=" * 45)
        print("       STUDENT MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Back to Main Menu")

        print("=" * 45)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            print("Returning to main menu...")
            break

        else:
            print("Invalid choice. Please enter 1-6.")