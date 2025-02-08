from faker import Faker

faker = Faker()

def generate_fake_patients(conn, count=50):
    """Generate fake data for the Patients table."""
    cursor = conn.cursor()
    fake_data = []
    for _ in range(count):
        fake_data.append((
            faker.name(),
            faker.random_int(min=1, max=100),
            faker.random_element(elements=["Male", "Female", "Other"]),
            faker.phone_number(),
            faker.address().replace("\n", ", "),
            faker.date_this_decade().isoformat()
        ))
    cursor.executemany('''
        INSERT INTO Patients (name, age, gender, contact_number, address, date_of_registration)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', fake_data)
    conn.commit()
    print(f"{count} fake patients added successfully.")

def generate_fake_doctors(conn, count=20):
    """Generate fake data for the Doctors table."""
    cursor = conn.cursor()
    medical_specializations = [
        "Cardiologist", "Neurologist", "Orthopedic Surgeon", "Pediatrician",
        "General Physician", "Dermatologist", "Psychiatrist", "Oncologist",
        "Radiologist", "Endocrinologist", "Anesthesiologist", "Nephrologist",
        "Urologist", "Gastroenterologist", "Hematologist", "Pulmonologist"
    ]
    fake_data = []
    for _ in range(count):
        fake_data.append((
            faker.name(),
            faker.random_element(elements=medical_specializations),
            faker.phone_number(),
            faker.random_element(elements=["Available", "Unavailable"])
        ))
    cursor.executemany('''
        INSERT INTO Doctors (name, specialization, contact_number, availability)
        VALUES (?, ?, ?, ?)
    ''', fake_data)
    conn.commit()
    print(f"{count} fake doctors added successfully.")


def generate_fake_appointments(conn, count=30):
    """Generate fake data for the Appointments table."""
    cursor = conn.cursor()
    cursor.execute('SELECT patient_id FROM Patients')
    patient_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT doctor_id FROM Doctors')
    doctor_ids = [row[0] for row in cursor.fetchall()]
    fake_data = []
    for _ in range(count):
        fake_data.append((
            faker.random_element(elements=patient_ids),
            faker.random_element(elements=doctor_ids),
            faker.date_this_month().isoformat(),
            faker.time(),
            faker.random_element(elements=["Scheduled", "Completed", "Cancelled"])
        ))
    cursor.executemany('''
        INSERT INTO Appointments (patient_id, doctor_id, date, time, status)
        VALUES (?, ?, ?, ?, ?)
    ''', fake_data)
    conn.commit()
    print(f"{count} fake appointments added successfully.")

def generate_fake_medical_records(conn, count=30):
    """Generate fake data for the Medical Records table."""
    cursor = conn.cursor()
    cursor.execute('SELECT patient_id FROM Patients')
    patient_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT doctor_id FROM Doctors')
    doctor_ids = [row[0] for row in cursor.fetchall()]
    fake_data = []
    for _ in range(count):
        fake_data.append((
            faker.random_element(elements=patient_ids),
            faker.random_element(elements=doctor_ids),
            faker.sentence(),
            faker.sentence(),
            faker.date_this_year().isoformat()
        ))
    cursor.executemany('''
        INSERT INTO MedicalRecords (patient_id, doctor_id, diagnosis, prescription, date)
        VALUES (?, ?, ?, ?, ?)
    ''', fake_data)
    conn.commit()
    print(f"{count} fake medical records added successfully.")

def generate_fake_billing(conn, count=20):
    """Generate fake data for the Billing table."""
    cursor = conn.cursor()
    cursor.execute('SELECT patient_id FROM Patients')
    patient_ids = [row[0] for row in cursor.fetchall()]
    fake_data = []
    for _ in range(count):
        fake_data.append((
            faker.random_element(elements=patient_ids),
            round(faker.random_number(digits=4, fix_len=True) / 100, 2),  # Random amount
            faker.date_this_month().isoformat(),
            faker.random_element(elements=["Paid", "Pending", "Cancelled"])
        ))
    cursor.executemany('''
        INSERT INTO Billing (patient_id, amount, date, status)
        VALUES (?, ?, ?, ?)
    ''', fake_data)
    conn.commit()
    print(f"{count} fake billing records added successfully.")

def generate_fake_users(conn, count=10):
    """Generate fake data for the Users table."""
    cursor = conn.cursor()
    roles = ["Admin", "Doctor", "Receptionist"]
    fake_data = []
    for _ in range(count):
        fake_data.append((
            faker.user_name(),
            faker.password(),
            faker.random_element(elements=roles)
        ))
    cursor.executemany('''
        INSERT INTO Users (username, password, role)
        VALUES (?, ?, ?)
    ''', fake_data)
    conn.commit()
    print(f"{count} fake users added successfully.")
