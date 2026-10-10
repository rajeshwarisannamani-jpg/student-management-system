import json
from pathlib import Path

DATA_FILE = Path("students.json")


def load_students():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print("Warning: students.json could not be read. Starting with an empty list.")
    return []


def save_students(students):
    DATA_FILE.write_text(json.dumps(students, indent=4), encoding="utf-8")


def next_id(students):
    return max((student["id"] for student in students), default=0) + 1


def add_student(students):
    name = input("Student name: ").strip()
    usn = input("USN / student ID: ").strip()
    course = input("Course or department: ").strip()
    if not name or not usn or not course:
        print("All fields are required.")
        return
    if any(s["usn"].casefold() == usn.casefold() for s in students):
        print("That student ID already exists.")
        return
    students.append({"id": next_id(students), "name": name, "usn": usn, "course": course})
    save_students(students)
    print("Student added successfully.")


def view_students(students):
    if not students:
        print("No students saved yet.")
        return
    print("\n--- Student Records ---")
    for s in students:
        print(f'ID: {s["id"]} | Name: {s["name"]} | USN: {s["usn"]} | Course: {s["course"]}')


def search_student(students):
    term = input("Enter student name or USN to search: ").strip().casefold()
    matches = [s for s in students if term in s["name"].casefold() or term in s["usn"].casefold()]
    if not matches:
        print("No matching student found.")
    else:
        for s in matches:
            print(f'ID: {s["id"]} | Name: {s["name"]} | USN: {s["usn"]} | Course: {s["course"]}')


def update_student(students):
    try:
        student_id = int(input("Enter the ID of the student to update: "))
    except ValueError:
        print("Please enter a numeric ID.")
        return
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        print("Student ID not found.")
        return
    name = input(f'New name [{student["name"]}]: ').strip()
    usn = input(f'New USN [{student["usn"]}]: ').strip()
    course = input(f'New course [{student["course"]}]: ').strip()
    if name:
        student["name"] = name
    if usn:
        if any(s["id"] != student_id and s["usn"].casefold() == usn.casefold() for s in students):
            print("That student ID already belongs to another record; USN was not changed.")
        else:
            student["usn"] = usn
    if course:
        student["course"] = course
    save_students(students)
    print("Student record updated.")


def delete_student(students):
    try:
        student_id = int(input("Enter the ID of the student to delete: "))
    except ValueError:
        print("Please enter a numeric ID.")
        return
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        print("Student ID not found.")
        return
    confirm = input(f'Delete {student["name"]}? Type yes to confirm: ').strip().casefold()
    if confirm == "yes":
        students.remove(student)
        save_students(students)
        print("Student deleted.")
    else:
        print("Deletion cancelled.")


def main():
    students = load_students()
    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add student")
        print("2. View all students")
        print("3. Search student")
        print("4. Update student")
        print("5. Delete student")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
