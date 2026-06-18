from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import sqlite3
import os
import hashlib
import hmac
import json
import secrets
import urllib.parse
import urllib.request
from functools import wraps


def load_env_file(path='.env'):
    """Load simple KEY=VALUE entries for local development."""
    if not os.path.exists(path):
        return

    with open(path, encoding='utf-8') as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'diabetes_risk_predictor_secret_2024')

# Database configuration
DATABASE = 'diabetes_risk_predictor.db'
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database and create tables"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Participants table
    c.execute(
        '''CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT NOT NULL,
            phone TEXT,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    )

    # Health records table
    c.execute(
        '''CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            FOREIGN KEY (participant_id) REFERENCES participants(id)
        )'''
    )

    # Users table (for login)
    c.execute(
        '''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    )

    # Create default admin user if missing
    default_username = os.environ.get('APP_ADMIN_USERNAME', 'admin')
    default_password = os.environ.get('APP_ADMIN_PASSWORD', 'admin123')

    c.execute('SELECT id FROM users WHERE username = ?', (default_username,))
    if c.fetchone() is None:
        salt = os.urandom(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            default_password.encode('utf-8'),
            salt,
            120000
        )
        stored = f"{salt.hex()}${pwd_hash.hex()}"
        c.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (default_username, stored)
        )

    conn.commit()
    conn.close()
    print('Database initialized successfully!')


def verify_password(stored_value: str, provided_password: str) -> bool:
    """stored_value format: salthex$hashhex"""
    try:
        salt_hex, hash_hex = stored_value.split('$', 1)
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt,
            120000
        )
        return hmac.compare_digest(pwd_hash, expected_hash)
    except Exception:
        return False


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please sign in to access this page.', 'error')
            return redirect(url_for('login', next=request.path))
        return view_func(*args, **kwargs)

    return wrapper


def get_google_redirect_uri():
    return (
        os.environ.get('GOOGLE_REDIRECT_URI')
        or os.environ.get('GOOGLE_AUTHORIZED_REDIRECT_URI')
        or url_for('google_callback', _external=True)
    )


def google_oauth_configured():
    return bool(os.environ.get('GOOGLE_CLIENT_ID') and os.environ.get('GOOGLE_CLIENT_SECRET'))


def exchange_google_code(code):
    data = urllib.parse.urlencode({
        'code': code,
        'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
        'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        'redirect_uri': get_google_redirect_uri(),
        'grant_type': 'authorization_code',
    }).encode('utf-8')

    request_data = urllib.request.Request(
        GOOGLE_TOKEN_URL,
        data=data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST'
    )

    with urllib.request.urlopen(request_data, timeout=15) as response:
        return json.loads(response.read().decode('utf-8'))


def get_google_user(access_token):
    request_data = urllib.request.Request(
        GOOGLE_USERINFO_URL,
        headers={'Authorization': f'Bearer {access_token}'}
    )

    with urllib.request.urlopen(request_data, timeout=15) as response:
        return json.loads(response.read().decode('utf-8'))


def sign_in_google_user(google_user):
    email = google_user.get('email')
    google_id = google_user.get('sub')

    if not email or not google_id:
        raise ValueError('Google account did not return an email address.')

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, username FROM users WHERE username = ?', (email,))
    user = c.fetchone()

    if user is None:
        c.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (email, f'google${google_id}')
        )
        conn.commit()
        user_id = c.lastrowid
        username = email
    else:
        user_id = user['id']
        username = user['username']

    conn.close()
    session['user_id'] = user_id
    session['username'] = username
    session['auth_provider'] = 'google'


def get_dashboard_stats():
    """Return the small stats bundle used by the admin dashboard."""
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM health_records')
    total_records = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM participants')
    total_participants = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM health_records WHERE diabetes_status = 2')
    diabetes_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM health_records WHERE diabetes_status = 1')
    prediabetes_count = c.fetchone()[0]

    c.execute(
        '''SELECT p.name, h.diabetes_status, h.submission_date, h.id as record_id
           FROM health_records h
           JOIN participants p ON p.id = h.participant_id
           ORDER BY h.submission_date DESC
           LIMIT 5'''
    )
    recent_records = c.fetchall()
    conn.close()

    return {
        'total_records': total_records,
        'total_participants': total_participants,
        'diabetes_count': diabetes_count,
        'prediabetes_count': prediabetes_count,
        'recent_records': recent_records,
    }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration form for health assessment"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            age = request.form.get('age')
            email = request.form.get('email')
            phone = request.form.get('phone')

            if not name or not email:
                flash('Name and Email are required!', 'error')
                return redirect(url_for('register'))

            conn = get_db_connection()
            c = conn.cursor()

            c.execute(
                '''INSERT INTO participants (name, age, email, phone)
                   VALUES (?, ?, ?, ?)''',
                (name, age if age else None, email, phone if phone else None)
            )
            conn.commit()
            participant_id = c.lastrowid

            # Checkboxes -> 1 if present else 0
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

            c.execute(
                '''INSERT INTO health_records (
                    participant_id, high_bp, high_chol, chol_check, bmi_category,
                    smoker, stroke, heart_disease, phys_activity, fruits, veggies,
                    heavy_alcohol, health_coverage, diff_walk, diabetes_status,
                    general_health, mental_health, physical_health, sex, age_category,
                    education_level, income_level
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    participant_id,
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
                    int(request.form.get('income_level', 0)),
                )
            )

            conn.commit()
            conn.close()

            flash(f'Health assessment for {name} recorded successfully!', 'success')
            return redirect(url_for('records'))

        except Exception as e:
            flash(f'Error submitting form: {str(e)}', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('login'))

        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            'SELECT id, username, password_hash FROM users WHERE username = ?',
            (username,)
        )
        user = c.fetchone()
        conn.close()

        if user and verify_password(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Signed in successfully!', 'success')
            next_url = request.args.get('next')
            if next_url and next_url.startswith('/') and not next_url.startswith('//'):
                return redirect(next_url)
            return redirect(url_for('dashboard'))

        flash('Invalid username or password.', 'error')
        return redirect(url_for('login'))

    return render_template(
        'login.html',
        google_login_enabled=google_oauth_configured()
    )


@app.route('/login/google')
def google_login():
    if not google_oauth_configured():
        flash('Google login is not configured.', 'error')
        return redirect(url_for('login'))

    state = secrets.token_urlsafe(32)
    session['google_oauth_state'] = state
    next_url = request.args.get('next')
    if next_url and next_url.startswith('/') and not next_url.startswith('//'):
        session['oauth_next'] = next_url

    query = urllib.parse.urlencode({
        'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
        'redirect_uri': get_google_redirect_uri(),
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'prompt': 'select_account',
    })
    return redirect(f'{GOOGLE_AUTH_URL}?{query}')


@app.route('/auth/google/callback')
def google_callback():
    if request.args.get('state') != session.pop('google_oauth_state', None):
        flash('Google sign-in could not be verified. Please try again.', 'error')
        return redirect(url_for('login'))

    code = request.args.get('code')
    if not code:
        flash('Google sign-in was cancelled or failed.', 'error')
        return redirect(url_for('login'))

    try:
        token_data = exchange_google_code(code)
        access_token = token_data.get('access_token')
        if not access_token:
            raise ValueError('Google did not return an access token.')

        google_user = get_google_user(access_token)
        sign_in_google_user(google_user)
        flash('Signed in with Google successfully!', 'success')
        next_url = session.pop('oauth_next', None)
        if next_url and next_url.startswith('/') and not next_url.startswith('//'):
            return redirect(next_url)
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'Google sign-in failed: {str(e)}', 'error')
        return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'GET':
        return render_template('logout.html')

    session.clear()
    flash('Signed out successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    try:
        return render_template('dashboard.html', stats=get_dashboard_stats())
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('dashboard.html', stats={})


@app.route('/records')
@login_required
def records():
    """Display all health records"""
    try:
        conn = get_db_connection()
        c = conn.cursor()

        c.execute(
            '''SELECT p.id, p.name, p.age, p.email, p.phone, p.registration_date,
                      h.id as record_id, h.diabetes_status, h.submission_date
               FROM participants p
               LEFT JOIN health_records h ON p.id = h.participant_id
               ORDER BY p.registration_date DESC'''
        )
        records = c.fetchall()
        conn.close()

        return render_template('records.html', records=records)
    except Exception as e:
        flash(f'Error retrieving records: {str(e)}', 'error')
        return render_template('records.html', records=[])


@app.route('/record')
def record():
    return redirect(url_for('records'))


@app.route('/record/<int:record_id>')
@login_required
def view_record(record_id):
    """View detailed record"""
    try:
        conn = get_db_connection()
        c = conn.cursor()

        c.execute(
            '''SELECT p.*, h.* FROM participants p
               JOIN health_records h ON p.id = h.participant_id
               WHERE h.id = ?''',
            (record_id,)
        )
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
@login_required
def delete_record(record_id):
    """Delete a record"""
    try:
        conn = get_db_connection()
        c = conn.cursor()

        c.execute(
            'SELECT participant_id FROM health_records WHERE id = ?',
            (record_id,)
        )
        result = c.fetchone()

        if result:
            participant_id = result[0]

            c.execute('DELETE FROM health_records WHERE id = ?', (record_id,))

            c.execute(
                'SELECT COUNT(*) FROM health_records WHERE participant_id = ?',
                (participant_id,)
            )
            count = c.fetchone()[0]

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
@login_required
def statistics():
    """Display statistics about diabetes risk"""
    try:
        conn = get_db_connection()
        c = conn.cursor()

        c.execute('SELECT COUNT(*) FROM health_records')
        total_records = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM participants')
        total_participants = c.fetchone()[0]

        c.execute(
            '''SELECT diabetes_status, COUNT(*) as count
               FROM health_records
               GROUP BY diabetes_status'''
        )
        diabetes_breakdown = c.fetchall()

        c.execute('SELECT COUNT(*) FROM health_records WHERE high_bp = 1')
        high_bp_count = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM health_records WHERE high_chol = 1')
        high_chol_count = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM health_records WHERE smoker = 1')
        smokers_count = c.fetchone()[0]

        conn.close()

        stats = {
            'total_records': total_records,
            'total_participants': total_participants,
            'diabetes_breakdown': dict(diabetes_breakdown) if diabetes_breakdown else {},
            'high_bp_count': high_bp_count,
            'high_chol_count': high_chol_count,
            'smokers_count': smokers_count,
        }

        return render_template('statistics.html', stats=stats)
    except Exception as e:
        flash(f'Error retrieving statistics: {str(e)}', 'error')
        return render_template('statistics.html', stats={})


@app.route('/api/statistics')
@login_required
def api_statistics():
    """API endpoint for statistics"""
    try:
        conn = get_db_connection()
        c = conn.cursor()

        c.execute('SELECT COUNT(*) FROM health_records')
        total = c.fetchone()[0]

        c.execute(
            'SELECT diabetes_status, COUNT(*) FROM health_records GROUP BY diabetes_status'
        )
        data = c.fetchall()

        conn.close()

        return jsonify({'total': total, 'breakdown': dict(data)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    init_db()
    app.run(
        debug=True,
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000))
    )

