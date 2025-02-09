import sqlite3

def delete_users():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Specify the usernames of users to delete
    users_to_delete = [
        ("Ak",),  # Replace with the usernames you want to delete
        # ("doctor1",),
        # ("receptionist1",)
    ]

    cursor.executemany('DELETE FROM Users WHERE username = ?', users_to_delete)
    conn.commit()
    conn.close()
    print("Specified users deleted successfully.")

delete_users()
