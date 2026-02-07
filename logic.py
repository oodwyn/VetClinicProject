import database
from models import Client, Patient, Doctor, Appointment
from datetime import datetime

class ClinicManager:
    def __init__(self):
        database.init_db()

    def register_client(self, name, phone):
        client = Client(None, name, phone)
        client_id = database.insert_client(client)
        client.client_id = client_id
        print(f"Клиент {client.name} успешно зарегистрирован с ID: {client_id}")
        return client

    def register_patient(self, owner_id, name, species, breed, dob):
        patient = Patient(None, name, species, breed, dob, owner_id)
        patient_id = database.insert_patient(patient)
        patient.patient_id = patient_id
        print(f"Пациент {patient.name} успешно добавлен с ID: {patient_id}")
        return patient

    def register_doctor(self, name, speciality):
        doctor = Doctor(None, name, speciality)
        doctor_id = database.insert_doctor(doctor)
        print(f"Врач {doctor.name} успешно добавлен с ID: {doctor_id}")
        return doctor

    def register_appointment(self, patient_id, doctor_id, date_time):
        patient_obj = database.get_patient_by_id(patient_id)
        doctor_obj = database.get_doctor_by_id(doctor_id)

        if not patient_obj or not doctor_obj:
            print("Ошибка: Пациент или Врач не найдены.")
            return None

        appointment = Appointment(
            None,
            patient_obj,
            doctor_obj,
            date_time,
            status="Запланирован",
            diagnosis="",
            treatment=""
        )

        appointment_id = database.insert_appointment(appointment)
        print(f"Запись о медицинском обследовании успешно добавлена с ID: {appointment_id}")
        return appointment
