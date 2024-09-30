import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# إعداد الاتصال بقاعدة البيانات
conn = mysql.connector.connect(
     host='localhost',
            user='root',
            password='',
            database='whatsapp_db',
    port=3306
)

cursor = conn.cursor()

# دالة لجلب الرسائل من قاعدة البيانات
def fetch_messages(search_term=""):
    query = "SELECT * FROM messages WHERE phone LIKE %s OR message LIKE %s OR sender LIKE %s ORDER BY send_date DESC"
    cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
    return cursor.fetchall()

# دالة لعرض الرسائل في الجدول
def display_messages(search_term=""):
    for row in message_table.get_children():
        message_table.delete(row)
    for row in fetch_messages(search_term):
        message_table.insert("", "end", values=row)

# دالة لحذف جميع الرسائل
def delete_all_messages():
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete all messages?")
    if confirm:
        cursor.execute("DELETE FROM messages")
        conn.commit()
        display_messages()
        messagebox.showinfo("Deleted", "All messages have been deleted.")

# دالة لحفظ الرسائل في ملف نصي
def save_messages_to_text():
    try:
        messages = fetch_messages()
        with open("messages.txt", "w", encoding="utf-8") as file:
            for message in messages:
                file.write(f"ID: {message[0]}, Phone: {message[1]}, Message: {message[2]}, Sender: {message[3]}, Date: {message[4]}\n")
        messagebox.showinfo("Success", "Messages have been saved to messages.txt")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# دالة لجلب الموظفين من قاعدة البيانات
def fetch_employees(search_term=""):
    query = """
    SELECT employees.id, employees.username, COUNT(messages.id) AS message_count
    FROM employees
    LEFT JOIN messages ON employees.username = messages.sender
    WHERE employees.username LIKE %s
    GROUP BY employees.id, employees.username
    """
    cursor.execute(query, ('%' + search_term + '%',))
    return cursor.fetchall()

# دالة لعرض الموظفين في الجدول
def display_employees(search_term=""):
    for row in employee_table.get_children():
        employee_table.delete(row)
    for row in fetch_employees(search_term):
        employee_table.insert("", "end", values=row)

# دالة لإضافة موظف جديد
def add_employee():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        try:
            cursor.execute("INSERT INTO employees (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            display_employees()
            messagebox.showinfo("Success", "Employee added successfully.")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
    else:
        messagebox.showwarning("Input Error", "Please enter both username and password.")

# دالة لحذف موظف
def delete_employee():
    selected_item = employee_table.selection()
    if selected_item:
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?")
        if confirm:
            employee_id = employee_table.item(selected_item)["values"][0]
            cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
            conn.commit()
            display_employees()
            messagebox.showinfo("Deleted", "Employee has been deleted.")
    else:
        messagebox.showwarning("Selection Error", "Please select an employee to delete.")

# دالة لتحديث البيانات في كل من الرسائل والموظفين
def update_data():
    display_messages(search_entry.get())
    display_employees(employee_search_entry.get())

# دالة لعرض نافذة منبثقة عند تمرير الماوس فوق عمود الرسالة
def on_hover(event):
    row_id = message_table.identify_row(event.y)
    column = message_table.identify_column(event.x)

    # التحقق مما إذا كنا على عمود الرسالة
    if column == "#3":  # العمود الثالث هو "Message"
        if row_id:
            # التأخير القصير قبل إظهار النافذة المنبثقة
            root.after(500, lambda: show_popup(event, row_id))

def show_popup(event, row_id):
    global popup_window
    if popup_window:  # أغلق النافذة المنبثقة إذا كانت مفتوحة
        popup_window.destroy()
    
    message = message_table.item(row_id, "values")[2]  # الرسالة هي القيمة الثالثة في السطر
    if len(message) > 50:  # إظهار النافذة فقط إذا كانت الرسالة طويلة
        popup_window = tk.Toplevel(root)
        popup_window.wm_overrideredirect(True)
        popup_window.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        label = tk.Label(popup_window, text=message, bg="white", wraplength=300)
        label.pack()
        popup_window.bind("<Leave>", lambda e: popup_window.destroy())

# متغير لتخزين نافذة منبثقة حالياً مفتوحة
popup_window = None

# إعداد واجهة المستخدم
root = tk.Tk()
root.title("Control Panel")

# جعل التطبيق يدعم وضع ملء الشاشة
root.state('zoomed')

# تغيير اللون العام للتطبيق
root.configure(bg="#f0f0f0")

# إنشاء تبويبات
tab_control = ttk.Notebook(root)

# تبويب الرسائل
messages_tab = ttk.Frame(tab_control)
tab_control.add(messages_tab, text="Messages")

# تبويب الموظفين
employees_tab = ttk.Frame(tab_control)
tab_control.add(employees_tab, text="Employees")

tab_control.pack(expand=1, fill="both")

# تكبير الأعمدة والصفوف لملء الشاشة
messages_tab.grid_rowconfigure(1, weight=1)
messages_tab.grid_columnconfigure(1, weight=1)

employees_tab.grid_rowconfigure(2, weight=1)
employees_tab.grid_columnconfigure(1, weight=1)

# === الرسائل ===

# حقل البحث
search_label = tk.Label(messages_tab, text="Search:", bg="white")
search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
search_entry = tk.Entry(messages_tab, bg="lightgray")
search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

search_button = tk.Button(messages_tab, text="Search", command=lambda: display_messages(search_entry.get()), bg="gray", fg="white")
search_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

# زر حذف جميع الرسائل
delete_button = tk.Button(messages_tab, text="Delete All Messages", command=delete_all_messages, bg="#ff4d4d", fg="white")
delete_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

# زر حفظ الرسائل في ملف نصي
save_button = tk.Button(messages_tab, text="Save to Text File", command=save_messages_to_text, bg="#d9d9d9")
save_button.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

# زر تحديث الصفحة
refresh_button = tk.Button(messages_tab, text="Refresh", command=update_data, bg="#d9d9d9")
refresh_button.grid(row=0, column=5, padx=10, pady=10, sticky="ew")

# إنشاء جدول لعرض الرسائل
message_columns = ("ID", "Phone", "Message", "Sender", "Date")
message_table = ttk.Treeview(messages_tab, columns=message_columns, show="headings")
for col in message_columns:
    message_table.heading(col, text=col)
    message_table.column(col, minwidth=0, width=120, stretch=tk.YES)
message_table.grid(row=1, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

# تلوين الأسطر في جدول الرسائل
message_table.tag_configure('evenrow', background='lightgray')
message_table.tag_configure('oddrow', background='#ffffff')

# إضافة تفاعل مع تمرير الماوس على الرسالة
message_table.bind("<Motion>", on_hover)

# عرض الرسائل عند بداية التشغيل
def update_message_table():
    for index, row in enumerate(fetch_messages()):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        message_table.insert("", "end", values=row, tags=(tag,))

update_message_table()

# === الموظفين ===

# حقل البحث
employee_search_label = tk.Label(employees_tab, text="Search:", bg="#f0f0f0")
employee_search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
employee_search_entry = tk.Entry(employees_tab, bg="lightgray")
employee_search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

employee_search_button = tk.Button(employees_tab, text="Search", command=lambda: display_employees(employee_search_entry.get()), bg="#d9d9d9")
employee_search_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

# حقل إضافة موظف جديد
username_label = tk.Label(employees_tab, text="Username:", bg="#f0f0f0")
username_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
username_entry = tk.Entry(employees_tab, bg="lightgray")
username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

password_label = tk.Label(employees_tab, text="Password:", bg="#f0f0f0")
password_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
password_entry = tk.Entry(employees_tab, show="*", bg="lightgray")
password_entry.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

add_employee_button = tk.Button(employees_tab, text="Add Employee", command=add_employee, bg="gray")
add_employee_button.grid(row=1, column=4, padx=10, pady=10, sticky="ew")

# زر حذف الموظف
delete_employee_button = tk.Button(employees_tab, text="Delete Employee", command=delete_employee, bg="#ff4d4d", fg="white")
delete_employee_button.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

# زر تحديث الصفحة
refresh_employee_button = tk.Button(employees_tab, text="Refresh", command=update_data, bg="#d9d9d9")
refresh_employee_button.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

# إنشاء جدول لعرض الموظفين
employee_columns = ("ID", "Username", "Messages Sent")
employee_table = ttk.Treeview(employees_tab, columns=employee_columns, show="headings")
for col in employee_columns:
    employee_table.heading(col, text=col)
    employee_table.column(col, minwidth=0, width=120, stretch=tk.YES)
employee_table.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

# تلوين الأسطر في جدول الموظفين
employee_table.tag_configure('evenrow', background='lightgray')
employee_table.tag_configure('oddrow', background='#ffffff')

# عرض الموظفين عند بداية التشغيل
def update_employee_table():
    for index, row in enumerate(fetch_employees()):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        employee_table.insert("", "end", values=row, tags=(tag,))

update_employee_table()

# تشغيل التطبيق
root.mainloop()

# إغلاق الاتصال بقاعدة البيانات عند إغلاق التطبيق
conn.close()
