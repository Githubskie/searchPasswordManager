import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Maak een nieuwe SQLite-database
conn = sqlite3.connect('database/password_managers.db')
c = conn.cursor()

# Maak een tabel in de database om de password manager gegevens op te slaan
c.execute('''CREATE TABLE IF NOT EXISTS password_managers
             (name TEXT, functionality_rating INT, ease_of_use_rating INT, safety_rating INT, 
             functionalities TEXT, payment_methods TEXT)''')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/engine')
def searchEngine():
    return render_template('searchEngine.html')

@app.route('/add')
def add():
    return render_template('addPasswordManager.html')

@app.route('/search_password_manager', methods=['GET', 'POST'])
def search_password_manager():
    if request.method == 'GET':
        return render_template('searchPasswordManager.html')

    if request.method == 'POST':
        functionality = request.form.get('functionality')
        usability = request.form.get('usability')
        security = request.form.get('security')
        password_exchange = request.form.get('password_exchange')
        two_factor_auth = request.form.get('two_factor_auth')
        emergency_access = request.form.get('emergency_access')
        document_vault = request.form.get('document_vault')
        custom_location = request.form.get('custom_location')
        open_source = request.form.get('open_source')
        payment_methods = request.form.getlist('payment_methods')

        conn = sqlite3.connect('database/password_managers.db')
        c = conn.cursor()

        # Use a formatted string to construct the SQL query with the IN clause and the correct number of placeholders
        query = '''SELECT name, website, price, rating
                   FROM password_managers
                   WHERE functionality=? AND usability=? AND security=?
                   AND password_exchange=? AND two_factor_auth=? AND emergency_access=?
                   AND document_vault=? AND custom_location=? AND open_source=?
                   AND payment_method IN ({})'''.format(','.join(['?'] * len(payment_methods)))

        # Pass the payment methods as a tuple to the execute method to avoid SQL injection attacks
        results = c.execute(query, (functionality, usability, security, password_exchange, two_factor_auth,
                                    emergency_access, document_vault, custom_location, open_source,
                                    *payment_methods)).fetchall()
        conn.close()

        return render_template('results.html', results=results)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Retrieve the data from the form
    value = request.form['value']
    important = request.form.getlist('important[]')
    payment_methods = request.form.getlist('payment_methods[]')

    # Construct the SQL query based on the selected criteria
    query = "SELECT * FROM password_managers WHERE "
    if value == "Functionality":
        query += "functionality_rating >= 3 "
    elif value == "Usability":
        query += "ease_of_use_rating >= 3 "
    elif value == "Security":
        query += "safety_rating >= 3 "
    if important:
        query += "AND ("
        for i in range(len(important)):
            query += "functionalities LIKE '%" + important[i] + "%'"
            if i < len(important) - 1:
                query += " OR "
        query += ") "
    if payment_methods:
        query += "AND ("
        for i in range(len(payment_methods)):
            query += "payment_methods LIKE '%" + payment_methods[i] + "%'"
            if i < len(payment_methods) - 1:
                query += " OR "
        query += ") "

    # Execute the query and retrieve the results
    conn = sqlite3.connect('database/password_managers.db')
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()
    conn.close()

    # Pass the results to the search results template
    return render_template('results.html', results=results)

@app.route('/add-password-manager', methods=['POST'])
def add_password_manager():
    name = request.form['name']
    functionality_rating = request.form['functionality_rating']
    ease_of_use_rating = request.form['ease_of_use_rating']
    safety_rating = request.form['safety_rating']
    password_exchange = request.form.get('password_exchange', 0, type=int)
    two_factor_auth = request.form.get('two_factor_auth', 0, type=int)
    emergency_access = request.form.get('emergency_access', 0, type=int)
    document_vault = request.form.get('document_vault', 0, type=int)
    custom_location = request.form.get('custom_location', 0, type=int)
    open_source = request.form.get('open_source', 0, type=int)
    direct_debit = request.form.get('direct_debit', 0, type=int)
    credit_card = request.form.get('credit_card', 0, type=int)
    ideal = request.form.get('ideal', 0, type=int)
    paypal = request.form.get('paypal', 0, type=int)

    functionalities = ','.join([str(password_exchange), str(two_factor_auth), str(emergency_access), str(document_vault), str(custom_location), str(open_source)])
    payment_methods = ','.join([str(direct_debit), str(credit_card), str(ideal), str(paypal)])

    conn = sqlite3.connect('database/password_managers.db')
    c = conn.cursor()

    # Voeg de gegevens toe aan de database
    c.execute("INSERT INTO password_managers (name, functionality_rating, ease_of_use_rating, safety_rating, functionalities, payment_methods) VALUES (?, ?, ?, ?, ?, ?)",
              (name, functionality_rating, ease_of_use_rating, safety_rating, functionalities, payment_methods))
    conn.commit()
    conn.close()

    message = f"{name} is added to the database!"
    return render_template('addPasswordManager.html', message=message)

@app.route('/delete-password-manager')
def delete_password_manager():
    conn = sqlite3.connect('database/password_managers.db')
    c = conn.cursor()
    c.execute("SELECT name FROM password_managers")
    password_managers = c.fetchall()
    conn.close()

    return render_template('deletePasswordManager.html', password_managers=password_managers)

@app.route('/delete/<name>', methods=['POST', 'GET'])
def delete(name):
    if request.method == 'POST':
        conn = sqlite3.connect('database/password_managers.db')
        c = conn.cursor()
        c.execute("DELETE FROM password_managers WHERE name=?", (name,))
        conn.commit()
        conn.close()

        return redirect(url_for('delete_password_manager'))
    return render_template('confirmDelete.html', name=name)


@app.route('/search')
def search():
    return render_template('searchPasswordManager.html')


if __name__ == '__main__':
    try:
        app.run(port=5001)
    finally:
        conn.close()
