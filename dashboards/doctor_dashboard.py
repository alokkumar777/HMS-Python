import tkinter as tk
from tkinter import ttk
import sqlite3
from data_management.medical_records import MedicalRecordsManagement

class DoctorDashboard:
    def __init__(self, root, back_to_dashboard):
        self.root = root
        self.back_to_dashboard = back_to_dashboard
        # self.doctor_id = doctor_id  # Store the logged-in doctor's ID
        self.root.title("Doctor Dashboard")
        self.root.geometry("1300x600")

        # Title Label
        label_title = tk.Label(root, text="Doctor Dashboard", font=("Verdana", 20, "bold"))
        label_title.pack(pady=10)

        # Buttons
        style = ttk.Style()
        # Configure the font size for the button
        style.configure("Custom.TButton", font=("Verdana", 10))
        style.configure("Custom.Treeview", font=("Verdana", 10))
        style.configure("Custom.Treeview.Heading", font=("Verdana", 10, "bold"))
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        ttk.Button(frame_buttons, text="View Appointments", command=self.view_appointments, padding=10, style="Custom.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(frame_buttons, text="View Patient Records", command=self.view_medical_records, padding=10, style="Custom.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(frame_buttons, text="LOGOUT", command=self.logout, padding=10, style="Custom.TButton").grid(row=0, column=2, padx=5)

        # Appointments List (Treeview)
        self.tree = ttk.Treeview(root, columns=("ID", "Patient", "Date", "Time", "Status"), show="headings", style="Custom.Treeview", padding=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Patient", text="Patient")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Status", text="Status")
        self.tree.pack(pady=10)

    def view_appointments(self):
        """View all appointments for the doctor."""
        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.appointment_id, p.name, a.date, a.time, a.status
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            WHERE a.doctor_id = ?  -- Replace with the logged-in doctor's ID
        ''', (19,))  # Replace 1 with the logged-in doctor's ID
        rows = cursor.fetchall()
        conn.close()

        # Clear existing data in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new data
        for row in rows:
            self.tree.insert("", "end", values=row)

    def view_medical_records(self):
        """View patient records for the doctor."""
        self.root.destroy()  # Close the admin dashboard
        root = tk.Tk()
        app = MedicalRecordsManagement(root, self.open_dashboard)
        root.mainloop()

    def open_dashboard(self):
        """Reopen the admin dashboard."""
        root = tk.Tk()
        app = DoctorDashboard(root, self.back_to_dashboard)
        root.mainloop()
    # def go_back_to_dashboard(self):
    #     """Return to the login screen."""
    #     self.root.destroy()
    #     self.back_to_dashboard()

    def logout(self):
        """Logout and return to Login Window."""
        self.root.destroy()
        from start import main  # Import and run the login script
        main()

def main():
    root = tk.Tk()
    app = DoctorDashboard(root, lambda: None)
    root.mainloop()

if __name__ == "__main__":
    main()