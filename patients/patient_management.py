import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class PatientManagement:
    def __init__(self, root, back_to_dashboard):
        self.root = root
        self.back_to_dashboard = back_to_dashboard
        self.root.title("Patient Management")
        self.root.geometry("1300x800")
        self.root.option_add("*Font", "Verdana 10")
        
        # Title Label
        label_title = tk.Label(root, text="Patient Management", font=("Verdana", 20, "bold"))
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

        # Category Selection
        ttk.Label(frame_input, text="Category:").grid(row=5, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar(value="Outpatient")
        ttk.Radiobutton(frame_input, text="Inpatient", variable=self.category_var, value="Inpatient", command=self.toggle_room_selection).grid(row=5, column=1, padx=5, pady=5)
        ttk.Radiobutton(frame_input, text="Outpatient", variable=self.category_var, value="Outpatient", command=self.toggle_room_selection).grid(row=5, column=2, padx=5, pady=5)

        # Room Selection
        ttk.Label(frame_input, text="Room:").grid(row=6, column=0, padx=5, pady=5)
        self.room_var = tk.StringVar()
        self.room_dropdown = ttk.Combobox(frame_input, textvariable=self.room_var, state="disabled", width=27)
        self.room_dropdown.grid(row=6, column=1, padx=5, pady=5)
        self.load_available_rooms()

        # Search Fields
        frame_search = tk.Frame(root)
        frame_search.pack(pady=10)

        ttk.Label(frame_search, text="Search by ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_search_id = ttk.Entry(frame_search, width=15)
        self.entry_search_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_search, text="Search by Name:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_search_name = ttk.Entry(frame_search, width=15)
        self.entry_search_name.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(frame_search, text="Search", command=self.search_patient, padding=1, style="Custom.TButton").grid(row=0, column=4, pady=5, padx=5)


        # Buttons
        style = ttk.Style()
        # Configure the font size for the button
        style.configure("Custom.TButton", font=("Verdana", 10))
        style.configure("Custom.Treeview", font=("Verdana", 10))
        style.configure("Custom.Treeview.Heading", font=("Verdana", 10, "bold"))
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        ttk.Button(frame_buttons, text="Add Patient", command=self.add_patient, padding=10, style="Custom.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(frame_buttons, text="Update Patient", command=self.load_patient_for_update, padding=10, style="Custom.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(frame_buttons, text="Delete Patient", command=self.delete_patient, padding=10, style="Custom.TButton").grid(row=0, column=2, padx=5)
        ttk.Button(frame_buttons, text="View All Patients", command=self.view_patients, padding=10, style="Custom.TButton").grid(row=0, column=3, padx=5)
        ttk.Button(frame_buttons, text="Back to Dashboard", command=self.go_back_to_dashboard, padding=10, style="Custom.TButton").grid(row=1, column=0, columnspan=4, pady=10)

        # Patient List (Treeview)
        frame_list = tk.Frame(root)
        frame_list.pack(pady=10)

        self.tree = ttk.Treeview(frame_list, columns=("ID", "Name", "Age", "Gender", "Contact", "Address", "Category", "Room"), show="headings", style="Custom.Treeview", padding=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Room", text="Room")
        self.tree.pack()

        # Adjust the width
        self.tree.column("ID", width=60)
        self.tree.column("Name", width=150)
        self.tree.column("Age", width=50)
        self.tree.column("Gender", width=100)
        self.tree.column("Contact", width=200)
        self.tree.column("Address", width=250)
        self.tree.column("Category", width=150)
        # Load initial data
        self.view_patients()

    def toggle_room_selection(self):
        if self.category_var.get() == "Inpatient":
            self.room_dropdown["state"] = "readonly"
        else:
            self.room_dropdown["state"] = "disabled"
            self.room_var.set("")

    def load_available_rooms(self):
        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute("SELECT room_number FROM Rooms WHERE is_available = 1")
        rooms = [row[0] for row in cursor.fetchall()]
        conn.close()
        self.room_dropdown["values"] = rooms
    
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
        category = self.category_var.get()
        room_number = self.room_var.get() if category == "Inpatient" else None

        if not name or not age or not gender or not contact or not address or (category == "Inpatient" and not room_number):
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()

        room_id = None
        if category == "Inpatient" and room_number:
            cursor.execute("SELECT room_id FROM Rooms WHERE room_number = ?", (room_number,))
            room_id = cursor.fetchone()[0]
            cursor.execute("UPDATE Rooms SET is_available = 0 WHERE room_id = ?", (room_id,))

        cursor.execute('''
            INSERT INTO Patients (name, age, gender, contact_number, address, date_of_registration, category, room_id)
            VALUES (?, ?, ?, ?, ?, DATE('now'), ?, ?)
        ''', (name, age, gender, contact, address, category, room_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Patient added successfully!")
        self.clear_entries()
        self.view_patients()


    def load_patient_for_update(self):
        """Load selected patient's data into input fields for updating."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to update!")
            return

        patient_id = self.tree.item(selected_item, "values")[0]

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Patients WHERE patient_id = ?', (patient_id,))
        patient = cursor.fetchone()
        conn.close()

        if patient:
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, patient[1])
            self.entry_age.delete(0, tk.END)
            self.entry_age.insert(0, patient[2])
            self.entry_gender.delete(0, tk.END)
            self.entry_gender.insert(0, patient[3])
            self.entry_contact.delete(0, tk.END)
            self.entry_contact.insert(0, patient[4])
            self.entry_address.delete(0, tk.END)
            self.entry_address.insert(0, patient[5])

        self.update_button = ttk.Button(self.root, text="Save Changes", command=lambda: self.update_patient(patient_id) , padding=5, style="Custom.TButton")
        self.update_button.pack(pady=10)

    def update_patient(self, patient_id):
        """Update patient details."""
        name = self.entry_name.get()
        age = self.entry_age.get()
        gender = self.entry_gender.get()
        contact = self.entry_contact.get()
        address = self.entry_address.get()
        category = self.category_var.get()
        new_room_number = self.room_var.get() if category == "Inpatient" else None

        if not name or not age or not gender or not contact or not address:
            messagebox.showerror("Error", "All fields are required!")
            return

        if category == "Inpatient" and not new_room_number:
            messagebox.showerror("Error", "Room number is required for inpatients!")
            return

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()

        try:
            # Get current patient information
            cursor.execute('''
                SELECT category, room_id 
                FROM Patients 
                WHERE patient_id = ?
            ''', (patient_id,))
            current_info = cursor.fetchone()
            current_category, current_room_id = current_info if current_info else (None, None)

            # Handle room changes
            new_room_id = None
            if category == "Inpatient":
                # Get new room ID
                cursor.execute("SELECT room_id FROM Rooms WHERE room_number = ?", (new_room_number,))
                new_room_id = cursor.fetchone()[0]

                # If patient already had a room, free it up (unless it's the same room)
                if current_room_id and current_room_id != new_room_id:
                    cursor.execute("UPDATE Rooms SET is_available = 1, assigned_patient_id = NULL WHERE room_id = ?", 
                                (current_room_id,))

                # Mark new room as occupied
                cursor.execute("UPDATE Rooms SET is_available = 0, assigned_patient_id = ? WHERE room_id = ?", 
                            (patient_id, new_room_id))
            else:
                # If patient was previously an inpatient, free up their room
                if current_room_id:
                    cursor.execute("UPDATE Rooms SET is_available = 1, assigned_patient_id = NULL WHERE room_id = ?", 
                                (current_room_id,))

            # Update patient information
            cursor.execute('''
                UPDATE Patients
                SET name = ?, age = ?, gender = ?, contact_number = ?, 
                    address = ?, category = ?, room_id = ?
                WHERE patient_id = ?
            ''', (name, age, gender, contact, address, category, new_room_id, patient_id))

            conn.commit()
            messagebox.showinfo("Success", "Patient updated successfully!")
            
        except sqlite3.Error as e:
            conn.rollback()
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()
            self.clear_entries()
            self.view_patients()
            if hasattr(self, 'update_button'):
                self.update_button.destroy()

    def delete_patient(self):
        """Delete a patient from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to delete!")
            return

        patient_id = self.tree.item(selected_item, "values")[0]

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Patients WHERE patient_id = ?', (patient_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Patient deleted successfully!")
        self.view_patients()

    def view_patients(self):
        """View all patients in the database."""
        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.patient_id, p.name, p.age, p.gender, p.contact_number, 
                p.address, p.category, COALESCE(r.room_number, '')
            FROM Patients p
            LEFT JOIN Rooms r ON p.room_id = r.room_id
        ''')
        rows = cursor.fetchall()
        conn.close()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in rows:
            self.tree.insert("", "end", values=row)

    def search_patient(self):
        """Search for patients by ID or Name."""
        search_id = self.entry_search_id.get()
        search_name = self.entry_search_name.get()

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()

        if search_id:
            cursor.execute('''
                SELECT p.patient_id, p.name, p.age, p.gender, p.contact_number, 
                    p.address, p.category, COALESCE(r.room_number, '')
                FROM Patients p
                LEFT JOIN Rooms r ON p.room_id = r.room_id
                WHERE p.patient_id = ?
            ''', (search_id,))
        elif search_name:
            cursor.execute('''
                SELECT p.patient_id, p.name, p.age, p.gender, p.contact_number, 
                    p.address, p.category, COALESCE(r.room_number, '')
                FROM Patients p
                LEFT JOIN Rooms r ON p.room_id = r.room_id
                WHERE p.name LIKE ?
            ''', (f'%{search_name}%',))
        else:
            messagebox.showerror("Error", "Please enter an ID or Name to search!")
            conn.close()
            return

        rows = cursor.fetchall()
        conn.close()

        if rows:
            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in rows:
                self.tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("No Results", "No patients found matching the search criteria.")


    def clear_entries(self):
        """Clear all input fields."""
        self.entry_name.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.entry_gender.delete(0, tk.END)
        self.entry_contact.delete(0, tk.END)
        self.entry_address.delete(0, tk.END)
        self.room_dropdown.set("")
        self.category_var.set("Outpatient")

def main():
    root = tk.Tk()
    app = PatientManagement(root, lambda:None)
    root.mainloop()

if __name__ == "__main__":
    main()
