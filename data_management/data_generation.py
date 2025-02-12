from faker import Faker
import sqlite3
import random

def generate_fake_data():
    """Generate and insert fake data into the hospital database."""
    conn = sqlite3.connect('../database/hospital.db')
    cursor = conn.cursor()
    fake = Faker()

    # Generate fake data for Rooms table
    room_types = ['Single', 'Shared', 'ICU', 'Deluxe']
    rooms_data = [
        (
            room_number, 
            random.choice(room_types), 
            random.choice([0, 1]),  # Randomly set room availability
            None if random.choice([0, 1]) == 1 else random.randint(1, 50)  # Assign patient ID if room is occupied
        )
        for room_number in range(101, 121)
    ]
    cursor.executemany('''
        INSERT INTO Rooms (room_number, room_type, is_available, assigned_patient_id)
        VALUES (?, ?, ?, ?)
    ''', rooms_data)

    # Generate fake data for Patients table
    patients_data = [
        (
            fake.name(),
            random.randint(1, 100),  # Age between 1 and 100
            random.choice(['Male', 'Female', 'Other']),
            fake.phone_number(),
            fake.address(),
            random.choice(['In Patient', 'Out Patient']),  # Categories
            random.choice(range(101, 121)),  # Random room number
            fake.date_this_year().isoformat()  # Random registration date
        )
        for _ in range(50)
    ]
    cursor.executemany('''
        INSERT INTO Patients (name, age, gender, contact_number, address, category, room_id, date_of_registration)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', patients_data)

    # Generate fake data for Doctors table
    specializations = ['Cardiologist', 'Neurologist', 'Pediatrician', 'Orthopedic', 'General Physician']
    doctors_data = [
        (
            fake.name(),
            random.choice(specializations),
            fake.phone_number(),
            random.choice(['Available', 'Unavailable'])
        )
        for _ in range(20)
    ]
    cursor.executemany('''
        INSERT INTO Doctors (name, specialization, contact_number, availability)
        VALUES (?, ?, ?, ?)
    ''', doctors_data)

    # Generate fake data for Appointments table
    appointments_data = [
        (
            random.randint(1, 50),  # Random patient ID
            random.randint(1, 20),  # Random doctor ID
            fake.date_this_year().isoformat(),
            fake.time(),
            random.choice(['Scheduled', 'Completed', 'Cancelled'])
        )
        for _ in range(100)
    ]
    cursor.executemany('''
        INSERT INTO Appointments (patient_id, doctor_id, date, time, status)
        VALUES (?, ?, ?, ?, ?)
    ''', appointments_data)

    # Generate fake data for Medical Records table
    medical_records_data = [
        (
            random.randint(1, 50),  # Random patient ID
            random.randint(1, 20),  # Random doctor ID
            fake.sentence(nb_words=6),  # Fake diagnosis
            fake.sentence(nb_words=8),  # Fake prescription
            fake.date_this_year().isoformat()
        )
        for _ in range(100)
    ]
    cursor.executemany('''
        INSERT INTO MedicalRecords (patient_id, doctor_id, diagnosis, prescription, date)
        VALUES (?, ?, ?, ?, ?)
    ''', medical_records_data)

    # Generate fake data for Billing table
    billing_data = [
        (
            random.randint(1, 50),  # Random patient ID
            round(random.uniform(500, 10000), 2),  # Random bill amount
            fake.date_this_year().isoformat(),
            random.choice(['Paid', 'Unpaid'])
        )
        for _ in range(50)
    ]
    cursor.executemany('''
        INSERT INTO Billing (patient_id, amount, date, status)
        VALUES (?, ?, ?, ?)
    ''', billing_data)

    # Generate fake data for Users table
    roles = ['Admin', 'Doctor', 'Receptionist']
    users_data = [
        (
            fake.user_name(),
            fake.password(),
            random.choice(roles)
        )
        for _ in range(10)
    ]
    cursor.executemany('''
        INSERT INTO Users (username, password, role)
        VALUES (?, ?, ?)
    ''', users_data)

    conn.commit()
    print("Fake data generated successfully.")
    conn.close()

if __name__ == "__main__":
    generate_fake_data()
