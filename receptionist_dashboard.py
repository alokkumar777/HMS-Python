import tkinter as tk
from tkinter import ttk
import sqlite3
from appointment_management import AppointmentManagement
from patient_management import PatientManagement

class ReceptionistDashboard:
    def __init__(self, root, back_to_dashboard):
        self.root = root
        self.back_to_dashboard = back_to_dashboard
        self.root.title("Receptionist Dashboard")
        self.root.geometry("800x600")

        # Title Label
        label_title = tk.Label(root, text="Receptionist Dashboard", font=("Arial", 20, "bold"))
        label_title.pack(pady=10)

        # Buttons
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Manage Appointments", command=self.manage_appointments).grid(row=0, column=0, padx=5)
        tk.Button(frame_buttons, text="Manage Patients", command=self.manage_patients).grid(row=0, column=1, padx=5)
        tk.Button(frame_buttons, text="Back to Login", command=self.logout).grid(row=0, column=2, padx=5)

    def manage_appointments(self):
        """Open Appointment Management Interface."""
        self.root.destroy()  # Close the admin dashboard
        root = tk.Tk()
        app = AppointmentManagement(root, self.open_dashboard)
        root.mainloop()

    def manage_patients(self):
        """Open Patient Management Interface."""
        self.root.destroy()  # Close the admin dashboard
        root = tk.Tk()
        app = PatientManagement(root, self.open_dashboard)
        root.mainloop()

    def open_dashboard(self):
        """Reopen the admin dashboard."""
        root = tk.Tk()
        app = ReceptionistDashboard(root, self.back_to_dashboard)
        root.mainloop()

    # def go_back_to_dashboard(self):
    #     """Return to the login screen."""
    #     self.root.destroy()
    #     self.back_to_dashboard()

    def logout(self):
        """Logout and return to Login Window."""
        self.root.destroy()
        from login import main  # Import and run the login script
        main()

def main():
    root = tk.Tk()
    app = ReceptionistDashboard(root, lambda: None)
    root.mainloop()

if __name__ == "__main__":
    main()