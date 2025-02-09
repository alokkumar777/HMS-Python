import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from tkinter import simpledialog

class AppointmentManagement:
    def __init__(self, root, back_to_dashboard):
        self.root = root
        self.back_to_dashboard = back_to_dashboard
        self.root.title("Appointment Management")
        self.root.geometry("1300x650")
        self.root.option_add("*Font", "Verdana 10")

        # Title Label
        label_title = ttk.Label(root, text="Appointment Management", font=("Verdana", 20, "bold"))
        label_title.pack(pady=10)

        # Input Fields
        frame_input = tk.Frame(root)
        frame_input.pack(pady=10)

        # Patient Dropdown
        ttk.Label(frame_input, text="Patient:").grid(row=0, column=0, padx=5, pady=5)
        self.patient_var = tk.StringVar()
        self.patient_dropdown = ttk.Combobox(frame_input, textvariable=self.patient_var, width=30)
        self.patient_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.load_patients()

        # Doctor Dropdown
        ttk.Label(frame_input, text="Doctor:").grid(row=1, column=0, padx=5, pady=5)
        self.doctor_var = tk.StringVar()
        self.doctor_dropdown = ttk.Combobox(frame_input, textvariable=self.doctor_var, width=30)
        self.doctor_dropdown.grid(row=1, column=1, padx=5, pady=5)
        self.load_doctors()

        # Date and Time
        ttk.Label(frame_input, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.entry_date = ttk.Entry(frame_input, width=30)
        self.entry_date.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Time (HH:MM:SS):").grid(row=3, column=0, padx=5, pady=5)
        self.entry_time = ttk.Entry(frame_input, width=30)
        self.entry_time.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        style = ttk.Style()
        # Configure the font size for the button
        style.configure("Custom.TButton", font=("Verdana", 10))
        style.configure("Custom.Treeview", font=("Verdana", 10))
        style.configure("Custom.Treeview.Heading", font=("Verdana", 10, "bold"))
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        ttk.Button(frame_buttons, text="Schedule Appointment", command=self.schedule_appointment, padding=10, style="Custom.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(frame_buttons, text="Update Appointment", command=self.update_appointment, padding=10, style="Custom.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(frame_buttons, text="Cancel Appointment", command=self.cancel_appointment, padding=10, style="Custom.TButton").grid(row=0, column=2, padx=5)
        ttk.Button(frame_buttons, text="View All Appointments", command=self.view_appointments, padding=10, style="Custom.TButton").grid(row=0, column=3, padx=5)
        ttk.Button(frame_buttons, text="Back to Dashboard", command=self.go_back_to_dashboard, padding=10, style="Custom.TButton").grid(row=1, column=0, columnspan=4, pady=10)


        # Appointment List (Treeview)
        frame_list = tk.Frame(root)
        frame_list.pack(pady=10)

        self.tree = ttk.Treeview(frame_list, columns=("ID", "Patient", "Doctor", "Date", "Time", "Status"), show="headings", style="Custom.Treeview", padding=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Patient", text="Patient")
        self.tree.heading("Doctor", text="Doctor")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Status", text="Status")
        self.tree.pack()

        # Load initial data
        self.view_appointments()

    def go_back_to_dashboard(self):
        """Return to the admin dashboard."""
        self.root.destroy()  # Close the current window
        self.back_to_dashboard()  # Open the admin dashboard

    def load_patients(self):
        """Load patients into the dropdown."""
        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT patient_id, name FROM Patients')
        patients = cursor.fetchall()
        conn.close()
        self.patient_dropdown['values'] = [f"{patient[0]} - {patient[1]}" for patient in patients]

    def load_doctors(self):
        """Load doctors into the dropdown."""
        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT doctor_id, name FROM Doctors')
        doctors = cursor.fetchall()
        conn.close()
        self.doctor_dropdown['values'] = [f"{doctor[0]} - {doctor[1]}" for doctor in doctors]

    def schedule_appointment(self):
        """Schedule a new appointment."""
        patient = self.patient_var.get()
        doctor = self.doctor_var.get()
        date = self.entry_date.get()
        time = self.entry_time.get()

        if not patient or not doctor or not date or not time:
            messagebox.showerror("Error", "All fields are required!")
            return

        patient_id = patient.split(" - ")[0]
        doctor_id = doctor.split(" - ")[0]

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Appointments (patient_id, doctor_id, date, time, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_id, doctor_id, date, time, "Scheduled"))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Appointment scheduled successfully!")
        self.clear_entries()
        self.view_appointments()

    def update_appointment(self):
        """Update appointment details."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an appointment to update!")
            return

        appointment_id = self.tree.item(selected_item, "values")[0]
        patient = self.patient_var.get()
        doctor = self.doctor_var.get()
        date = self.entry_date.get()
        time = self.entry_time.get()

        if not patient or not doctor or not date or not time:
            messagebox.showerror("Error", "All fields are required!")
            return

        patient_id = patient.split(" - ")[0]
        doctor_id = doctor.split(" - ")[0]

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Appointments
            SET patient_id = ?, doctor_id = ?, date = ?, time = ?
            WHERE appointment_id = ?
        ''', (patient_id, doctor_id, date, time, appointment_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Appointment updated successfully!")
        self.clear_entries()
        self.view_appointments()

    def cancel_appointment(self):
        """Cancel an appointment."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an appointment to cancel!")
            return

        appointment_id = self.tree.item(selected_item, "values")[0]

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Appointments
            SET status = ?
            WHERE appointment_id = ?
        ''', ("Cancelled", appointment_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Appointment cancelled successfully!")
        self.view_appointments()

    def view_appointments(self):
        """View all appointments in the database."""
        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.appointment_id, p.name, d.name, a.date, a.time, a.status
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            JOIN Doctors d ON a.doctor_id = d.doctor_id
        ''')
        rows = cursor.fetchall()
        conn.close()

        # Clear existing data in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new data
        for row in rows:
            self.tree.insert("", "end", values=row)

    def clear_entries(self):
        """Clear all input fields."""
        self.patient_var.set("")
        self.doctor_var.set("")
        self.entry_date.delete(0, tk.END)
        self.entry_time.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = AppointmentManagement(root, lambda: None)
    root.mainloop()

if __name__ == "__main__":
    main()
