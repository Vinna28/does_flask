from flask import Flask, render_template, flash, redirect, url_for, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField

app =Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'does'
app.config['MYSQL_PASSWORD'] = '1'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MySQL
mysql = MySQL(app)


# Index
@app.route('/')
def index():
	return render_template('home.html')

# Students
@app.route('/students')
def students():
	# Create cursor
	cur = mysql.connection.cursor()

	# Get students
	result = cur.execute("SELECT * FROM students")

	students = cur.fetchall()

	if result > 0:
		return render_template('dashboard.html', students=students)
	else:
		msg = 'No Data Found'
		return render_template('dashboard.html', msg=msg)
	# Close connection
	cur.close()

class RegisterForm(Form):
	name = StringField('Name')
	birthdate = StringField('Birthdate')
	address = StringField('Address')
	gender = StringField('Gender')
	major = StringField('Major')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		birthdate = form.birthdate.data
		address = form.address.data
		gender = form.gender.data
		major = form.major.data

		# Create Cursor
		cur = mysql.connection.cursor()

		# Execute
		cur.execute("INSERT INTO students(name, birthdate, address, gender, major) VALUES(%s, %s, %s, %s, %s)",(name, birthdate, address, gender, major))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash('Student data created', 'success')

		return redirect(url_for('students'))

	return render_template('register_student.html', form=form)

# Edit Student
@app.route('/edit_student/<string:id>', methods=['GET', 'POST'])
def edit_article(id):
	# Create cursor
	cur = mysql.connection.cursor()

	# Get student by id
	result = cur.execute("SELECT * FROM students WHERE id = %s", [id])

	student = cur.fetchone()

	# Get form
	form = RegisterForm(request.form)

	# Populate article form fields
	form.name.data = student['name']
	form.birthdate.data = student['birthdate']
	form.address.data = student['address']
	form.gender.data = student['gender']
	form.major.data = student['major']

	# form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = request.form['name']
		birthdate = request.form['birthdate']
		address = request.form['address']
		gender = request.form['gender']
		major = request.form['major']

		# Create Cursor
		cur = mysql.connection.cursor()

		# Execute
		cur.execute("UPDATE students SET name=%s, birthdate=%s, address=%s, gender=%s, major=%s WHERE id = %s", (name, birthdate, address, gender, major, id))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash('Student List Updated', 'success')

		return redirect(url_for('students'))

	return render_template('edit_student.html', form=form)

# Delete Student
@app.route('/delete_student/<string:id>', methods=['POST'])
def delete_student(id):
	# Create cursor
	cur = mysql.connection.cursor()

	# Execute
	cur.execute("DELETE FROM students WHERE id = %s", [id])

	# Commit to DB
	mysql.connection.commit()

	# Close connection
	cur.close()

	flash('Student List Deleted', 'success')

	return redirect(url_for('students'))

if __name__ == "__main__":
	app.secret_key='secret123'
	app.run(debug=True)
