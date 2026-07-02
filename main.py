import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
import sqlite3
import webbrowser
import os

def class_routine():
    path = os.path.abspath("class-routine.html")
    webbrowser.open("file://" + path)
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    department TEXT,
    semester TEXT,
    password TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS todo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cgpa_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch TEXT,
    semester INTEGER,
    cgpa REAL,
    grade TEXT,
    performance TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notices(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    event_date TEXT,
    status TEXT,
    UNIQUE(title, event_date)
)
""")
conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    title TEXT,
    filepath TEXT
)
""")

conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

conn.commit()
cursor.execute("SELECT * FROM admin")

if cursor.fetchone() is None:

    cursor.execute("""
        INSERT INTO admin(username, password)
        VALUES(?, ?)
        """, ("Admin", "8464"))

    conn.commit()
cursor.execute("""
INSERT OR IGNORE INTO admin(username, password)
VALUES(?, ?)
""", ("Admin", "8464"))
conn.commit()
cursor.execute(
    "DELETE FROM notices WHERE title=?",
    ("Semester Exam starts from 15 July",)
)
conn.commit()
print("Database Connected Successfully")
subjects = {
    "B.Tech CSE": {
        "Semester 1": [
            "Mathematics-I",
            "Physics",
            "Programming in C",
            "English",
            "Workshop",
            "Basic Electronics"
        ]
    }
}

def login():

    login_window = tk.Toplevel(root)

    login_window.title("Student Login")

    login_window.geometry("400x300")

    login_window.configure(bg="#EAF4FF")

    tk.Label(
        login_window,
        text="Student Login",
        font=("Arial",18,"bold"),
        bg="#EAF4FF"
    ).pack(pady=15)

    tk.Label(login_window,text="Email",bg="#EAF4FF").pack()

    email_entry=tk.Entry(login_window,width=30)

    email_entry.pack(pady=5)

    tk.Label(login_window,text="Password",bg="#EAF4FF").pack()

    password_entry=tk.Entry(login_window,width=30,show="*")

    password_entry.pack(pady=5)
    
    login_button = tk.Button(
        login_window,
        text="Login",
        font=("Arial", 12, "bold"),
        bg="#0078D7",
        fg="white",
        width=18,
        command=lambda: check_login(
            email_entry.get(),
            password_entry.get()
        )
    )

    login_button.pack(pady=20)

def check_login(email, password):

    cursor.execute(
        "SELECT * FROM students WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    if user:
        dashboard()

    else:
        messagebox.showerror(
            "Error",
            "Invalid Email or Password"
        )    

def admin_login():

    admin_window = tk.Toplevel(root)

    admin_window.title("Admin Login")

    admin_window.geometry("400x300")

    admin_window.configure(bg="#EAF4FF")

    tk.Label(
        admin_window,
        text="Admin Login",
        font=("Arial",18,"bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=20)

    tk.Label(admin_window, text="Username", bg="#EAF4FF").pack()

    username_entry = tk.Entry(admin_window, width=30)
    username_entry.pack(pady=5)

    tk.Label(admin_window, text="Password", bg="#EAF4FF").pack()

    password_entry = tk.Entry(admin_window, width=30, show="*")
    password_entry.pack(pady=5)

    tk.Button(
        admin_window,
        text="Login",
        bg="#FF9800",
        fg="white",
        width=15,
        command=lambda: check_admin(
            username_entry.get(),
            password_entry.get()
        )
    ).pack(pady=20)

def admin_panel():

    panel = tk.Toplevel(root)

    panel.title("Admin Panel")

    panel.geometry("500x500")

    panel.configure(bg="#EAF4FF")

    tk.Label(
        panel,
        text="ADMIN PANEL",
        font=("Arial",20,"bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=20)

    tk.Button(
        panel,
        text="➕ Add Notice",
        width=20,
        height=2,
        command=add_notice
    ).pack(pady=10)

    tk.Button(
        panel,
        text="➕ Add Event",
        width=20,
        height=2,
        command=add_event
    ).pack(pady=10)

    tk.Button(
        panel,
        text="🗑 Delete Notice",
        width=20,
        height=2,
        command=delete_notice
    ).pack(pady=10)

    tk.Button(
        panel,
        text="🗑 Delete Event",
        width=20,
        height=2,
        command=delete_event
    ).pack(pady=10)
    tk.Button(
        panel,
        text="📚 Upload Notes",
        width=20,
        height=2,
        command=upload_notes
    ).pack(pady=10)

def add_notice():

    notice_window = tk.Toplevel(root)

    notice_window.title("Add Notice")

    notice_window.geometry("400x300")

    notice_window.configure(bg="#EAF4FF")

    tk.Label(
        notice_window,
        text="Add New Notice",
        font=("Arial",16,"bold"),
        bg="#EAF4FF"
    ).pack(pady=15)

    tk.Label(notice_window, text="Notice Title", bg="#EAF4FF").pack()

    title_entry = tk.Entry(notice_window, width=35)
    title_entry.pack(pady=5)

    tk.Label(notice_window, text="Status", bg="#EAF4FF").pack()

    status_box = ttk.Combobox(
        notice_window,
        values=("Upcoming", "Ongoing", "Completed"),
        state="readonly",
        width=30
    )

    status_box.pack(pady=5)
    status_box.current(0)

    tk.Button(
        notice_window,
        text="Save Notice",
        bg="green",
        fg="white",
        command=lambda: save_notice(
            title_entry.get(),
            status_box.get()
        )
    ).pack(pady=20)

def save_notice(title, status):

    if title.strip() == "":
        messagebox.showerror("Error", "Enter Notice Title")
        return

    cursor.execute(
        "INSERT INTO notices(title, status) VALUES(?, ?)",
        (title, status)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Notice Added Successfully!"
    )    

def delete_notice():

    delete_window = tk.Toplevel(root)

    delete_window.title("Delete Notice")

    delete_window.geometry("450x400")

    delete_window.configure(bg="#EAF4FF")

    tk.Label(
        delete_window,
        text="Delete Notice",
        font=("Arial",18,"bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=10)

    listbox = tk.Listbox(delete_window, width=45, height=12)
    listbox.pack(pady=10)

    cursor.execute("SELECT id, title, status FROM notices")
    notices = cursor.fetchall()

    for notice in notices:
        listbox.insert(
            tk.END,
            f"{notice[0]} | {notice[1]} | {notice[2]}"
        )

    tk.Button(
        delete_window,
        text="Delete Selected",
        bg="red",
        fg="white",
        command=lambda: remove_notice(
            listbox,
            delete_window
        )
    ).pack(pady=10)
def remove_notice(listbox, window):

    selected = listbox.curselection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a notice."
        )
        return

    data = listbox.get(selected[0])

    notice_id = data.split("|")[0].strip()

    cursor.execute(
        "DELETE FROM notices WHERE id=?",
        (notice_id,)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Notice Deleted Successfully!"
    )

    window.destroy()

def add_event():

    event_window = tk.Toplevel(root)

    event_window.title("Add Event")

    event_window.geometry("400x350")

    event_window.configure(bg="#EAF4FF")

    tk.Label(
        event_window,
        text="Add New Event",
        font=("Arial",16,"bold"),
        bg="#EAF4FF"
    ).pack(pady=15)

    tk.Label(event_window, text="Event Title", bg="#EAF4FF").pack()

    title_entry = tk.Entry(event_window, width=35)
    title_entry.pack(pady=5)

    tk.Label(event_window, text="Event Date", bg="#EAF4FF").pack()

    date_entry = tk.Entry(event_window, width=35)
    date_entry.pack(pady=5)

    tk.Label(event_window, text="Status", bg="#EAF4FF").pack()

    status_box = ttk.Combobox(
        event_window,
        values=("Upcoming", "Ongoing", "Completed"),
        state="readonly",
        width=30
    )

    status_box.current(0)
    status_box.pack(pady=5)

    tk.Button(
        event_window,
        text="Save Event",
        bg="green",
        fg="white",
        command=lambda: save_event(
            title_entry.get(),
            date_entry.get(),
            status_box.get()
        )
    ).pack(pady=20)
def save_event(title, event_date, status):

    if title.strip() == "" or event_date.strip() == "":
        messagebox.showerror(
            "Error",
            "Please fill all fields."
        )
        return

    cursor.execute(
        "INSERT INTO events(title, event_date, status) VALUES(?,?,?)",
        (title, event_date, status)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Event Added Successfully!"
    )

def delete_event():

    delete_window = tk.Toplevel(root)

    delete_window.title("Delete Event")

    delete_window.geometry("500x400")

    delete_window.configure(bg="#EAF4FF")

    tk.Label(
        delete_window,
        text="Delete Event",
        font=("Arial",18,"bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=10)

    listbox = tk.Listbox(delete_window, width=55, height=12)
    listbox.pack(pady=10)

    cursor.execute("SELECT id, title, event_date, status FROM events")

    events = cursor.fetchall()

    for event in events:

        listbox.insert(
            tk.END,
            f"{event[0]} | {event[1]} | {event[2]} | {event[3]}"
        )

    tk.Button(
        delete_window,
        text="Delete Selected",
        bg="red",
        fg="white",
        command=lambda: remove_event(
            listbox,
            delete_window
        )
    ).pack(pady=10)

def remove_event(listbox, window):

    selected = listbox.curselection()

    if not selected:

        messagebox.showerror(
            "Error",
            "Please select an event."
        )

        return

    data = listbox.get(selected[0])

    event_id = data.split("|")[0].strip()

    cursor.execute(
        "DELETE FROM events WHERE id=?",
        (event_id,)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Event Deleted Successfully!"
    )

    window.destroy()
def ai_chatbot():

    chat_window = tk.Toplevel(root)

    chat_window.title("Campus AI Chatbot")

    chat_window.geometry("650x600")

    chat_window.configure(bg="#EAF4FF")

    tk.Label(
        chat_window,
        text="🤖 Campus AI Assistant",
        font=("Arial",18,"bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=10)

    chat_area = tk.Text(
        chat_window,
        width=70,
        height=22,
        font=("Arial",11),
        state="disabled",
        wrap="word"
    )

    chat_area.pack(pady=10)

    input_frame = tk.Frame(chat_window,bg="#EAF4FF")

    input_frame.pack(fill="x",padx=10,pady=10)

    message_entry = tk.Entry(
        input_frame,
        width=55,
        font=("Arial",11)
    )

    message_entry.pack(side="left",padx=5)

    tk.Button(
        input_frame,
        text="Send",
        bg="#0078D7",
        fg="white",
        command=lambda: send_message(
            message_entry,
            chat_area
        )
    ).pack(side="left",padx=5)

    tk.Button(
        chat_window,
        text="Clear Chat",
        bg="red",
        fg="white",
        command=lambda: clear_chat(chat_area)
    ).pack(pady=5)

def send_message(message_entry, chat_area):

    message = message_entry.get().strip()

    if message == "":
        return

    chat_area.config(state="normal")

    chat_area.insert(tk.END, "You: " + message + "\n")

    user_message = message.lower()

    if "hello" in user_message or "hi" in user_message:
        reply = "Hello! Welcome to Campus Companion."

    elif "cgpa" in user_message:
        reply = "CGPA means Cumulative Grade Point Average."

    elif "python" in user_message:
        reply = "Python is a high-level programming language."

    elif "dsa" in user_message:
        reply = "DSA stands for Data Structures and Algorithms."

    elif "attendance" in user_message:
        reply = "Attendance helps you track your class presence."

    elif "campus companion" in user_message:
        reply = "Campus Companion is a Smart Student Management System."

    else:
        reply = "Sorry! I don't know this yet. Later I'll answer using AI."

    chat_area.insert(tk.END, "AI: " + reply + "\n\n")

    chat_area.config(state="disabled")

    chat_area.see(tk.END)

    message_entry.delete(0, tk.END)
    message_entry.pack(side="left", padx=5)
    message_entry.bind(
        "<Return>",
        lambda event: send_message(
            message_entry,
            chat_area
        )
    )

def clear_chat(chat_area):

    chat_area.config(state="normal")

    chat_area.delete("1.0", tk.END)

    chat_area.config(state="disabled")    
    
def check_admin(username, password):

    cursor.execute("SELECT username, password FROM admin")
    print(cursor.fetchall())

    username = username.strip()
    password = password.strip()

    cursor.execute(
        "SELECT * FROM admin WHERE username=? AND password=?",
        (username, password)
    )

    admin = cursor.fetchone()

    if admin is not None:
        messagebox.showinfo("Success", "Admin Login Successful!")
        admin_panel()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")    
def dashboard():

    dashboard_window = tk.Toplevel(root)

    dashboard_window.title("Campus Companion Dashboard")

    dashboard_window.geometry("1000x650")

    dashboard_window.configure(bg="#EAF4FF")

    tk.Label(
        dashboard_window,
        text="Welcome to Campus Companion",
        font=("Arial", 22, "bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=20)
    button_frame = tk.Frame(
        dashboard_window,
        bg="#EAF4FF"
    )

    button_frame.pack(pady=30)
    routine_btn = tk.Button(
        button_frame,
        text="📅 Class Routine",
        width=22,
        height=2,
        command=class_routine
    )

    routine_btn.grid(row=0,column=0,padx=10,pady=10)
    attendance_btn = tk.Button(
        button_frame,
        text="📊 Attendance",
        width=22,
        height=2
    )

    attendance_btn.grid(row=0,column=1,padx=10,pady=10)
    cgpa_btn = tk.Button(
        button_frame,
        text="🎓 CGPA",
        width=22,
        height=2,
        command=cgpa_calculator
    )

    cgpa_btn.grid(row=1,column=0,padx=10,pady=10)
    notes_btn = tk.Button(
        button_frame,
        text="📝 Notes",
        width=22,
        height=2,
        command=view_notes
    )

    notes_btn.grid(row=1,column=1,padx=10,pady=10)
    todo_btn = tk.Button(
        button_frame,
        text="✅ To-Do List",
        width=22,
        height=2,
        command=todo_list
    )
    todo_btn.grid(row=2, column=0, padx=10, pady=10)

    notice_btn = tk.Button(
        button_frame,
        text="📢 Notice Board",
        width=22,
        height=2,
        command=notice_board
    )
    notice_btn.grid(row=2, column=1, padx=10, pady=10)

    events_btn = tk.Button(
        button_frame,
        text="🎉 Events",
        width=22,
        height=2,
        command=event_board
    )
    events_btn.grid(row=3, column=0, padx=10, pady=10)

    lost_btn = tk.Button(
        button_frame,
        text="🔍 Lost & Found",
        width=22,
        height=2,
        command=lost_found
    )
    lost_btn.grid(row=3, column=1, padx=10, pady=10)

    calendar_btn = tk.Button(
        button_frame,
        text="🗓 Academic Calendar",
        width=22,
        height=2,
        command=academic_calendar
    )
    calendar_btn.grid(row=4, column=0, padx=10, pady=10)

    chatbot_btn = tk.Button(
        button_frame,
        text="🤖 AI Chatbot",
        width=22,
        height=2,
        command=ai_chatbot
    )
    chatbot_btn.grid(row=4, column=1, padx=10, pady=10)
    tk.Button(
        button_frame,
        text="📚 Previous CGPA",
        width=22,
         height=2,
        command=show_previous_cgpa
    ).grid(row=5, column=0, padx=10, pady=10)

def class_routine():

    routine_window = tk.Toplevel(root)

    routine_window.title("Class Routine")

    routine_window.geometry("900x600")

    routine_window.configure(bg="#EAF4FF")

    tk.Label(
        routine_window,
        text="📅 CLASS ROUTINE",
        font=("Arial", 20, "bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=20)

    tk.Label(
        routine_window,
        text="Class Routine Module Connected Successfully!",
        font=("Arial", 13),
        bg="#EAF4FF"
    ).pack(pady=10)    
    
def todo_list():

    todo_window = tk.Toplevel(root)
    todo_window.title("To-Do List")
    todo_window.geometry("500x500")
    todo_window.configure(bg="#EAF4FF")

    tk.Label(
        todo_window,
        text="TO-DO LIST",
        font=("Arial",20,"bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=10)

    task_entry = tk.Entry(todo_window, width=30)
    task_entry.pack(pady=10)

    task_listbox = tk.Listbox(todo_window, width=40, height=12)
    task_listbox.pack(pady=10)

    # 🔥 Load existing tasks
    load_tasks(task_listbox)

    tk.Button(
        todo_window,
        text="Add Task",
        bg="green",
        fg="white",
        command=lambda: add_task(task_entry, task_listbox)
    ).pack(pady=5)

    tk.Button(
        todo_window,
        text="Delete Selected",
        bg="red",
        fg="white",
        command=lambda: delete_task(task_listbox)
    ).pack(pady=5)

def load_tasks(listbox):

    listbox.delete(0, tk.END)

    cursor.execute("SELECT task FROM todo")
    tasks = cursor.fetchall()

    for t in tasks:
        listbox.insert(tk.END, t[0])    

def add_task(entry, listbox):

    task = entry.get().strip()

    if task == "":
        messagebox.showerror("Error", "Task cannot be empty")
        return

    cursor.execute("INSERT INTO todo(task) VALUES(?)", (task,))
    conn.commit()

    entry.delete(0, tk.END)

    load_tasks(listbox)

def delete_task(listbox):

    selected = listbox.curselection()

    if not selected:
        messagebox.showerror("Error", "Select a task first")
        return

    task = listbox.get(selected)

    cursor.execute("DELETE FROM todo WHERE task=?", (task,))
    conn.commit()

    load_tasks(listbox)    
   
def notice_board():

    win = tk.Toplevel(root)
    win.title("Notice Board")
    win.geometry("400x400")

    listbox = tk.Listbox(win, width=50, height=20)
    listbox.pack(pady=10)

    cursor.execute("SELECT title, status FROM notices")
    data = cursor.fetchall()

    if not data:
        listbox.insert(tk.END, "No notices found")
        return

    for d in data:
        listbox.insert(tk.END, f"{d[0]} - {d[1]}")
    
def event_board():

    win = tk.Toplevel(root)
    win.title("Events")
    win.geometry("400x400")

    listbox = tk.Listbox(win, width=50, height=20)
    listbox.pack(pady=10)

    cursor.execute("SELECT title, event_date, status FROM events")
    data = cursor.fetchall()

    if not data:
        listbox.insert(tk.END, "No events found")
        return

    for d in data:
        listbox.insert(tk.END, f"{d[0]} | {d[1]} | {d[2]}")

def lost_found():

    lost_window = tk.Toplevel(root)

    lost_window.title("Lost & Found")

    lost_window.geometry("600x500")

    lost_window.configure(bg="#EAF4FF")

    tk.Label(
        lost_window,
        text="🔍 Lost & Found",
        font=("Arial",20,"bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=20)

    lost_text = """
📱 Black Redmi Mobile found near Library.

🎒 Blue Backpack found in Room 204.

🪪 Student ID Card found in CSE Department.

⌚ Black Wrist Watch found near Canteen.

📢 Contact the College Office to claim your item.
"""

    tk.Label(
        lost_window,
        text=lost_text,
        justify="left",
        font=("Arial",12),
        bg="#EAF4FF"
    ).pack(padx=20, pady=10)

def academic_calendar():

    calendar_window = tk.Toplevel(root)

    calendar_window.title("Academic Calendar")

    calendar_window.geometry("650x500")

    calendar_window.configure(bg="#EAF4FF")

    tk.Label(
        calendar_window,
        text="🗓 Academic Calendar",
        font=("Arial",20,"bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=20)

    calendar_data = [
        ("01 July", "Semester Classes Begin"),
        ("10 July", "Project Submission"),
        ("15 July", "Mid Semester Exam"),
        ("25 July", "Python Workshop"),
        ("05 August", "Sports Meet"),
        ("15 August", "Independence Day Celebration")
    ]

    frame = tk.Frame(calendar_window, bg="#EAF4FF")
    frame.pack(pady=10)

    tk.Label(frame, text="Date", width=20,
             font=("Arial",12,"bold"),
             bg="#B3D9FF").grid(row=0,column=0)

    tk.Label(frame, text="Event", width=35,
             font=("Arial",12,"bold"),
             bg="#B3D9FF").grid(row=0,column=1)

    for i, item in enumerate(calendar_data, start=1):

        tk.Label(frame,
                 text=item[0],
                 width=20,
                 relief="solid").grid(row=i,column=0)

        tk.Label(frame,
                 text=item[1],
                 width=35,
                 relief="solid").grid(row=i,column=1)
        
def cgpa_calculator():

    cgpa_window = tk.Toplevel(root)

    cgpa_window.title("CGPA Calculator")

    cgpa_window.geometry("500x400")

    cgpa_window.configure(bg="#EAF4FF")

    tk.Label(
        cgpa_window,
        text="🎓 CGPA Calculator",
        font=("Arial",20,"bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=20)

    tk.Label(
        cgpa_window,
        text="Select Your Branch",
        bg="#EAF4FF",
        font=("Arial",12)
    ).pack()

    branch_box = ttk.Combobox(
        cgpa_window,
        width=30,
        state="readonly"
    )

    branch_box["values"] = (
        "B.Tech CSE",
        "B.Tech CSE (AI & ML)",
        "B.Tech ECE",
        "B.Tech EE",
        "B.Tech ME",
        "BCA",
        "B.Sc Computer Science",
        "BBA",
        "B.Com",
        "MBA"
    )

    branch_box.pack(pady=10)

    tk.Label(
        cgpa_window,
        text="Select Semester",
        bg="#EAF4FF",
        font=("Arial",12)
    ).pack(pady=10)

    semester_box = ttk.Combobox(
        cgpa_window,
        width=30,
        state="readonly"
    )

    semester_box["values"] = (
        "Semester 1",
        "Semester 2",
        "Semester 3",
        "Semester 4",
        "Semester 5",
        "Semester 6",
        "Semester 7",
        "Semester 8"
    )

    semester_box.pack(pady=10)
    continue_btn = tk.Button(
        cgpa_window,
        text="Continue",
        width=18,
        command=lambda: open_marks_page(
            branch_box.get(),
            semester_box.get()
        )    
    )

    continue_btn.pack(pady=20)

def open_marks_page(branch, semester):

    marks_window = tk.Toplevel(root)
    marks_window.title("Enter Marks")
    marks_window.geometry("600x500")
    marks_window.configure(bg="#EAF4FF")

    tk.Label(
        marks_window,
        text=f"{branch} - {semester}",
        font=("Arial",16,"bold"),
        bg="#EAF4FF"
    ).pack(pady=10)

    tk.Label(
        marks_window,
        text="Enter marks out of 100",
        bg="#EAF4FF",
        fg="gray"
    ).pack(pady=5)

    subject_list = subjects[branch][semester]
    entries = []

    for subject in subject_list:

        frame = tk.Frame(marks_window, bg="#EAF4FF")
        frame.pack(pady=5)

        tk.Label(frame, text=subject, width=25, anchor="w", bg="#EAF4FF").pack(side="left")

        entry = tk.Entry(frame, width=10)
        entry.pack(side="left")

        tk.Label(frame, text="/100", bg="#EAF4FF").pack(side="left")

        entries.append(entry)

    tk.Button(
        marks_window,
        text="Calculate CGPA",
        bg="green",
        fg="white",
        width=15,
        command=lambda: calculate_cgpa(entries, branch, semester)
    ).pack(pady=20)    

def calculate_cgpa(entries, branch, semester):

    total_gp = 0
    count = len(entries)

    if count == 0:
        messagebox.showerror("Error", "No subjects found")
        return

    for entry in entries:

        value = entry.get().strip()

        if value == "":
            messagebox.showerror("Error", "Please enter all marks")
            return

        try:
            mark = float(value)
        except:
            messagebox.showerror("Error", "Only numbers allowed")
            return

        if mark >= 90:
            gp = 10
        elif mark >= 80:
            gp = 9
        elif mark >= 70:
            gp = 8
        elif mark >= 60:
            gp = 7
        elif mark >= 50:
            gp = 6
        elif mark >= 40:
            gp = 5
        else:
            gp = 0

        total_gp += gp

    cgpa = total_gp / count

    if cgpa >= 8:
        grade = "A+"
        performance = "Excellent ⭐⭐⭐⭐"
    elif cgpa >= 7:
        grade = "A"
        performance = "Very Good ⭐⭐⭐"
    elif cgpa >= 6:
        grade = "B+"
        performance = "Good ⭐⭐"
    else:
        grade = "B"
        performance = "Average ⭐"

    result = tk.Toplevel(root)
    result.title("Result")
    result.geometry("350x250")
    result.configure(bg="#EAF4FF")

    tk.Label(result, text=f"CGPA: {cgpa:.2f}", font=("Arial",14,"bold"), bg="#EAF4FF").pack(pady=10)
    tk.Label(result, text=f"Grade: {grade}", bg="#EAF4FF").pack()
    tk.Label(result, text=f"Performance: {performance}", bg="#EAF4FF").pack(pady=10)       
    tk.Button(
        result,
        text="Save Record",
        bg="blue",
        fg="white",
        width=15,
        command=lambda: save_record(branch, semester, cgpa, grade, performance)
    ).pack(pady=10)

def save_record(branch, semester, cgpa, grade, performance):

    cursor.execute("""
        INSERT INTO cgpa_records(branch, semester, cgpa, grade, performance)
        VALUES (?, ?, ?, ?, ?)
    """, (branch, semester, cgpa, grade, performance))

    conn.commit()

    messagebox.showinfo("Saved", "CGPA Saved Successfully!")

def show_previous_cgpa():

    history_window = tk.Toplevel(root)
    history_window.title("Previous CGPA")
    history_window.geometry("500x500")
    history_window.configure(bg="#EAF4FF")

    tk.Label(
        history_window,
        text="📚 Previous CGPA Records",
        font=("Arial",16,"bold"),
        bg="#EAF4FF"
    ).pack(pady=10)

    cursor.execute("SELECT branch, semester, cgpa, grade, performance FROM cgpa_records")
    records = cursor.fetchall()

    if not records:
        tk.Label(history_window, text="No records found", bg="#EAF4FF").pack()
        return

    for r in records:

        text = f"{r[0]} | {r[1]} \nCGPA: {r[2]:.2f} | Grade: {r[3]} | {r[4]}"

        tk.Label(
            history_window,
            text=text,
            bg="#EAF4FF",
            justify="left",
            anchor="w"
        ).pack(pady=5, fill="x")

def view_notes():

    notes_window = tk.Toplevel(root)

    notes_window.title("Study Notes")

    notes_window.geometry("500x500")

    notes_window.configure(bg="#EAF4FF")

    tk.Label(
        notes_window,
        text="📚 Study Notes",
        font=("Arial",18,"bold"),
        bg="#EAF4FF",
        fg="#003366"
    ).pack(pady=15)

    listbox = tk.Listbox(
        notes_window,
        width=55,
        height=18
    )

    listbox.pack(pady=10)

    cursor.execute(
        "SELECT subject, title FROM notes"
    )

    data = cursor.fetchall()

    if not data:

        listbox.insert(
            tk.END,
            "No Notes Available"
        )

    else:

        for note in data:

            listbox.insert(
                tk.END,
                f"{note[0]}  ➜  {note[1]}"
            )        

def upload_notes():

    filepath = filedialog.askopenfilename(

        filetypes=[
            ("PDF Files", "*.pdf"),
            ("Word Files", "*.docx"),
            ("All Files", "*.*")
        ]
    )

    if filepath == "":
        return

    upload_window = tk.Toplevel(root)

    upload_window.title("Upload Notes")

    upload_window.geometry("400x300")

    upload_window.configure(bg="#EAF4FF")

    tk.Label(
        upload_window,
        text="Upload Notes",
        font=("Arial",16,"bold"),
        bg="#EAF4FF"
    ).pack(pady=15)

    tk.Label(upload_window, text="Subject", bg="#EAF4FF").pack()

    subject_box = ttk.Combobox(
        upload_window,
        values=(
            "Mathematics-I",
            "Physics",
            "Programming in C",
            "English",
            "Workshop",
            "Basic Electronics"
        ),
        state="readonly",
        width=30
    )

    subject_box.pack(pady=5)

    tk.Label(upload_window, text="Notes Title", bg="#EAF4FF").pack()

    title_entry = tk.Entry(upload_window, width=35)

    title_entry.pack(pady=5)

    tk.Button(

        upload_window,

        text="Save",

        bg="green",

        fg="white",

        command=lambda: save_notes(

            subject_box.get(),

            title_entry.get(),

            filepath

        )

    ).pack(pady=20)

def save_notes(subject, title, filepath):

    if subject == "" or title.strip() == "":

        messagebox.showerror(
            "Error",
            "Fill all fields."
        )

        return

    cursor.execute(

        "INSERT INTO notes(subject,title,filepath) VALUES(?,?,?)",

        (subject, title, filepath)

    )

    conn.commit()

    messagebox.showinfo(

        "Success",

        "Notes Uploaded Successfully!"

    )    
    
def register():
    register_window = tk.Toplevel(root)

    register_window.title("Student Registration")
    register_window.geometry("500x500")
    register_window.configure(bg="#EAF4FF")

    # Heading
    heading = tk.Label(
        register_window,
        text="Student Registration",
        font=("Arial", 18, "bold"),
        bg="#EAF4FF",
        fg="#003366"
    )
    heading.pack(pady=15)

    # Name
    tk.Label(register_window, text="Full Name", bg="#EAF4FF").pack()
    name_entry = tk.Entry(register_window, width=35)
    name_entry.pack(pady=5)

    # Email
    tk.Label(register_window, text="Email", bg="#EAF4FF").pack()
    email_entry = tk.Entry(register_window, width=35)
    email_entry.pack(pady=5)

    # Phone
    tk.Label(register_window, text="Phone Number", bg="#EAF4FF").pack()
    phone_entry = tk.Entry(register_window, width=35)
    phone_entry.pack(pady=5)

    tk.Label(register_window, text="Department", bg="#EAF4FF").pack()
 
    department_entry = tk.Entry(register_window, width=35)

    department_entry.pack(pady=5)

    tk.Label(register_window, text="Semester", bg="#EAF4FF").pack()

    semester_entry = tk.Entry(register_window, width=35)

    semester_entry.pack(pady=5)

    tk.Label(register_window, text="Password", bg="#EAF4FF").pack()

    password_entry = tk.Entry(register_window, width=35, show="*")

    password_entry.pack(pady=5)

    tk.Label(register_window, text="Confirm Password", bg="#EAF4FF").pack()

    confirm_password_entry = tk.Entry(register_window, width=35, show="*")

    confirm_password_entry.pack(pady=5)

    register_button = tk.Button(
        register_window,
        text="Register",
        font=("Arial", 12, "bold"),
        bg="#28A745",
        fg="white",
        width=18,
        command=lambda: save_data(
            name_entry.get(),
            email_entry.get(),
            phone_entry.get(),
            department_entry.get(),
            semester_entry.get(),
            password_entry.get()
        )
)

    register_button.pack(pady=15)
def save_data(name, email, phone, department, semester, password):

    cursor.execute("""
    INSERT INTO students(name,email,phone,department,semester,password)
    VALUES(?,?,?,?,?,?)
    """,
    (name, email, phone, department, semester, password))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Registration Successful!"
    )

root = tk.Tk()

root.title("Campus Companion")

root.geometry("1000x650")
root.configure(bg="#EAF4FF")
title = tk.Label(
    root,
    text="CAMPUS COMPANION",
    font=("Arial", 24, "bold"),
    bg="#EAF4FF",
    fg="#003366"
)
title.pack()
subtitle = tk.Label(
    root,
    text="Smart Student Management System",
    font=("Arial", 12),
    bg="#EAF4FF",
    fg="gray"
)

subtitle.pack(pady=5)
login_btn = tk.Button(
    root,
    text="Login",
    font=("Arial", 14, "bold"),
    width=18,
    command=login
)

login_btn.pack(pady=20)
register_btn = tk.Button(
    root,
    text="Register",
    font=("Arial", 14, "bold"),
    width=18,
    command=register
)

register_btn.pack()
admin_btn = tk.Button(
    root,
    text="Admin Login",
    font=("Arial",14,"bold"),
    width=18,
    bg="#FF9800",
    fg="white",
    command=admin_login
)

admin_btn.pack(pady=15)

root.mainloop()

