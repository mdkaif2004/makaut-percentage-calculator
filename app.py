from flask import Flask, render_template, request, redirect, flash, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'

DATA_FILE = 'users.csv'

def cgpa_to_percentage(cgpa):
    base_cgpa = 6.25
    base_percentage = 55

    if cgpa > 10:
        return "❌ Error: CGPA cannot be greater than 10"
    elif cgpa < 0:
        return "❌ Error: CGPA cannot be negative"

    if cgpa < base_cgpa:
        percentage = max(0, base_percentage - ((base_cgpa - cgpa) * 10))
    else:
        percentage = (cgpa - base_cgpa) * 10 + base_percentage

    return round(percentage, 2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/developer')
def developer():
    return render_template('developer.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        location = request.form.get('location')
        try:
            cgpa = float(request.form.get('cgpa'))
            percentage = cgpa_to_percentage(cgpa)
            if isinstance(percentage, str):
                flash(percentage, 'error')
                return redirect(url_for('home'))

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            file_exists = os.path.isfile(DATA_FILE)
            with open(DATA_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(['Timestamp', 'Name', 'Email', 'Location', 'CGPA', 'Percentage'])
                writer.writerow([timestamp, name, email, location, cgpa, percentage])

            flash(f"CGPA: {cgpa} | Percentage: {percentage:.2f}%", "success")
            return redirect(url_for('home'))

        except ValueError:
            flash("❌ Invalid CGPA input!", 'error')
            return redirect(url_for('home'))
