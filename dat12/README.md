# Student Registration System - Day 12 Task

A complete web application for managing student registrations using Flask and SQLite.

## Project Structure

```
dat12/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── students.db           # SQLite database (created on first run)
├── templates/
│   ├── base.html         # Base template for all pages
│   ├── index.html        # Home page
│   ├── register.html     # Student registration form
│   └── students.html     # Display all registered students
└── static/
    └── style.css         # CSS styling
```

## Features

✅ **Database Integration**
- SQLite database with student records table
- Automatic database initialization
- Data validation and unique constraints

✅ **Student Registration Form**
- Collects: Name, Roll Number, Department, Year, Email, Phone, Gender, Address
- Form validation on both client and server side
- Success/Error messages

✅ **Data Management**
- Insert student records via POST requests
- Retrieve and display all records dynamically
- Delete records functionality
- Timestamps for each registration

✅ **User Interface**
- Responsive design
- Professional styling
- Navigation between pages
- Statistics dashboard

✅ **Backend Routes**
- `/` - Home page
- `/register` - Registration form (GET/POST)
- `/students` - View all students
- `/delete/<id>` - Delete student record
- `/api/students` - JSON API endpoint

## Installation & Setup

### 1. Clone/Extract Project
```bash
cd dat12
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

The application will start on: `http://localhost:5000`

## Usage

### Register a Student
1. Navigate to "Register Student" page
2. Fill in all required fields:
   - Student Name
   - Roll Number (must be unique)
   - Department
   - Year
   - Email
   - Phone Number
   - Gender
   - Address
3. Click "Register Student" button
4. Success message will appear

### View All Students
1. Click "View Students" page
2. See all registered students in a formatted table
3. Click "Delete" to remove any record

### Database
- Database file: `students.db` (created automatically)
- Table: `students`
- All data is persisted in SQLite

## Database Schema

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_number TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    year TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    gender TEXT NOT NULL,
    address TEXT NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Testing Checklist

- [x] Database created successfully
- [x] Flask connected to SQLite
- [x] Registration form working
- [x] Data stored in database
- [x] Students list displays data
- [x] Form submission successful
- [x] Navigation between pages working
- [x] Delete functionality working
- [x] Error handling implemented
- [x] Responsive design

## Requirements Met

✅ Database Integration
- SQLite database created
- Students table with all fields
- Successful database connection

✅ Form Integration
- All required fields collected
- Form data processing

✅ Data Storage
- POST request handling
- SQLite record insertion
- Success messages

✅ Students List Page
- Dynamic data retrieval
- HTML table display
- Flask templates

✅ Flask Backend
- Database connection
- Table creation
- Data insertion
- Data retrieval
- Route handling
- Form processing

## Technologies Used

- **Backend:** Flask (Python web framework)
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3
- **Server:** Flask development server

## Next Steps

This application can be expanded with:
- User authentication
- Search and filter functionality
- Export to CSV/Excel
- Advanced analytics
- Email notifications
- Admin dashboard

## Notes

- Run this application only on your local machine for development
- For production, use a production WSGI server like Gunicorn
- Enable HTTPS in production
- Use environment variables for sensitive data

---

**Day 12 Task** - Student Registration System using Flask + SQLite
