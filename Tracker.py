import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

def today():
    return datetime.now().strftime("%d-%m-%Y")

SUBJECT_KEYS = {
    "math": "MATH123",
    "python": "PY123",
    "webd": "WEB123"
}

students_data = {}
DATA_FILE = None
TOTAL = 10

class Student:
    def __init__(self, name, sid, present, history=None):
        self.name = name.lower()
        self.id = sid
        self.present = present
        self.history = history if history else []

    def percent(self):
        return round((self.present / TOTAL) * 100) if TOTAL else 0

    def eligible(self):
        return self.percent() >= 75

    def add_history(self, value):
        self.history.append({"date": today(), "present": value})

def save_data():
    data = {"total": TOTAL, "students": []}
    for s in students_data.values():
        data["students"].append({
            "name": s.name,
            "id": s.id,
            "present": s.present,
            "history": s.history
        })
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    global TOTAL
    students_data.clear()
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    TOTAL = data.get("total", 10)
    for i in data.get("students", []):
        students_data[i["name"]] = Student(
            i["name"], i["id"], i["present"], i.get("history", [])
        )

def get_student(name, sid):
    name = name.lower().strip()
    if name not in students_data:
        messagebox.showerror("Error", "Student not found")
        return None
    if students_data[name].id != sid:
        messagebox.showerror("Access Denied", "Incorrect Student ID")
        return None
    return students_data[name]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Attendance System")
        self.geometry("550x650")
        self.resizable(False, False)
        self.role = None
        self.frames = {}
        for F in (LoginPage, SubjectPage, TeacherKeyPage,
                  AdminPage, TeacherPage, StudentPage):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)
        self.show(LoginPage)

    def show(self, page):
        self.frames[page].tkraise()

class LoginPage(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        tk.Label(self, text="Login", font=("Arial", 18, "bold")).pack(pady=20)
        self.role_box = ttk.Combobox(
            self, values=["admin", "teacher", "student"], state="readonly"
        )
        self.role_box.pack()
        self.role_box.set("admin")
        self.key = tk.Entry(self, show="*")
        self.key.pack(pady=10)
        tk.Button(self, text="Login", command=self.login).pack(pady=20)

    def login(self):
        r = self.role_box.get()
        k = self.key.get()
        if (r == "admin" and k == "12345") or \
           (r == "teacher" and k == "1234") or \
           (r == "student" and k == "123"):
            self.master.role = r
            if r == "teacher":
                self.master.show(TeacherKeyPage)
            else:
                self.master.show(SubjectPage)
        else:
            messagebox.showerror("Error", "Invalid Login Key")

class SubjectPage(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        tk.Label(self, text="Select Subject", font=("Arial", 16, "bold")).pack(pady=20)
        for s in ("math", "python", "webd"):
            tk.Button(self, text=s.title(), width=20,
                      command=lambda x=s: self.select(x)).pack(pady=5)
        tk.Button(self, text="Logout",
                  command=lambda: root.show(LoginPage)).pack(pady=20)

    def select(self, subject):
        global DATA_FILE
        DATA_FILE = f"{subject}_data.json"
        load_data()
        if self.master.role == "admin":
            self.master.show(AdminPage)
        else:
            self.master.show(StudentPage)

class TeacherKeyPage(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        tk.Label(self, text="Enter Subject Key", font=("Arial", 16, "bold")).pack(pady=20)
        self.entry = tk.Entry(self, show="*")
        self.entry.pack(pady=10)
        tk.Button(self, text="Submit", command=self.verify).pack(pady=10)
        tk.Button(self, text="Logout",
                  command=lambda: root.show(LoginPage)).pack(pady=10)

    def verify(self):
        if self.entry.get() in SUBJECT_KEYS.values():
            self.master.show(TeacherPage)
        else:
            messagebox.showerror("Error", "Invalid Subject Key")

class BaseMenu(tk.Frame):
    def create_inputs(self):
        tk.Label(self, text="Student Name").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        tk.Label(self, text="Student ID").pack()
        self.id_entry = tk.Entry(self)
        self.id_entry.pack(pady=5)

    def get_student_obj(self):
        try:
            sid = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid ID")
            return None
        return get_student(self.name_entry.get(), sid)

    def logout(self):
        self.master.show(LoginPage)

    def switch_subject(self):
        self.master.show(SubjectPage)

class AdminPage(BaseMenu):
    def __init__(self, root):
        super().__init__(root)
        tk.Label(self, text="Admin Panel", font=("Arial", 16, "bold")).pack(pady=10)
        self.create_inputs()
        tk.Button(self, text="Check Attendance", command=self.attend).pack()
        tk.Button(self, text="Check Eligibility", command=self.status).pack()
        tk.Button(self, text="Update Attendance", command=self.update).pack()
        tk.Button(self, text="Class Attendance Update",
                  command=self.class_attendance_update).pack()
        tk.Button(self, text="Update Total Classes", command=self.update_total).pack()
        tk.Button(self, text="Show Student Data", command=self.show_all).pack()

        self.remove_btn = tk.Button(self, text="Remove Student", command=self.remove)
        self.remove_btn.pack()

        self.add_btn = tk.Button(self, text="Add Student", command=self.add)
        self.add_btn.pack()

        tk.Button(self, text="Switch Subject", command=self.switch_subject).pack()
        tk.Button(self, text="Logout", command=self.logout).pack(pady=10)

    def class_attendance_update(self):
        win = tk.Toplevel(self)
        win.title("Class Attendance Update")
        canvas = tk.Canvas(win)
        scrollbar = tk.Scrollbar(win, command=canvas.yview)
        frame = tk.Frame(canvas)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        vars = {}
        for s in students_data.values():
            v = tk.StringVar(value="absent")
            vars[s.name] = v
            tk.Label(frame, text=f"{s.name} ({s.id})").pack()
            tk.Radiobutton(frame, text="Present", variable=v, value="present").pack()
            tk.Radiobutton(frame, text="Absent", variable=v, value="absent").pack()

        def save():
            for n, v in vars.items():
                if v.get() == "present":
                    students_data[n].present += 1
            save_data()
            win.destroy()

        tk.Button(win, text="Save", command=save).pack()
        tk.Button(win, text="Back", command=win.destroy).pack()

    def show_all(self):
        msg = "\n".join(f"{s.name} | {s.id} | {s.present}/{TOTAL}" for s in students_data.values())
        messagebox.showinfo("Students", msg or "No students")

    def attend(self):
        s = self.get_student_obj()
        if s:
            messagebox.showinfo("Attendance", f"{s.name}: {s.present}/{TOTAL}")

    def status(self):
        s = self.get_student_obj()
        if s:
            messagebox.showinfo("Eligibility", "ELIGIBLE" if s.eligible() else "NOT ELIGIBLE")

    def update(self):
        s = self.get_student_obj()
        if s:
            n = simpledialog.askinteger("Update", "Enter present days")
            if n is not None:
                s.present = n
                save_data()

    def update_total(self):
        global TOTAL
        t = simpledialog.askinteger("Update Total", "Enter total classes")
        if t:
            TOTAL = t
            save_data()

    def remove(self):
        s = self.get_student_obj()
        if s:
            del students_data[s.name]
            save_data()

    def add(self):
        win = tk.Toplevel(self)
        n = tk.Entry(win); n.pack()
        i = tk.Entry(win); i.pack()
        p = tk.Entry(win); p.pack()
        tk.Button(win, text="Save",
                  command=lambda: (students_data.setdefault(
                      n.get().lower(), Student(n.get(), int(i.get()), int(p.get()))),
                      save_data(), win.destroy())).pack()

class TeacherPage(AdminPage):
    def __init__(self, root):
        super().__init__(root)
        self.add_btn.pack_forget()
        self.remove_btn.pack_forget()

    def switch_subject(self):
        self.master.show(TeacherKeyPage)

class StudentPage(BaseMenu):
    def __init__(self, root):
        super().__init__(root)
        tk.Label(self, text="Student Panel", font=("Arial", 16, "bold")).pack(pady=10)
        self.create_inputs()
        tk.Button(self, text="View Attendance", command=self.attend).pack()
        tk.Button(self, text="Check Eligibility", command=self.status).pack()
        tk.Button(self, text="Switch Subject", command=self.switch_subject).pack()
        tk.Button(self, text="Logout", command=self.logout).pack(pady=10)

    def attend(self):
        s = self.get_student_obj()
        if s:
            messagebox.showinfo("Attendance", f"{s.name}: {s.present}/{TOTAL}")

    def status(self):
        s = self.get_student_obj()
        if s:
            messagebox.showinfo("Eligibility", "ELIGIBLE" if s.eligible() else "NOT ELIGIBLE")

if __name__ == "__main__":
    App().mainloop()
