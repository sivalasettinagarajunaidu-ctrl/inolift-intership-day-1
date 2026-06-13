from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'diabetes_risk_predictor_secret_2024'

# Database configuration
DATABASE = 'diabetes_risk_predictor.db'

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create tables"""
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        # Create Students/Participants table
        c.execute('''CREATE TABLE IF NOT EXISTS participants
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     age INTEGER,
                     email TEXT NOT NULL,
                     phone TEXT,
                     registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        # Create Health Indicators table
        c.execute('''CREATE TABLE IF NOT EXISTS health_records
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     participant_id INTEGER NOT NULL,
                     high_bp INTEGER,
                     high_chol INTEGER,
                     chol_check INTEGER,
                     bmi_category INTEGER,
                     smoker INTEGER,
                     stroke INTEGER,
                     heart_disease INTEGER,
                     phys_activity INTEGER,
                     fruits INTEGER,
                     veggies INTEGER,
                     heavy_alcohol INTEGER,
                     health_coverage INTEGER,
                     diff_walk INTEGER,
                     diabetes_status INTEGER,
                     general_health INTEGER,
                     mental_health INTEGER,
                     physical_health INTEGER,
                     sex INTEGER,
                     age_category INTEGER,
                     education_level INTEGER,
                     income_level INTEGER,
                     submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     FOREIGN KEY (participant_id) REFERENCES participants(id))''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration form for health assessment"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            age = request.form.get('age')
            email = request.form.get('email')
            phone = request.form.get('phone')
            
            # Validate required fields
            if not name or not email:
                flash('Name and Email are required!', 'error')
                return redirect(url_for('register'))
            
            conn = get_db_connection()
            c = conn.cursor()
            
            # Insert participant record
            c.execute('''INSERT INTO participants (name, age, email, phone)
                        VALUES (?, ?, ?, ?)''',
                     (name, age if age else None, email, phone if phone else None))
            conn.commit()
            participant_id = c.lastrowid
            
            # Insert health indicators
            # For checkboxes, we need to check if they were sent (1 if checked, 0 if unchecked/not sent)
            high_bp = 1 if request.form.get('high_bp') else 0
            high_chol = 1 if request.form.get('high_chol') else 0
            chol_check = 1 if request.form.get('chol_check') else 0
            smoker = 1 if request.form.get('smoker') else 0
            stroke = 1 if request.form.get('stroke') else 0
            heart_disease = 1 if request.form.get('heart_disease') else 0
            phys_activity = 1 if request.form.get('phys_activity') else 0
            fruits = 1 if request.form.get('fruits') else 0
            veggies = 1 if request.form.get('veggies') else 0
            heavy_alcohol = 1 if request.form.get('heavy_alcohol') else 0
            health_coverage = 1 if request.form.get('health_coverage') else 0
            diff_walk = 1 if request.form.get('diff_walk') else 0
            
            c.execute('''INSERT INTO health_records 
                        (participant_id, high_bp, high_chol, chol_check, bmi_category,
                         smoker, stroke, heart_disease, phys_activity, fruits, veggies,
                         heavy_alcohol, health_coverage, diff_walk, diabetes_status,
                         general_health, mental_health, physical_health, sex, age_category,
                         education_level, income_level)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (participant_id,
                      high_bp,
                      high_chol,
                      chol_check,
                      int(request.form.get('bmi_category', 0)),
                      smoker,
                      stroke,
                      heart_disease,
                      phys_activity,
                      fruits,
                      veggies,
                      heavy_alcohol,
                      health_coverage,
                      diff_walk,
                      int(request.form.get('diabetes_status', 0)),
                      int(request.form.get('general_health', 0)),
                      int(request.form.get('mental_health', 0) or 0),
                      int(request.form.get('physical_health', 0) or 0),
                      int(request.form.get('sex', 0)),
                      int(request.form.get('age_category', 0)),
                      int(request.form.get('education_level', 0)),
                      int(request.form.get('income_level', 0))))
            
            conn.commit()
            conn.close()
            
            flash(f'Health assessment for {name} recorded successfully!', 'success')
            return redirect(url_for('records'))
            
        except Exception as e:
            flash(f'Error submitting form: {str(e)}', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/records')
def records():
    """Display all health records"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Get all records with participant info
        c.execute('''SELECT p.id, p.name, p.age, p.email, p.phone, p.registration_date,
                            h.id as record_id, h.diabetes_status, h.submission_date
                     FROM participants p
                     LEFT JOIN health_records h ON p.id = h.participant_id
                     ORDER BY p.registration_date DESC''')
        records = c.fetchall()
        conn.close()
        
        return render_template('records.html', records=records)
    except Exception as e:
        flash(f'Error retrieving records: {str(e)}', 'error')
        return render_template('records.html', records=[])

@app.route('/record')
def record():
    """Redirect the singular records URL to the records list."""
    return redirect(url_for('records'))

@app.route('/record/<int:record_id>')
def view_record(record_id):
    """View detailed record"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('''SELECT p.*, h.* FROM participants p
                     JOIN health_records h ON p.id = h.participant_id
                     WHERE h.id = ?''', (record_id,))
        record = c.fetchone()
        conn.close()
        
        if record is None:
            flash('Record not found!', 'error')
            return redirect(url_for('records'))
        
        return render_template('record_detail.html', record=record)
    except Exception as e:
        flash(f'Error retrieving record: {str(e)}', 'error')
        return redirect(url_for('records'))

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    """Delete a record"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Get participant_id first
        c.execute('SELECT participant_id FROM health_records WHERE id = ?', (record_id,))
        result = c.fetchone()
        
        if result:
            participant_id = result[0]
            
            # Delete health record
            c.execute('DELETE FROM health_records WHERE id = ?', (record_id,))
            
            # Check if participant has other records
            c.execute('SELECT COUNT(*) FROM health_records WHERE participant_id = ?', (participant_id,))
            count = c.fetchone()[0]
            
            # If no other records, delete participant
            if count == 0:
                c.execute('DELETE FROM participants WHERE id = ?', (participant_id,))
            
            conn.commit()
            flash('Record deleted successfully!', 'success')
        else:
            flash('Record not found!', 'error')
        
        conn.close()
    except Exception as e:
        flash(f'Error deleting record: {str(e)}', 'error')
    
    return redirect(url_for('records'))

@app.route('/statistics')
def statistics():
    """Display statistics about diabetes risk"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Get total records
        c.execute('SELECT COUNT(*) FROM health_records')
        total_records = c.fetchone()[0]
        
        # Get total participants
        c.execute('SELECT COUNT(*) FROM participants')
        total_participants = c.fetchone()[0]
        
        # Get diabetes status breakdown
        c.execute('''SELECT diabetes_status, COUNT(*) as count
                     FROM health_records
                     GROUP BY diabetes_status''')
        diabetes_breakdown = c.fetchall()
        
        # Get high BP count
        c.execute('SELECT COUNT(*) FROM health_records WHERE high_bp = 1')
        high_bp_count = c.fetchone()[0]
        
        # Get high cholesterol count
        c.execute('SELECT COUNT(*) FROM health_records WHERE high_chol = 1')
        high_chol_count = c.fetchone()[0]
        
        # Get smokers count
        c.execute('SELECT COUNT(*) FROM health_records WHERE smoker = 1')
        smokers_count = c.fetchone()[0]
        
        conn.close()
        
        stats = {
            'total_records': total_records,
            'total_participants': total_participants,
            'diabetes_breakdown': dict(diabetes_breakdown) if diabetes_breakdown else {},
            'high_bp_count': high_bp_count,
            'high_chol_count': high_chol_count,
            'smokers_count': smokers_count
        }
        
        return render_template('statistics.html', stats=stats)
    except Exception as e:
        flash(f'Error retrieving statistics: {str(e)}', 'error')
        return render_template('statistics.html', stats={})

@app.route('/api/statistics')
def api_statistics():
    """API endpoint for statistics"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) FROM health_records')
        total = c.fetchone()[0]
        
        c.execute('SELECT diabetes_status, COUNT(*) FROM health_records GROUP BY diabetes_status')
        data = c.fetchall()
        
        conn.close()
        
        return jsonify({
            'total': total,
            'breakdown': dict(data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
