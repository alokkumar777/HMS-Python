import sqlite3

def update_user(current_username, new_username=None, new_password=None, new_role=None):
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Dynamic query construction
    updates = []
    params = []

    if new_username:
        updates.append("username = ?")
        params.append(new_username)
    if new_password:
        updates.append("password = ?")
        params.append(new_password)
    if new_role:
        updates.append("role = ?")
        params.append(new_role)

    if not updates:
        print("No updates specified. Please provide new values.")
        conn.close()
        return

    # Add the WHERE clause at the end
    params.append(current_username)
    query = f"UPDATE Users SET {', '.join(updates)} WHERE username = ?"

    cursor.execute(query, params)
    conn.commit()
    conn.close()
    print(f"User '{current_username}' updated successfully.")

# Example Usage
# update_user("Alok Kumar", new_username="Alok123", new_password="newpassword123", new_role="Super Admin")
# update_user("doctor1", new_username="doctor2")
# update_user("receptionist1", new_role="Head Receptionist")

