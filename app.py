from flask import Flask, request, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'temporary_key'

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='database.cd8yimkomvoj.us-east-1.rds.amazonaws.com',
        user='admin',
        password='charan_2004',
        database='clone_1'
    )

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = password

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('login'))
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result and result[0] == password:
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

# Dashboard Route (after login)
@app.route('/dashboard')
def dashboard():
    course_urls = [
        'https://colnebucket.s3.us-east-1.amazonaws.com/python_code.pdf',
        'https://colnebucket.s3.us-east-1.amazonaws.com/PYTHON%2BPROGRAMMING%2BNOTES.pdf'
    ]
    
    return render_template('dashboard.html', course_urls=course_urls)

# Home Route (Landing Page)
@app.route('/')
def home():
    return render_template('home.html')

# Logout
@app.route('/logout')
def logout():
    return redirect(url_for('login.html'))

if __name__ == '__main__':
    app.run(debug=True)
