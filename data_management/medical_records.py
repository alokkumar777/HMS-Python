import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class MedicalRecordsManagement:
    def __init__(self, root, back_to_dashboard):
        self.root = root
        self.back_to_dashboard = back_to_dashboard
        self.root.title("Medical Records Management")
        self.root.geometry("1300x650")
        self.root.option_add("*Font", "Verdana 10")

        # Title Label
        label_title = ttk.Label(root, text="Medical Records Management", font=("Verdana", 20, "bold"))
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

        # Diagnosis and Prescription
        ttk.Label(frame_input, text="Diagnosis:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_diagnosis = ttk.Entry(frame_input, width=32)
        self.entry_diagnosis.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Prescription:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_prescription = ttk.Entry(frame_input, width=32)
        self.entry_prescription.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5)
        self.entry_date = ttk.Entry(frame_input, width=32)
        self.entry_date.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        style = ttk.Style()
        # Configure the font size for the button
        style.configure("Custom.TButton", font=("Verdana", 10))
        style.configure("Custom.Treeview", font=("Verdana", 10))
        style.configure("Custom.Treeview.Heading", font=("Verdana", 10, "bold"))
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        ttk.Button(frame_buttons, text="Add Record", command=self.add_record, padding=10, style="Custom.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(frame_buttons, text="Update Record", command=self.update_record, padding=10, style="Custom.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(frame_buttons, text="Delete Record", command=self.delete_record, padding=10, style="Custom.TButton").grid(row=0, column=2, padx=5)
        ttk.Button(frame_buttons, text="View All Records", command=self.view_records, padding=10, style="Custom.TButton").grid(row=0, column=3, padx=5)
        ttk.Button(frame_buttons, text="Back to Dashboard", command=self.go_back_to_dashboard, padding=10, style="Custom.TButton").grid(row=1, column=0, columnspan=4, pady=10)


        # Medical Records List (Treeview)
        
        frame_list = tk.Frame(root)
        frame_list.pack(pady=10)

        self.tree = ttk.Treeview(frame_list, columns=("ID", "Patient", "Doctor", "Diagnosis", "Prescription", "Date"), show="headings", style="Custom.Treeview", padding=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Patient", text="Patient")
        self.tree.heading("Doctor", text="Doctor")
        self.tree.heading("Diagnosis", text="Diagnosis")
        self.tree.heading("Prescription", text="Prescription")
        self.tree.heading("Date", text="Date")
        self.tree.pack()

        # Load initial data
        self.view_records()

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

    def add_record(self):
        """Add a new medical record."""
        patient = self.patient_var.get()
        doctor = self.doctor_var.get()
        diagnosis = self.entry_diagnosis.get()
        prescription = self.entry_prescription.get()
        date = self.entry_date.get()

        if not patient or not doctor or not diagnosis or not prescription or not date:
            messagebox.showerror("Error", "All fields are required!")
            return

        patient_id = patient.split(" - ")[0]
        doctor_id = doctor.split(" - ")[0]

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO MedicalRecords (patient_id, doctor_id, diagnosis, prescription, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_id, doctor_id, diagnosis, prescription, date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Medical record added successfully!")
        self.clear_entries()
        self.view_records()

    def update_record(self):
        """Update an existing medical record."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to update!")
            return

        record_id = self.tree.item(selected_item, "values")[0]
        patient = self.patient_var.get()
        doctor = self.doctor_var.get()
        diagnosis = self.entry_diagnosis.get()
        prescription = self.entry_prescription.get()
        date = self.entry_date.get()

        if not patient or not doctor or not diagnosis or not prescription or not date:
            messagebox.showerror("Error", "All fields are required!")
            return

        patient_id = patient.split(" - ")[0]
        doctor_id = doctor.split(" - ")[0]

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE MedicalRecords
            SET patient_id = ?, doctor_id = ?, diagnosis = ?, prescription = ?, date = ?
            WHERE record_id = ?
        ''', (patient_id, doctor_id, diagnosis, prescription, date, record_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Medical record updated successfully!")
        self.clear_entries()
        self.view_records()

    def delete_record(self):
        """Delete a medical record."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete!")
            return

        record_id = self.tree.item(selected_item, "values")[0]

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM MedicalRecords WHERE record_id = ?', (record_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Medical record deleted successfully!")
        self.view_records()

    def view_records(self):
        """View all medical records in the database."""
        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.record_id, p.name, d.name, m.diagnosis, m.prescription, m.date
            FROM MedicalRecords m
            JOIN Patients p ON m.patient_id = p.patient_id
            JOIN Doctors d ON m.doctor_id = d.doctor_id
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
        self.entry_diagnosis.delete(0, tk.END)
        self.entry_prescription.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = MedicalRecordsManagement(root, lambda:None)
    root.mainloop()

if __name__ == "__main__":
    main()
    