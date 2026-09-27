import students
import companies
import drives
import applications
import placements
import reports


def main():
    while True:
        print("========== PLACEMENT MANAGEMENT SYSTEM ==========")
        print("1. Student Management")
        print("2. Company Management")
        print("3. Placement Drive Management")
        print("4. Application Management")
        print("5. Placement Management")
        print("6. Reports")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            students.student_menu()

        elif choice == "2":
            companies.company_menu()

        elif choice == "3":
            drives.drive_menu()

        elif choice == "4":
            applications.application_menu()

        elif choice == "5":
            placements.placement_menu()

        elif choice == "6":
            reports.report_menu()

        elif choice == "7":
            print("Thank you for using Placement Management System.")
            break

        else:
            print("Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()