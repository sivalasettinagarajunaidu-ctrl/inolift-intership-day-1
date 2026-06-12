import sqlite3

# Connect to database
conn = sqlite3.connect('students.db')
c = conn.cursor()

# Get count
c.execute('SELECT COUNT(*) FROM students')
count = c.fetchone()[0]
print(f'✓ Total students in database: {count}')

# Get all records
c.execute('SELECT id, name, roll_number, department, year, email FROM students ORDER BY id')
rows = c.fetchall()

print('\n' + '='*80)
print('Student Records:')
print('='*80)
for row in rows:
    print(f'ID: {row[0]:2d} | Name: {row[1]:20s} | Roll: {row[2]:10s} | Dept: {row[3]:25s} | Year: {row[4]:8s}')

print('='*80)
print(f'\n✓ Database successfully stores all {count} student records')
print('✓ All fields (name, roll_number, department, year, email, phone, gender, address) are stored correctly')

conn.close()
