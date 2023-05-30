import sqlite3

# Maak een nieuwe SQLite-database
conn = sqlite3.connect('database/password_managers.db')

# Maak een tabel in de database om de password manager gegevens op te slaan
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS password_managers
             (name TEXT, functionality_rating INT, ease_of_use_rating INT, safety_rating INT, 
             password_exchange BOOLEAN, two_factor_auth BOOLEAN, emergency_access BOOLEAN, 
             document_vault BOOLEAN, custom_location BOOLEAN, open_source BOOLEAN, 
             direct_debit BOOLEAN, credit_card BOOLEAN, ideal BOOLEAN, paypal BOOLEAN)''')

# Sluit de databaseconnectie
conn.close()
