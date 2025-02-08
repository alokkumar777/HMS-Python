import sqlite3

def create_connection():
    """Create a database connection."""
    conn = sqlite3.connect('hospital.db')
    return conn

def create_tables(conn):
    """Create all the necessary tables."""
    cursor = conn.cursor()
    
    # Patients Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            contact_number TEXT,
            address TEXT,
            date_of_registration TEXT
        )
    ''')

    # Doctors Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            contact_number TEXT,
            availability TEXT
        )
    ''')

    # Appointments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            date TEXT,
            time TEXT,
            status TEXT,
            FOREIGN KEY (patient_id) REFERENCES Patients (patient_id),
            FOREIGN KEY (doctor_id) REFERENCES Doctors (doctor_id)
        )
    ''')

    # Medical Records Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MedicalRecords (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            diagnosis TEXT,
            prescription TEXT,
            date TEXT,
            FOREIGN KEY (patient_id) REFERENCES Patients (patient_id),
            FOREIGN KEY (doctor_id) REFERENCES Doctors (doctor_id)
        )
    ''')

    # Billing Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Billing (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            amount REAL,
            date TEXT,
            status TEXT,
            FOREIGN KEY (patient_id) REFERENCES Patients (patient_id)
        )
    ''')

    # Users Table (for login)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    conn.commit()
    print("Tables created successfully.")


if __name__ == "__main__":
    conn = create_connection()
    create_tables(conn)
    conn.close()

    