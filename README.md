# Hospital Management System (HMS)

The **Hospital Management System (HMS)** is a Python-based application designed to manage hospital operations such as patient registration, doctor management, appointment scheduling, medical records, and billing. It uses `tkinter` for the graphical user interface (GUI) and `SQLite3` for the database.

---

## Features

- **Role-Based Access**:
  - Admin: Manage patients, doctors, appointments, billing, and medical records.
  - Doctor: View appointments and patient records.
  - Receptionist: Manage appointments and patient registrations.
- **Patient Management**: Add, update, delete, and view patient details.
- **Doctor Management**: Add, update, delete, and view doctor details.
- **Appointment Management**: Schedule, update, and cancel appointments.
- **Medical Records**: Add and view medical records for patients.
- **Billing and Reports**: Generate bills and view revenue reports.

## Installation and Setup

### Step 1: Clone the Repository

1. Open a terminal or command prompt.
2. Clone the project repository:

   ```bash
   git clone https://github.com/alokkumar777/HMS-Python.git
   ```

3. Navigate to the project directory:
   ```bash
   cd hms-python
   ```

### Step 2: Set Up a Virtual Environment

1. Create a virtual environment:

   ```bash
   python -m venv hms_env
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     hms_env\Scripts\activate
     ```
   - macOS/Linux
     ```bash
     source hms_env/bin/activate
     ```

### Step 3: Install Required Libraries

- Install the required libraries using `pip`:

  ```bash
  pip install -r requirements.txt
  ```

### Step 4: Initialize the Database

1. Run the `database.py` script to create the database and tables:

   ```bash
   cd database
   py database.py
   ```

2. Add test users to the database (optional):
   ```bash
   cd ..
   cd user_management
   py add_users.py
   ```
3. Generate fake data (optional):
   ```bash
   cd ..
   cd data_management
   py main_data_gen.py
   ```

### Step 5: Run the Application

1. Start the application by running the `start.py` script:

   ```bash
   cd ..
   py start.py
   ```

2. Use the following credentials to log in:
   - Admin:
     - Username: `Admin`
     - Password: `admin123`
   - Doctor:
     - Username: `fisher`
     - Password: `fisher123`
   - Receptionist:
     - Username: `recep`
     - Password: `recep123`

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push them to your fork.
4. Submit a pull request.

---

Enjoy using the Hospital Management System! 🏥
