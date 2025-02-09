import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class DoctorManagement:
    def __init__(self, root, back_to_dashboard):
        self.root = root
        self.back_to_dashboard = back_to_dashboard
        self.root.title("Doctor Management")
        self.root.geometry("1300x630")
        self.root.option_add("*Font", "Verdana 10")

        # Title Label
        label_title = ttk.Label(root, text="Doctor Management", font=("Verdana", 20, "bold"))
        label_title.pack(pady=10)

        # Input Fields
        frame_input = tk.Frame(root)
        frame_input.pack(pady=10)

        ttk.Label(frame_input, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ttk.Entry(frame_input, width=30)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Specialization:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_specialization = ttk.Entry(frame_input, width=30)
        self.entry_specialization.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Contact Number:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_contact = ttk.Entry(frame_input, width=30)
        self.entry_contact.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Availability:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_availability = ttk.Entry(frame_input, width=30)
        self.entry_availability.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        style = ttk.Style()
        # Configure the font size for the button
        style.configure("Custom.TButton", font=("Verdana", 10))
        style.configure("Custom.Treeview", font=("Verdana", 10))
        style.configure("Custom.Treeview.Heading", font=("Verdana", 10, "bold"))
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        ttk.Button(frame_buttons, text="Add Doctor", command=self.add_doctor, padding=10, style="Custom.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(frame_buttons, text="Update Doctor", command=self.update_doctor, padding=10, style="Custom.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(frame_buttons, text="Delete Doctor", command=self.delete_doctor, padding=10, style="Custom.TButton").grid(row=0, column=2, padx=5)
        ttk.Button(frame_buttons, text="View All Doctors", command=self.view_doctors, padding=10, style="Custom.TButton").grid(row=0, column=3, padx=5)
        ttk.Button(frame_buttons, text="Back to Dashboard", command=self.go_back_to_dashboard, padding=10, style="Custom.TButton").grid(row=1, column=0, columnspan=4, pady=10)


        # Doctor List (Treeview)
        frame_list = tk.Frame(root)
        frame_list.pack(pady=10)

        self.tree = ttk.Treeview(frame_list, columns=("ID", "Name", "Specialization", "Contact", "Availability"), show="headings", style="Custom.Treeview", padding=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Specialization", text="Specialization")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("Availability", text="Availability")
        self.tree.pack()

        # Load initial data
        self.view_doctors()

    def go_back_to_dashboard(self):
        """Return to the admin dashboard."""
        self.root.destroy()  # Close the current window
        self.back_to_dashboard()  # Open the admin dashboard

    def add_doctor(self):
        """Add a new doctor to the database."""
        name = self.entry_name.get()
        specialization = self.entry_specialization.get()
        contact = self.entry_contact.get()
        availability = self.entry_availability.get()

        if not name or not specialization or not contact or not availability:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Doctors (name, specialization, contact_number, availability)
            VALUES (?, ?, ?, ?)
        ''', (name, specialization, contact, availability))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Doctor added successfully!")
        self.clear_entries()
        self.view_doctors()

    def update_doctor(self):
        """Update doctor details."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a doctor to update!")
            return

        doctor_id = self.tree.item(selected_item, "values")[0]
        name = self.entry_name.get()
        specialization = self.entry_specialization.get()
        contact = self.entry_contact.get()
        availability = self.entry_availability.get()

        if not name or not specialization or not contact or not availability:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Doctors
            SET name = ?, specialization = ?, contact_number = ?, availability = ?
            WHERE doctor_id = ?
        ''', (name, specialization, contact, availability, doctor_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Doctor updated successfully!")
        self.clear_entries()
        self.view_doctors()

    def delete_doctor(self):
        """Delete a doctor from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a doctor to delete!")
            return

        doctor_id = self.tree.item(selected_item, "values")[0]

        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Doctors WHERE doctor_id = ?', (doctor_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Doctor deleted successfully!")
        self.view_doctors()

    def view_doctors(self):
        """View all doctors in the database."""
        conn = sqlite3.connect('database/hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Doctors')
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
        self.entry_specialization.delete(0, tk.END)
        self.entry_contact.delete(0, tk.END)
        self.entry_availability.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = DoctorManagement(root, lambda: None)
    root.mainloop()

if __name__ == "__main__":
    main()