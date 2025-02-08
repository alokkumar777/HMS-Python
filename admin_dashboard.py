import tkinter as tk
from tkinter import messagebox, ttk
from patient_management import PatientManagement
from doctor_management import DoctorManagement
from medical_records import MedicalRecordsManagement
from appointment_management import AppointmentManagement
from billing_reports import BillingReports

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System - Admin Dashboard")
        self.root.geometry("800x500")

        # Title Label
        label_title = tk.Label(root, text="Admin Dashboard", font=("Verdana", 20, "bold"))
        label_title.pack(pady=20)

        # Buttons for Functionalities
        # Create a style object
        style = ttk.Style()

        # Configure the font size for the button
        style.configure("Custom.TButton", font=("Verdana", 10))  # Set the font and size
        button_patients = ttk.Button(root, text="Manage Patients", command=self.manage_patients, width=20, padding=10, style="Custom.TButton")
        button_patients.pack(pady=10)

        button_doctors = ttk.Button(root, text="Manage Doctors", command=self.manage_doctors, width=20, padding=10, style="Custom.TButton")
        button_doctors.pack(pady=10)

        button_appointments = ttk.Button(root, text="Manage Appointments", command=self.manage_appointments, width=20, padding=10, style="Custom.TButton")
        button_appointments.pack(pady=10)

        button_medical_records = ttk.Button(root, text="Manage Medical Records", command=self.manage_medical_records, width=20, padding=10, style="Custom.TButton")
        button_medical_records.pack(pady=10)

        button_reports = ttk.Button(root, text="View Reports", command=self.view_reports, width=20, padding=10, style="Custom.TButton")
        button_reports.pack(pady=10)

        button_logout = ttk.Button(root, text="Logout", command=self.logout, width=20, padding=10, style="Custom.TButton")
        button_logout.pack(pady=10)

    def manage_patients(self):
        """Open Patient Management Interface."""
        self.root.destroy()  # Close the admin dashboard
        root = tk.Tk()
        app = PatientManagement(root, self.open_dashboard)
        root.mainloop()
        # Placeholder for patient management functionality

    def manage_doctors(self):
        """Open Doctor Management Interface."""
        self.root.destroy()  # Close the admin dashboard
        root = tk.Tk()
        app = DoctorManagement(root, self.open_dashboard)
        root.mainloop()
        # Placeholder for doctor management functionality

    def manage_appointments(self):
        """Open Appointment Management Interface."""
        self.root.destroy()  # Close the admin dashboard
        root = tk.Tk()
        app = AppointmentManagement(root, self.open_dashboard)
        root.mainloop()
        # Placeholder for appointment management functionality

    def manage_medical_records(self):
        """Open Medical Records Management Interface."""
        self.root.destroy()  # Close the admin dashboard
        root = tk.Tk()
        app = MedicalRecordsManagement(root, self.open_dashboard)
        root.mainloop()

    def view_reports(self):
        """Open Reports Interface."""
        self.root.destroy()  # Close the admin dashboard
        root = tk.Tk()
        app = BillingReports(root, self.open_dashboard)
        root.mainloop()
        # Placeholder for reports functionality

    def open_dashboard(self):
        """Reopen the admin dashboard."""
        root = tk.Tk()
        app = AdminDashboard(root)
        root.mainloop()

    def logout(self):
        """Logout and return to Login Window."""
        self.root.destroy()
        from login import main  # Import and run the login script
        main()

def main():
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()

