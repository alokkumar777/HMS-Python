import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from admin_dashboard import AdminDashboard  # Import the AdminDashboard class
from doctor_dashboard import DoctorDashboard
from receptionist_dashboard import ReceptionistDashboard

def validate_login(username, password, role):
    """Validate user credentials."""
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ? AND role = ?', (username, password, role))
    user = cursor.fetchone()
    conn.close()
    return user

def login():
    username = entry_username.get()
    password = entry_password.get()
    role = role_var.get()

    if not username or not password or not role:
        messagebox.showerror("Error", "All fields are required!")
        return

    user = validate_login(username, password, role)
    if user:
        messagebox.showinfo("Login Successful", f"Welcome {user[1]}!")
        root.destroy()  # Close the login window
        open_dashboard(role)  # Open the dashboard based on role
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

def open_dashboard(role):
    """Open the dashboard based on user role."""
    root = tk.Tk()
    if role == "Admin":
        app = AdminDashboard(root, lambda: main())  # Pass the main function as a callback
    elif role == "Doctor":
        app = DoctorDashboard(root, lambda: main())  # Pass the main function as a callback
    elif role == "Receptionist":
        app = ReceptionistDashboard(root, lambda: main())  # Pass the main function as a callback
    root.mainloop()

def main():
    """Main function to start the application."""
    # Main GUI
    global root 
    root = tk.Tk()
    root.title("Hospital Management System - Login")
    root.geometry("600x360")
    root.option_add("*Font", "Verdana 10")

    label_title = tk.Label(root, text="Login", font=("Verdana", 20, "bold"))
    label_title.pack(pady=20)

    label_username = tk.Label(root, text="Username:")
    label_username.pack(pady=10)
    global entry_username 
    entry_username = ttk.Entry(root, width=30)
    entry_username.pack()

    label_password = tk.Label(root, text="Password:")
    label_password.pack(pady=10)
    global entry_password 
    entry_password = ttk.Entry(root, show="*", width=30)
    entry_password.pack()

    # Add a label
    ttk.Label(root, text="Role:").pack(pady=10)
    # Create a frame to hold the radio buttons
    role_frame = tk.Frame(root)
    role_frame.pack(pady=10)

    # Create a style for ttk.Radiobutton
    style = ttk.Style()
    style.configure("Custom.TRadiobutton", font=("Verdana", 10))

    # Add radio buttons to the frame
    global role_var 
    role_var = tk.StringVar(value="Admin")  # Default role
    ttk.Radiobutton(role_frame, text="Admin", variable=role_var, value="Admin", style="Custom.TRadiobutton").pack(side=tk.LEFT, padx=10)
    ttk.Radiobutton(role_frame, text="Doctor", variable=role_var, value="Doctor", style="Custom.TRadiobutton").pack(side=tk.LEFT, padx=10)
    ttk.Radiobutton(role_frame, text="Receptionist", variable=role_var, value="Receptionist", style="Custom.TRadiobutton").pack(side=tk.LEFT, padx=10)


    style = ttk.Style()
    style.configure("Custom.TButton", font=("Verdana", 10))
    button_login = ttk.Button(root, text="Login", command=login, width=20, padding=5, style="Custom.TButton")
    button_login.pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    main()

