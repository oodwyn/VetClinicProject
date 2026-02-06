import sqlite3
from models import Client, Patient, Doctor


def init_db():
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
   ''' )

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        species TEXT NOT NULL,
        breed TEXT NOT NULL,
        dob TEXT NOT NULL,
        client_id INTEGER,
        FOREIGN KEY (client_id) REFERENCES clients (client_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Doctors (
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        speciality TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Appointments (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        date_time TEXT NOT NULL,
        status TEXT NOT NULL,
        diagnosis TEXT,
        treatment TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
        FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
        )
    ''')

    connection.commit()
    connection.close()

def insert_client(client_obj):
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Clients (name, phone) VALUES (?, ?)",
        (client_obj.name, client_obj.phone)
    )
    new_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return new_id

def insert_patient(patient_obj):
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Patients (name, species, breed, dob, client_id) VALUES (?, ?, ?, ?, ?)",
        (patient_obj.name, patient_obj.species, patient_obj.breed, patient_obj.dob, patient_obj.client_id)
    )
    new_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return new_id

def insert_doctor(doctor_obj):
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Doctors (name, speciality) VALUES (?, ?)",
                   (doctor_obj.name, doctor_obj.speciality)
    )
    new_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return new_id

def insert_appointment(appointment_obj):
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Appointments (patient_id, doctor_id, date_time, status, diagnosis, treatment) VALUES (?, ?, ?, ?, ?, ?)",
        (
            appointment_obj.patient.patient_id,
            appointment_obj.doctor.doctor_id,
            appointment_obj.date_time,
            appointment_obj.status,
            appointment_obj.diagnosis,
            appointment_obj.treatment
        )
    )
    new_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return new_id


def get_patient_by_id(p_id):
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Patients WHERE patient_id = ?", (p_id,))
    data = cursor.fetchone()
    connection.close()

    if data:
        return Patient(data[0], data[1], data[2], data[3], data[4], data[5])
    return None

def get_doctor_by_id(d_id):
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Doctors WHERE doctor_id = ?", (d_id,))
    data = cursor.fetchone()
    connection.close()

    if data:
        return Doctor(data[0], data[1], data[2])
    return None

if __name__ == '__main__':
    init_db()

def get_all_patients():
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    cursor.execute('''
                   SELECT p.patient_id, p.name, p.species, p.breed, p.dob, c.name
                   FROM Patients p
                            JOIN Clients c ON p.client_id = c.client_id
                   ''')
    data = cursor.fetchall()
    connection.close()
    return data

def update_patient(p_id, name, species, breed, dob): # обновляет данные пациента
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    cursor.execute('''
                   UPDATE Patients
                   SET name=?,
                       species=?,
                       breed=?,
                       dob=?
                   WHERE patient_id = ?
                   ''', (name, species, breed, dob, p_id))
    connection.commit()
    connection.close()

def delete_patient(p_id): # Удаляет пациента
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Patients WHERE patient_id = ?", (p_id,))
    connection.commit()
    connection.close()

def get_all_clients(): # Выпадающий список
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    cursor.execute("SELECT client_id, name FROM Clients")
    data = cursor.fetchall()
    connection.close()
    return data