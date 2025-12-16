import json
import os
from datetime import datetime  

def time():                 
   return datetime.now().strftime("[%d-%m-%Y  %I:%M:%S %p]")

class Tracker:
    total = 10

    def __init__(self):
        self.name = input("Enter student name : ").lower()
        self.present = int(input("Enter days present : "))
        self.id = int(input("Enter student ID: "))

    def attend(self):
        p = round((self.present / Tracker.total) * 100)
        print(f"\n{time()} Attendance - {self.name}: {self.present}/{Tracker.total} ({p}%)")

    def status(self):
        p = round((self.present / Tracker.total) * 100)
        print()
        if p >= 75:
            print(f"{time()} {self.name} is eligible for Final ({p}%)")
        else:
            print(f"{time()} {self.name} is NOT eligible for Final ({p}%)")
            
    def update_attendance(self, new_p):
        self.present = new_p
        print(f"\n{time()} Attendance updated for {self.name} to {new_p}")
        
    @staticmethod
    def update_multiple_attendance():
        print("\n--- MULTIPLE ATTENDANCE UPDATE ---")
        try:
            count = int(input("How many students do you want to update? : "))
        except ValueError:
            print("Invalid number!")
            return

        for _ in range(count):
            print("\nUpdating next student...")
            s = Tracker.verify_student()
            if s == "logout":
                return
            if s:
                try:
                    new_p = int(input(f"Enter new attendance for {s.name}: "))
                    s.update_attendance(new_p)
                except ValueError:
                    print("Invalid attendance!")

        print(f"\n{time()} [All attendance updated successfully!]\n")

    @staticmethod
    def verify_student():
        name = input("Enter student name : ").lower()

        if name not in students_data:
            print("Student not found.")
            return None

        attempts = 3
        while attempts > 0:
            try:
                id = int(input("Enter student ID : "))
            except:
                print("Invalid ID format!")
                attempts -= 1
                continue

            if id == students_data[name].id:
                return students_data[name]
            else:
                attempts -= 1
                print(f"\n{time()} Incorrect ID! Attempts left: {attempts}")

        print("Too many wrong attempts - Logging out!")
        return "logout"
    
    @classmethod
    def update_total(cls, new_total):
        cls.total = new_total
        print(f"\n{time()} Total working days updated - {new_total}")

    @staticmethod
    def remove_student():
        print()
        name = input("Enter student name to remove : ").lower()
        if name in students_data:
            del students_data[name]
            print(f"{time()} Student '{name}' removed successfully.")
        else:
            print("Student not found.")

students_data = {}
DATA_FILE = None

def save_data():
    global DATA_FILE

    data = {
        "total": Tracker.total,
        "students": []
    }
    for s in students_data.values():
        data["students"].append({
            "name": s.name,
            "present": s.present,
            "id": s.id
        })

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_data():
    global DATA_FILE, students_data

    if not os.path.exists(DATA_FILE):
        return "No Data file"

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    Tracker.total = data.get("total", 10)

    for item in data.get("students", []):
        t = Tracker.__new__(Tracker)
        t.name = item["name"]
        t.present = item["present"]
        t.id = item["id"]
        students_data[t.name] = t

def select_subject():
    global DATA_FILE

    c = input('''\nSelect Subject:
1 - math
2 - python
3 - webd
4 - logout
- ''').lower()

    if c in ["1", "math"]:
        DATA_FILE = "math_data.json"
        load_data()
        return "math"

    elif c in ["2", "python"]:
        DATA_FILE = "python_data.json"
        load_data()
        return "python"

    elif c in ["3", "webd"]:
        DATA_FILE = "webd_data.json"
        load_data()
        return "webd"

    elif c in ["4", "logout"]:
        return "logout"

    else:
        print("Invalid subject")
        return None
def admin_menu():
    while True:
        try:
            m = int(input('''
--- ADMIN MENU ---
1 - Check Attendance
2 - Check Eligibility
3 - Update Total Classes
4 - Add Students
5 - Update Attendance 
6 - Remove Student
7 - Show Student Data
8 - Quit (Back to Subject Select)
- '''))
        except ValueError:
            print("Enter a valid number!")
            continue

        if m == 1:
            s = Tracker.verify_student()
            if s == "logout": 
                return
            if s: s.attend()

        elif m == 2:
            s = Tracker.verify_student()
            if s == "logout": 
                return
            if s: s.status()

        elif m == 3:
            new_total = int(input("Enter new total classes : "))
            Tracker.update_total(new_total)
            save_data()

        elif m == 4:
            num = int(input("How many students to add : "))
            print()
            for _ in range(num):
                s = Tracker()
                students_data[s.name] = s
                print()
            print(f"{time()} Students added!")
            save_data()

        elif m == 5:
            Tracker.update_multiple_attendance()
            save_data()

        elif m == 6:
            Tracker.remove_student()
            save_data()

        elif m == 7:
            print("\n--- STORED STUDENT DATA ---")
            if len(students_data) == 0:
                print("No students found")
            else:
                for s in students_data.values():
                    print(f"{time()} Name: {s.name}, ID: {s.id}, Present: {s.present}")

        elif m == 8:
            break

        else:
            print("Invalid option!")
def teacher_menu():
    while True:
        try:
            m = int(input('''
--- TEACHER MENU ---
1 - Check Attendance
2 - Check Eligibility
3 - Update Total Classes
4 - Update Attendance
5 - Show Student Data
6 - Quit (Back to Subject Select)
- '''))
        except ValueError:
            print("Enter a valid number!")
            continue

        if m == 1:
            s = Tracker.verify_student()
            if s == "logout": return
            if s: s.attend()

        elif m == 2:
            s = Tracker.verify_student()
            if s == "logout": return
            if s: s.status()

        elif m == 3:
            new_total = int(input("Enter new total classes : "))
            Tracker.update_total(new_total)
            save_data()

        elif m == 4:
            Tracker.update_multiple_attendance()
            save_data()

        elif m == 5:
            print("\n--- STORED STUDENT DATA ---")
            for s in students_data.values():
                print(f"{time()} Name: {s.name}, ID: {s.id}, Present: {s.present}")

        elif m == 6:
            break
def student_menu():
    while True:
        try:
            m = int(input('''
--- STUDENT MENU ---
1 - Check Attendance
2 - Check Eligibility
3 - Quit (Back to Subject Select)
- '''))
        except ValueError:
            print("Enter a valid number")
            continue

        if m == 1:
            s = Tracker.verify_student()
            if s == "logout": return
            if s: s.attend()

        elif m == 2:
            s = Tracker.verify_student()
            if s == "logout": return
            if s: s.status()

        elif m == 3:
            break
        
attempts = 3
while attempts > 0:
    o = input("\nLogin as admin/teacher/student : ").lower()

    if o == "admin":
        while attempts > 0:
            k = input("Enter login key : ")
            if k == '12345':
                print(f"\n{time()} Admin Access Granted")

                while True:
                    subject = select_subject()

                    if subject == "logout":
                        print("Logging out...\n")
                        break

                    elif subject:
                        admin_menu()

                break

            else:
                attempts -= 1
                print(f"Invalid login. Attempts left: {attempts}")

    elif o == "teacher":
        while attempts > 0:
            k = input("Enter login key : ")
            if k == '1234':
                print(f"\n{time()} Teacher Access Granted")

                while True:
                    subject = select_subject()

                    if subject == "logout":
                        print("Logging out...\n")
                        break

                    elif subject:
                        teacher_menu()

                break

            else:
                attempts -= 1
                print(f"Invalid login. Attempts left: {attempts}")

    elif o == "student":
        while attempts > 0:
            k = input("Enter login key : ")
            if k == '123':
                print(f"\n{time()} Student Access Granted")

                while True:
                    subject = select_subject()

                    if subject == "logout":
                        print("Logging out...\n")
                        break

                    elif subject:
                        student_menu()

                break

            else:
                attempts -= 1
                print(f"Invalid login. Attempts left: {attempts}")

    else:
        attempts -= 1
        print(f"Invalid login. Attempts left: {attempts}")

if attempts == 0:
    print("Too many attempts. Access locked.")
