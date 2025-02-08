import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class PatientManagement:
    def __init__(self, root, back_to_dashboard):
        self.root = root
        self.back_to_dashboard = back_to_dashboard
        self.root.title("Patient Management")
        self.root.geometry("1300x630")

        # Title Label
        label_title = tk.Label(root, text="Patient Management", font=("Arial", 20, "bold"))
        label_title.pack(pady=10)

        # Input Fields
        frame_input = tk.Frame(root)
        frame_input.pack(pady=10)

        ttk.Label(frame_input, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ttk.Entry(frame_input, width=30)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_age = ttk.Entry(frame_input, width=30)
        self.entry_age.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Gender:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_gender = ttk.Entry(frame_input, width=30)
        self.entry_gender.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Contact Number:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_contact = ttk.Entry(frame_input, width=30)
        self.entry_contact.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Address:").grid(row=4, column=0, padx=5, pady=5)
        self.entry_address = ttk.Entry(frame_input, width=30)
        self.entry_address.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        ttk.Button(frame_buttons, text="Add Patient", command=self.add_patient, padding=10).grid(row=0, column=0, padx=5)
        ttk.Button(frame_buttons, text="Update Patient", command=self.update_patient, padding=10).grid(row=0, column=1, padx=5)
        ttk.Button(frame_buttons, text="Delete Patient", command=self.delete_patient, padding=10).grid(row=0, column=2, padx=5)
        ttk.Button(frame_buttons, text="View All Patients", command=self.view_patients, padding=10).grid(row=0, column=3, padx=5)
        ttk.Button(frame_buttons, text="Back to Dashboard", command=self.go_back_to_dashboard, padding=10).grid(row=1, column=0, columnspan=4, pady=10)

        # Patient List (Treeview)
        frame_list = tk.Frame(root)
        frame_list.pack(pady=10)

        self.tree = ttk.Treeview(frame_list, columns=("ID", "Name", "Age", "Gender", "Contact", "Address"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("Address", text="Address")
        self.tree.pack()

        # Load initial data
        self.view_patients()
    
    def go_back_to_dashboard(self):
        """Return to the admin dashboard."""
        self.root.destroy()  # Close the current window
        self.back_to_dashboard()  # Open the admin dashboard

    def add_patient(self):
        """Add a new patient to the database."""
        name = self.entry_name.get()
        age = self.entry_age.get()
        gender = self.entry_gender.get()
        contact = self.entry_contact.get()
        address = self.entry_address.get()

        if not name or not age or not gender or not contact or not address:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Patients (name, age, gender, contact_number, address, date_of_registration)
            VALUES (?, ?, ?, ?, ?, DATE('now'))
        ''', (name, age, gender, contact, address))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Patient added successfully!")
        self.clear_entries()
        self.view_patients()

    def update_patient(self):
        """Update patient details."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to update!")
            return

        patient_id = self.tree.item(selected_item, "values")[0]
        name = self.entry_name.get()
        age = self.entry_age.get()
        gender = self.entry_gender.get()
        contact = self.entry_contact.get()
        address = self.entry_address.get()

        if not name or not age or not gender or not contact or not address:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Patients
            SET name = ?, age = ?, gender = ?, contact_number = ?, address = ?
            WHERE patient_id = ?
        ''', (name, age, gender, contact, address, patient_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Patient updated successfully!")
        self.clear_entries()
        self.view_patients()

    def delete_patient(self):
        """Delete a patient from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to delete!")
            return

        patient_id = self.tree.item(selected_item, "values")[0]

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Patients WHERE patient_id = ?', (patient_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Patient deleted successfully!")
        self.view_patients()

    def view_patients(self):
        """View all patients in the database."""
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Patients')
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
        self.entry_name.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.entry_gender.delete(0, tk.END)
        self.entry_contact.delete(0, tk.END)
        self.entry_address.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = PatientManagement(root)
    root.mainloop()

if __name__ == "__main__":
    main()
