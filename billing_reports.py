import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from tkinter import simpledialog
import pandas as pd
from datetime import datetime

class BillingReports:
    def __init__(self, root, back_to_dashboard):
        self.root = root
        self.back_to_dashboard = back_to_dashboard
        self.root.title("Billing and Reports")
        self.root.geometry("1000x600")

        # Title Label
        label_title = tk.Label(root, text="Billing and Reports", font=("Arial", 20, "bold"))
        label_title.pack(pady=10)

        # Input Fields
        frame_input = tk.Frame(root)
        frame_input.pack(pady=10)

        # Patient Dropdown
        tk.Label(frame_input, text="Patient:").grid(row=0, column=0, padx=5, pady=5)
        self.patient_var = tk.StringVar()
        self.patient_dropdown = ttk.Combobox(frame_input, textvariable=self.patient_var, width=30)
        self.patient_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.load_patients()

        # Amount and Date
        tk.Label(frame_input, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_amount = tk.Entry(frame_input, width=30)
        self.entry_amount.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.entry_date = tk.Entry(frame_input, width=30)
        self.entry_date.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Generate Bill", command=self.generate_bill).grid(row=0, column=0, padx=5)
        tk.Button(frame_buttons, text="View Billing History", command=self.view_billing_history).grid(row=0, column=1, padx=5)
        tk.Button(frame_buttons, text="Generate Revenue Report", command=self.generate_revenue_report).grid(row=0, column=2, padx=5)
        ttk.Button(frame_buttons, text="Back to Dashboard", command=self.go_back_to_dashboard, padding=10).grid(row=1, column=0, columnspan=4, pady=10)


        # Billing History (Treeview)
        frame_list = tk.Frame(root)
        frame_list.pack(pady=10)

        self.tree = ttk.Treeview(frame_list, columns=("ID", "Patient", "Amount", "Date", "Status"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Patient", text="Patient")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Status", text="Status")
        self.tree.pack()

        # Load initial data
        self.view_billing_history()

    def go_back_to_dashboard(self):
        """Return to the admin dashboard."""
        self.root.destroy()  # Close the current window
        self.back_to_dashboard()  # Open the admin dashboard

    def load_patients(self):
        """Load patients into the dropdown."""
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT patient_id, name FROM Patients')
        patients = cursor.fetchall()
        conn.close()
        self.patient_dropdown['values'] = [f"{patient[0]} - {patient[1]}" for patient in patients]

    def generate_bill(self):
        """Generate a new bill."""
        patient = self.patient_var.get()
        amount = self.entry_amount.get()
        date = self.entry_date.get()

        if not patient or not amount or not date:
            messagebox.showerror("Error", "All fields are required!")
            return

        patient_id = patient.split(" - ")[0]

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Billing (patient_id, amount, date, status)
            VALUES (?, ?, ?, ?)
        ''', (patient_id, amount, date, "Unpaid"))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Bill generated successfully!")
        self.clear_entries()
        self.view_billing_history()

    def view_billing_history(self):
        """View all billing history in the database."""
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.bill_id, p.name, b.amount, b.date, b.status
            FROM Billing b
            JOIN Patients p ON b.patient_id = p.patient_id
        ''')
        rows = cursor.fetchall()
        conn.close()

        # Clear existing data in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new data
        for row in rows:
            self.tree.insert("", "end", values=row)

    def generate_revenue_report(self):
        """Generate a revenue report."""
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, SUM(amount) as total_revenue
            FROM Billing
            WHERE status = 'Paid'
            GROUP BY date
        ''')
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("Info", "No revenue data available.")
            return

        # Create a DataFrame for the report
        df = pd.DataFrame(rows, columns=["Date", "Total Revenue"])
        print(df)  # Print the report to the console (or save it to a file)

        # Display the report in a new window
        report_window = tk.Toplevel(self.root)
        report_window.title("Revenue Report")

        tree = ttk.Treeview(report_window, columns=("Date", "Total Revenue"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Total Revenue", text="Total Revenue")
        tree.pack()

        for _, row in df.iterrows():
            tree.insert("", "end", values=(row["Date"], row["Total Revenue"]))

    def clear_entries(self):
        """Clear all input fields."""
        self.patient_var.set("")
        self.entry_amount.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = BillingReports(root)
    root.mainloop()

if __name__ == "__main__":
    main()

    