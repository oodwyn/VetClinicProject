from datetime import date, datetime

class Patient:
    def __init__(self, patient_id, name, species, breed, dob, client_id):
        self.patient_id = patient_id
        self.name = name
        self.species = species
        self.breed = breed
        self.dob = dob
        self.client_id = client_id

    def __del__(self):
        pass

    def __str__ (self):
        return f"""
        ###########################
             КАРТОЧКА ПАЦИЕНТА
        ###########################
        Кличка: {self.name}
        Вид: {self.species}
        Порода: {self.breed}
        Дата рождения: {self.dob} (Возраст: {self.get_age()})
        Владелец: {self.client_id}
        ---------------------------
        """

    def get_age(self):
        today = date.today()
        date_obj = datetime.strptime(self.dob, '%d/%m/%Y')
        total_months = (today.year - date_obj.year) * 12 + (today.month - date_obj.month)
        if today.day < date_obj.day: total_months -= 1
        years = total_months // 12
        months = total_months % 12
        if years > 0:
            return f"{years} лет {months} месяцев" # потом исправить окончания
        else:
            return f"{months} месяцев"

    def get_medical_history(self):
        pass

class Client:
    def __init__(self, client_id, name, phone):
        self.client_id = client_id
        self.name = name
        self.phone = phone
        self.pets = []

    def __del__(self):
        pass

    def __str__ (self):
        return f"""
            ----Клиент----
        ФИО: {self.name}
        Телефон: {self.phone}
            --------------
        """

    def add_pet(self, patient_object):
        self.pets.append(patient_object)

class Doctor:
    def __init__(self, doctor_id, name, speciality):
        self.doctor_id = doctor_id
        self.name = name
        self.speciality = speciality

    def __del__(self):
        pass

    def __str__ (self):
        return f"""
            ---- Врач ----
        ФИО: {self.name}
        Специализация: {self.speciality}
            --------------
        """

class Appointment:
    def __init__(self, appointment_id, patient, doctor, date_time, status="Запланирован", diagnosis="", treatment=""):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.date_time = date_time
        self.status = status
        self.diagnosis = diagnosis
        self.treatment = treatment

    def __del__(self):
        pass

    def __str__ (self):
        if self.status == "Запланирован":
            return f"""
                ---- Запись ----
            Дата: {self.date_time}
            Врач: {self.doctor.name}
            Пациент: {self.patient.name}
                ----------------
            """
        elif self.status == "Отменен":
            return f"""
                ---- Запись ОТМЕНЕНА (Просрочена) ----
            Дата: {self.date_time}
            Врач: {self.doctor.name}
            Пациент: {self.patient.name}
                --------------------------------------
            """
        else:
            return f"""
                ---- Медицинская карточка ----
            Дата: {self.date_time}
            Врач: {self.doctor.name}
            Пациент: {self.patient.name}
            Диагноз: {self.diagnosis}
            Назначения: {self.treatment}
                ------------------------------
            """

    def complete_visit(self, diagnosis, treatment):
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.status = "Завершен"

    def check_status(self):
        now = datetime.now()
        appt_time = datetime.strptime(self.date_time, '%d/%m/%Y %H:%M')
        if self.status == "Запланирован" and appt_time < now:
            self.status = "Отменен"

