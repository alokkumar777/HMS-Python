import sqlite3
from database import create_connection, create_tables
from data_generation import (
    generate_fake_patients, 
    generate_fake_doctors, 
    generate_fake_appointments,
    generate_fake_medical_records, 
    generate_fake_billing, 
    generate_fake_users
)

if __name__ == "__main__":
    conn = create_connection()
    create_tables(conn)

    generate_fake_patients(conn, count=50)
    generate_fake_doctors(conn, count=20)
    generate_fake_appointments(conn, count=30)
    generate_fake_medical_records(conn, count=30)
    generate_fake_billing(conn, count=20)
    generate_fake_users(conn, count=10)

    conn.close()
