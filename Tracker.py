class Tracker:
    total = 10

    def __init__(self):
        self.name = input("Enter student name : ").lower()
        self.present = int(input("Enter days present : "))
        self.id = int(input("Enter student ID: "))

    def attend(self):
        p = round((self.present / Tracker.total) * 100)
        print(f"\nAttendance → {self.name}: {self.present}/{Tracker.total} ({p}%)")

    def status(self):
        p = round((self.present / Tracker.total) * 100)
        print()
        if p >= 75:
            print(f"{self.name} is eligible for Final ({p}%)")
        else:
            print(f"{self.name} is NOT eligible for Final ({p}%)")

    def update_attendance(self, new_p):
        self.present = new_p
        print(f"\nAttendance updated for {self.name} to {new_p}")
    @staticmethod
    def verify_student():
        """Returns student object if verified, else None."""

        name = input("Enter student name : ").lower()

        if name not in students_data:
            print("Student not found.")
            return None

        attempts = 3
        while attempts > 0:
            try:
                sid = int(input("Enter student ID : "))
            except:
                print("Invalid ID format!")
                attempts -= 1
                continue

            if sid == students_data[name].id:
                return students_data[name]

            else:
                attempts -= 1
                print(f"Incorrect ID! Attempts left: {attempts}")

        print("Too many wrong attempts → Logging out!")
        return "logout"

    
    @classmethod
    def update_total(cls, new_total):
        cls.total = new_total
        print(f"\nTotal working days updated → {new_total}")

    @staticmethod
    def remove_student():
        print()
        name = input("Enter student name to remove : ").lower()
        if name in students_data:
            del students_data[name]
            print(f"Student '{name}' removed successfully.")
        else:
            print("Student not found.")
            


students_data = {}



def admin_menu():
    while True:
        try:
            m = int(input('''
--- ADMIN MENU ---
1 → Check Attendance
2 → Check Eligibility
3 → Update Total Classes
4 → Add Students
5 → Update Attendance
6 → Remove Student
7 → Show Student Data
8 → Quit
→ '''))
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

        elif m == 4:
            num = int(input("How many students to add : "))
            for _ in range(num):
                s = Tracker()
                students_data[s.name] = s
            print("Students added!")

        elif m == 5:
            s = Tracker.verify_student()
            if s == "logout": return
            if s:
                new_p = int(input("Enter new attendance : "))
                s.update_attendance(new_p)

        elif m == 6:
            Tracker.remove_student()

        elif m == 7:
            print("\n--- STORED STUDENT DATA ---")
            for s in students_data.values():
                print(f"Name: {s.name}, ID: {s.id}, Present: {s.present}")

        elif m == 8:
            print("Logging out as Admin!")
            break

        else:
            print("Invalid option!")


def teacher_menu():
    while True:
        try:
            m = int(input('''
--- TEACHER MENU ---
1 → Check Attendance
2 → Check Eligibility
3 → Update Total Classes
4 → Update Attendance
5 → Show Student Data
6 → Quit
→ '''))
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

        elif m == 4:
            s = Tracker.verify_student()
            if s == "logout": return
            if s:
                new_p = int(input("Enter new attendance : "))
                s.update_attendance(new_p)

        elif m == 5:
            print("\n--- STORED STUDENT DATA ---")
            for s in students_data.values():
                print(f"Name: {s.name}, ID: {s.id}, Present: {s.present}")

        elif m == 6:
            print("Logging out as Teacher")
            break


def student_menu():
    while True:
        try:
            m = int(input('''
--- STUDENT MENU ---
1 → Check Attendance
2 → Check Eligibility
3 → Quit
→ '''))
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
            print("Logging out as Student")
            break

attempts = 3

while attempts > 0:
    o = input("\nLogin as admin/teacher/student : ").lower()

    if o == "admin":
        while attempts > 0:
            k = input("Enter login key : ")
            if k == '27092006':
                print("\nAdmin Access Granted")
                admin_menu()
                break
            else:
                attempts -= 1
                print(f"Invalid login. Attempts left: {attempts}")

    elif o == "teacher":
        while attempts > 0:
            k = input("Enter login key : ")
            if k == '12345':
                print("\nTeacher Access Granted")
                teacher_menu()
                break
            else:
                attempts -= 1
                print(f"Invalid login. Attempts left: {attempts}")

    elif o == "student":
        while attempts > 0:
            k = input("Enter login key : ")
            if k == '123':
                print("\nStudent Access Granted")
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
