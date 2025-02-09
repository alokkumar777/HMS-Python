import sqlite3

def view_users_table(conn):
    """Fetch and display all data from the Users table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()

    # Display the data
    print("Users Table:")
    print("ID | Username | Password | Role")
    print("-" * 30)
    for row in rows:
        print(row)

# Connect to the database and call the function
conn = sqlite3.connect('hospital.db')
view_users_table(conn)
conn.close()
