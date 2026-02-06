from flask import Flask, render_template, request, redirect, url_for
import database
from models import Client

app = Flask(__name__)
database.init_db()

# Главная страница
@app.route('/')
def index():
    patients = database.get_all_patients()
    return render_template('index.html', patients=patients)

# Добавление пациента
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        breed = request.form['breed']
        dob = request.form['dob']
        client_id = request.form['client_id']
        from models import Patient
        new_p = Patient(None, name, species, breed, dob, client_id)
        database.insert_patient(new_p)

        return redirect(url_for('index'))

    clients = database.get_all_clients()
    return render_template('patient_form.html', clients=clients, patient=None)

# Редактирование пациента
@app.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        breed = request.form['breed']
        dob = request.form['dob']

        database.update_patient(id, name, species, breed, dob)
        return redirect(url_for('index'))

    # GET запрос - загружаем данные пациента, чтобы заполнить поля
    patient_obj = database.get_patient_by_id(id)
    return render_template('patient_form.html', clients=[], patient=patient_obj)

# Удаление пациента
@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    database.delete_patient(id)
    return redirect(url_for('index'))

# Создание клиента (быстрое)
@app.route('/add_dummy_client')
def add_dummy_client():
    from models import Client
    c = Client(None, "Иван Иванов", "+79001234567")
    database.insert_client(c)
    return "Клиент Иван Иванов добавлен! <a href='/'>Назад</a>"

if __name__ == '__main__':
    app.run(debug=True)