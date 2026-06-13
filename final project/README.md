# 🏥 Diabetes Risk Predictor - Flask + SQLite Web Application

A comprehensive web application for diabetes risk assessment and health indicator tracking based on CDC's BRFSS 2015 data.

## 📋 Features

- ✅ **Comprehensive Health Assessment Form** - Collects 21+ health indicators
- ✅ **SQLite Database** - Secure data storage with proper schema
- ✅ **Dynamic Records Display** - View all registered health assessments
- ✅ **Detailed Records Management** - View, edit, and delete health records
- ✅ **Statistics & Analytics** - Aggregated health data insights with charts
- ✅ **Professional UI** - Modern, responsive design with CSS styling
- ✅ **Data Validation** - Client and server-side form validation
- ✅ **Error Handling** - Comprehensive error pages and messages

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will start at: **http://localhost:5000**

### 3. Test the System

- Navigate to **Home** page
- Go to **Register** page and submit health assessment form
- View all records on **Records** page
- Check statistics on **Statistics** page

## 📁 Project Structure

```
diabetes-risk-predictor/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── diabetes_risk_predictor.db  # SQLite database (auto-created)
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Home page
│   ├── register.html      # Health assessment form
│   ├── records.html       # All records display
│   ├── record_detail.html # Detailed record view
│   ├── statistics.html    # Analytics dashboard
│   ├── 404.html           # Page not found error
│   └── 500.html           # Server error page
└── static/
    ├── style.css          # Comprehensive styling
    └── script.js          # Client-side functionality
```

## 💾 Database Schema

### `participants` Table
```sql
CREATE TABLE participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT NOT NULL,
    phone TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### `health_records` Table
```sql
CREATE TABLE health_records (
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
);
```

## 🔗 Routes & Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/register` | GET, POST | Health assessment form |
| `/records` | GET | View all records |
| `/record/<id>` | GET | View specific record |
| `/delete/<id>` | POST | Delete a record |
| `/statistics` | GET | View analytics dashboard |
| `/api/statistics` | GET | API endpoint for stats JSON |

## 📊 Health Indicators Tracked

The application collects data on:

### Chronic Conditions
- High Blood Pressure
- High Cholesterol
- History of Stroke
- Heart Disease
- Difficulty Walking

### Lifestyle Factors
- Smoking Status
- Heavy Alcohol Use
- Physical Activity
- Fruit Consumption
- Vegetable Consumption

### Health Metrics
- BMI Category
- General Health Status
- Mental Health Days
- Physical Health Days
- Health Insurance Coverage

### Demographics
- Age Category
- Education Level
- Income Level
- Gender
- Diabetes Status (Target Variable)

## 🧪 Testing the System

### 1. Register 10+ Students
```
- Complete the registration form for each student
- Include diverse health profiles
- Test form validation
```

### 2. Verify Database
```
- Check that records are stored in SQLite
- Verify foreign key relationships
- Check data integrity
```

### 3. Test Display
```
- View all records on the records page
- Click on individual records for details
- Verify all data displays correctly
```

### 4. Test Navigation
```
- Navigate between all pages
- Test back buttons
- Verify links work correctly
```

### 5. Test Statistics
```
- Generate aggregated statistics
- View charts and visualizations
- Verify percentages calculate correctly
```

## 🎨 UI Components

- **Navigation Bar** - Fixed navigation with links to all pages
- **Alert Messages** - Success and error notifications
- **Form Components** - Text inputs, selects, checkboxes
- **Data Tables** - Sortable, responsive tables with actions
- **Statistics Cards** - Key metrics display
- **Charts** - Chart.js integration for data visualization
- **Buttons** - Primary, secondary, and danger action buttons
- **Cards** - Content organization with shadow effects

## 🔒 Security Features

- SQL Injection Prevention - Parameterized queries
- Form Validation - Both client and server-side
- Error Handling - Proper exception handling
- Database Constraints - Foreign keys and relationships

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🛠️ Technologies Used

- **Backend**: Flask 2.3.3
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js
- **Styling**: Custom CSS with gradients and animations

## 📝 Sample Test Data

To test the system, use the following sample data:

```
Student 1:
- Name: John Doe
- Age: 35
- Email: john.doe@example.com
- Phone: (123) 456-7890
- Health Indicators: Various combinations
- Diabetes Status: No Diabetes

Student 2:
- Name: Jane Smith
- Age: 45
- Email: jane.smith@example.com
- Phone: (234) 567-8901
- Health Indicators: Includes high BP and cholesterol
- Diabetes Status: Prediabetes

... (repeat for 10+ students)
```

## 🐛 Troubleshooting

### Database Not Found
- The database is auto-created on first run
- Check write permissions in project directory

### Port Already in Use
- Change the port in `app.py`: `app.run(port=5001)`

### Form Not Submitting
- Check browser console for JavaScript errors
- Verify form field names match database columns

### CSS/JS Not Loading
- Verify `static` folder exists with files
- Check file paths in templates
- Clear browser cache

## 📞 Support

For issues or questions:
1. Check the terminal output for error messages
2. Verify all dependencies are installed
3. Ensure SQLite is functioning correctly
4. Check database file permissions

## 📄 License

Educational project for learning Flask and SQLite integration.

## 🎓 Learning Objectives

This project demonstrates:
- ✓ Flask routing and request handling
- ✓ SQLite database integration
- ✓ HTML form processing
- ✓ Template rendering with Jinja2
- ✓ Database CRUD operations
- ✓ Professional UI/UX design
- ✓ Error handling and validation
- ✓ Data visualization with charts

---

**Created**: 2024
**Framework**: Flask with SQLite
**Status**: Fully Functional ✅
