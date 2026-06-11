from flask import Flask, render_template

app = Flask(__name__)


students = [
    {"roll_no": "101", "name": "Arjun", "department": "IT", "year": "3"},
    {"roll_no": "102", "name": "Priya", "department": "CSE", "year": "2"},
    {"roll_no": "103", "name": "Rahul", "department": "ECE", "year": "4"},
    {"roll_no": "104", "name": "Meena", "department": "EEE", "year": "1"},
    {"roll_no": "105", "name": "Karthik", "department": "MECH", "year": "3"},
    {"roll_no": "106", "name": "Sneha", "department": "CIVIL", "year": "2"},
    {"roll_no": "107", "name": "Vikram", "department": "AIML", "year": "1"},
    {"roll_no": "108", "name": "Divya", "department": "IT", "year": "4"},
    {"roll_no": "109", "name": "Sanjay", "department": "CSE", "year": "3"},
    {"roll_no": "110", "name": "Anitha", "department": "ECE", "year": "2"},
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/students")
def student_records():
    return render_template("students.html", students=students)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
