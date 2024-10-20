import os
from flask import Flask, render_template, request, redirect, url_for, session

# Get the absolute path of the directory containing this file
basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Flask application instance with the explicit template folder
app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))
app.secret_key = 'your_secret_key'  # Set your secret key here

# Dummy data for students
students = {
    
  "Aditya": "Aditya Rathod",
  "Atique": "Atique Shaikh",
  "Arcita": "Archita Tiwari",
  "Gauri": "Gauri Korde",
  "Harsh": "Harsh Sonar",
  "Janhavi": "Janhavi Chaturvedi",
  "Prarthana": "Prarthana Jaweri",
  "Priyank": "Priyank Rana",
  "Rahul": "Rahul Shirsat",
  "Siddesh": "Siddesh Gadhari",
  "Shreyash": "Shreyash Gawande",
  "Shreya": "Shreya Apar",
  "Shubham": "Shubham Koli",
  "Vedant": "Vedant Sawant",
  "Vishwakarma": "Ayush Awdheshkumar Vishwakarma"
}

# Store attendance data temporarily for summary
attendance_data = {}

# Route for marking attendance
@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        class_name = request.form.get('class')
        department = request.form.get('department')
        subject = request.form.get('subject')
        total_students = request.form.get('total_students')
        year = request.form.get('year')  # Get the selected year

        # Store attendance for each student
        attendance = {}
        for student_key, student_name in students.items():
            attendance_status = request.form.get(f'attendance_{student_key}', 'Absent')  # Default to Absent
            attendance[student_name] = attendance_status

        # Store the attendance and additional details for the summary page
        global attendance_data
        attendance_data = {
            'class': class_name,
            'department': department,
            'subject': subject,
            'total_students': total_students,
            'year': year,  # Store the year
            'attendance': attendance
        }

        # Redirect to the summary page
        return redirect(url_for('attendance_summary'))

    return render_template('mark_attendance.html', students=students)

# Route to display attendance summary
@app.route('/attendance_summary')
def attendance_summary():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('attendance_summary.html', attendance_data=attendance_data)

# Route for Login Page
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Dummy login validation, you can improve it
        if username == "admin" and password == "admin123":
            session['username'] = username  # Store username in session
            return redirect(url_for('mark_attendance'))
        else:
            return "Login Failed! Please check your username and password."

    return render_template('login.html')

# Forgot Password route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email_or_username = request.form['email']
        # Simulated password reset process (you can add actual logic here)
        if email_or_username in students:  # Assuming the student names as usernames
            return redirect(url_for('reset_password', username=email_or_username))
        else:
            return "User not found. Please try again."
    
    return render_template('forgot_password.html')

# Reset Password route
@app.route('/reset-password/<username>', methods=['GET', 'POST'])
def reset_password(username):
    if request.method == 'POST':
        new_password = request.form['new_password']
        students[username] = new_password  # Update the user's password
        return redirect(url_for('login'))  # Redirect back to login after password reset
    
    return render_template('reset_password.html', username=username)

# Route for Logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))  # Redirect to login page after logout

if __name__ == '__main__':
    app.run(debug=True)
