import pywhatkit as kit
import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='whatsapp_db',
            port=3306
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

def validate_login(username, password):
    conn = connect_db()
    if conn is None:
        return False

    cursor = conn.cursor()
    cursor.execute("SELECT password FROM employees WHERE username=%s", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return password == result[0]
    return False

def send_messages(phone_entry, message_entry):
    conn = connect_db()
    if conn is None:
        return

    username = logged_in_user
    phone_numbers = phone_entry.get("1.0", tk.END).strip().split('\n')
    message = message_entry.get("1.0", tk.END).strip()
    cursor = conn.cursor()

    for phone in phone_numbers:
        phone = phone.strip()
        if phone and message:
            try:
                kit.sendwhatmsg_instantly(phone, message, 15, True, 5)
                cursor.execute(
                    "INSERT INTO messages (phone, message, sender, send_date) VALUES (%s, %s, %s, NOW())",
                    (phone, message, username)
                )
                conn.commit()
            except Exception as e:
                print(f"Error sending message: {e}")
                messagebox.showerror("Error", f"Failed to send message to {phone}")

    conn.close()

def check_login():
    global logged_in_user
    username = username_entry.get()
    password = password_entry.get()
    if validate_login(username, password):
        logged_in_user = username
        login_frame.pack_forget()
        show_message_screen()
    else:
        messagebox.showerror("Login Error", "Invalid username or password")

def create_popup_menu(widget):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Cut", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))

    def show_popup(event):
        menu.post(event.x_root, event.y_root)

    widget.bind("<Button-3>", show_popup)

def show_login_screen():
    global username_entry, password_entry, login_frame
    login_frame = tk.Frame(root, bg='white')
    login_frame.place(relwidth=1, relheight=1)

    tk.Label(login_frame, text="Username", bg='white', fg='red', font=('Helvetica', 14, 'bold')).pack(pady=10)
    username_entry = tk.Entry(login_frame, bg='lightgray', font=('Helvetica', 14), width=30)
    username_entry.pack(pady=10)

    tk.Label(login_frame, text="Password", bg='white', fg='red', font=('Helvetica', 14, 'bold')).pack(pady=10)
    password_entry = tk.Entry(login_frame, show="*", bg='lightgray', font=('Helvetica', 14), width=30)
    password_entry.pack(pady=10)

    login_button = tk.Button(login_frame, text="Login", bg='red', fg='white', font=('Helvetica', 14, 'bold'), command=check_login)
    login_button.pack(pady=20)

    tk.Label(login_frame, text="© All Rights Reserved For (khaled32r) 2024", bg='white', fg='grey', font=('Helvetica', 10)).pack(pady=10)

def show_message_screen():
    global phone_entries, message_entries
    message_frame = tk.Frame(root, bg='white')
    message_frame.place(relwidth=1, relheight=1)

    phone_entries = []
    message_entries = []

    def create_message_widget(row, col):
        tk.Label(message_frame, text=f"Message {row + 1}", bg='white', fg='red', font=('Helvetica', 14, 'bold')).grid(row=0, column=col, padx=10, pady=10)
        message_entry = scrolledtext.ScrolledText(message_frame, height=5, width=30, bg='lightgray', font=('Helvetica', 12), wrap=tk.WORD)
        message_entry.grid(row=1, column=col, padx=10, pady=10)
        create_popup_menu(message_entry)
        message_entries.append(message_entry)

    def create_phone_widget(row, col):
        tk.Label(message_frame, text=f"Phone Numbers {row + 1} (one per line)", bg='white', fg='red', font=('Helvetica', 14, 'bold')).grid(row=2, column=col, padx=10, pady=10)
        phone_entry = scrolledtext.ScrolledText(message_frame, height=24, width=30, bg='lightgray', font=('Helvetica', 12), wrap=tk.WORD)
        phone_entry.grid(row=3, column=col, padx=10, pady=10)
        create_popup_menu(phone_entry)
        phone_entries.append(phone_entry)
        send_button = tk.Button(message_frame, text="Send Messages", bg='red', fg='white', font=('Helvetica', 14, 'bold'), command=lambda: send_messages(phone_entry, message_entries[row]))
        send_button.grid(row=4, column=col, padx=10, pady=20)

    for i in range(5):
        create_message_widget(i, i)
        create_phone_widget(i, i)

    tk.Label(message_frame, text="© All Rights Reserved For (khaledalahmad32r) 2024", bg='white', fg='grey', font=('Helvetica', 10)).grid(row=5, columnspan=5, pady=10)
    tk.Label(message_frame, text="Created by khaled alahmad", bg='white', fg='grey', font=('Helvetica', 10)).grid(row=6, columnspan=5, pady=5)

root = tk.Tk()
root.title("WhatsApp Messaging App")
root.geometry("1500x900")

logged_in_user = None

show_login_screen()

root.mainloop()
