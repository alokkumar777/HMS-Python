import sqlite3

def add_user():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    # Insert single user at a time using execute
    cursor.execute('''
        INSERT INTO Users (username, password, role)
        VALUES (?, ?, ?)
    ''', ('Alok Kumar', 'itsak123', 'Admin'))

    # Commit the changes
    conn.commit()
    conn.close()
    print("Test users added successfully.")

add_user()
