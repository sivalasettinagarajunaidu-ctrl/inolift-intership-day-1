from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database configuration
DATABASE = 'students.db'

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create tables"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  roll_number TEXT NOT NULL UNIQUE,
                  department TEXT NOT NULL,
                  year TEXT NOT NULL,
                  email TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  gender TEXT NOT NULL,
                  address TEXT NOT NULL,
                  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration form and processing"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            roll_number = request.form.get('roll_number')
            department = request.form.get('department')
            year = request.form.get('year')
            email = request.form.get('email')
            phone = request.form.get('phone')
            gender = request.form.get('gender')
            address = request.form.get('address')
            
            # Validate form data
            if not all([name, roll_number, department, year, email, phone, gender, address]):
                flash('All fields are required!', 'error')
                return redirect(url_for('register'))
            
            # Insert into database
            conn = get_db_connection()
            c = conn.cursor()
            
            c.execute('''INSERT INTO students 
                        (name, roll_number, department, year, email, phone, gender, address)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                     (name, roll_number, department, year, email, phone, gender, address))
            
            conn.commit()
            conn.close()
            
            flash(f'Student {name} registered successfully!', 'success')
            return redirect(url_for('register'))
            
        except sqlite3.IntegrityError:
            flash('Roll number already exists! Please use a unique roll number.', 'error')
            return redirect(url_for('register'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/students')
def students():
    """Display all registered students"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM students ORDER BY registration_date DESC')
        students_list = c.fetchall()
        conn.close()
        
        return render_template('students.html', students=students_list)
    except Exception as e:
        flash(f'Error retrieving students: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """Delete a student record"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        flash('Student record deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'error')
    
    return redirect(url_for('students'))

@app.route('/api/students')
def api_students():
    """API endpoint to get students data"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM students ORDER BY registration_date DESC')
        students_list = c.fetchall()
        conn.close()
        
        # Convert to list of dicts
        students_data = [dict(student) for student in students_list]
        return {'students': students_data, 'count': len(students_data)}
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
