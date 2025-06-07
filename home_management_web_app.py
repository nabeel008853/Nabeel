
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DB_PATH = 'home_management_web.db'

# Initialize database
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    if name and email and phone:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
                conn.commit()
                flash('User added successfully!', 'success')
        except sqlite3.IntegrityError:
            flash('Email already exists.', 'error')
    else:
        flash('All fields are required.', 'warning')

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
