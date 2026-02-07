from flask import Flask, render_template, request, redirect, url_for
import database
from logic import ClinicManager

app = Flask(__name__)
manager = ClinicManager()
database.init_db()

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Вход в личный кабинет
@app.route('/clients', methods=['GET', 'POST'])
def clients_login():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        client_obj = manager.register_client(name, phone)
        return redirect(url_for('dashboard', client_id=client_obj.client_id))

    all_clients = database.get_all_clients()
    return render_template('login.html', clients=all_clients)


# Обработка кнопки "Войти"
@app.route('/login_action', methods=['POST'])
def login_action():
    client_id = request.form['client_id']
    return redirect(url_for('dashboard', client_id=client_id))


# Личный кабинет
@app.route('/dashboard/<int:client_id>')
def dashboard(client_id):
    client = database.get_client(client_id)
    pets = database.get_client_pets(client_id)
    history = database.get_client_appointments(client_id)
    return render_template('dashboard.html', client=client, pets=pets, history=history)


# Добавление питомца (пациента)
@app.route('/add_pet/<int:client_id>', methods=['GET', 'POST'])
def add_pet(client_id):
    if request.method == 'POST':
        new_pet = manager.register_patient(
            owner_id=client_id,
            name=request.form['name'],
            species=request.form['species'],
            breed=request.form['breed'],
            dob=request.form['dob']
        )
        return render_template(
            'confirmation.html',
            title="Питомец добавлен!",
            message=f"Карточка для «{new_pet.name}» успешно создана.",
            client_id=client_id
        )

    return render_template('add_pet.html', client_id=client_id)


# Удаление питомца
@app.route('/delete_pet/<int:pet_id>/<int:client_id>')
def delete_pet(pet_id, client_id):
    database.delete_patient(pet_id)
    return redirect(url_for('dashboard', client_id=client_id))

# Запись к врачу
@app.route('/book/<int:client_id>', methods=['GET', 'POST'])
def book_appointment(client_id):
    if request.method == 'POST':
        # Форматирование даты
        raw_date = request.form['date_time']
        clean_date = raw_date.replace('T', ' ')

        manager.register_appointment(
            patient_id=request.form['patient_id'],
            doctor_id=request.form['doctor_id'],
            date_time=clean_date
        )
        return render_template(
            'confirmation.html',
            title="Вы записаны!",
            message=f"Ваш приём успешно запланирован на {clean_date}.",
            client_id=client_id
        )

    doctors = database.get_all_doctors()
    pets = database.get_client_pets(client_id)
    return render_template('book.html', doctors=doctors, pets=pets, client_id=client_id)


if __name__ == '__main__':
    app.run(debug=True)