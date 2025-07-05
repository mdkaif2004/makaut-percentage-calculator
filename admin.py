from flask import Blueprint, render_template, request, redirect, session, send_file
import csv
import os

admin_bp = Blueprint('admin_bp', __name__)

DATA_FILE = 'users.csv'

@admin_bp.route('/admin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'mdkaif2004' and password == 'Lgb4TY466!!oir0YY*B*B()':
            session['admin'] = True
            session['action_message'] = 'Login Successful!'
            return redirect('/dashboard')
        return render_template('admin.html', error='Invalid credentials')
    return render_template('admin.html')

@admin_bp.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    users = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline='') as file:
            reader = csv.DictReader(file)
            users = list(reader)

    action_message = session.pop('action_message', None)
    return render_template('dashboard.html', users=users, action_message=action_message)


@admin_bp.route('/download')
def download():
    if not session.get('admin'):
        return redirect('/admin')
    return send_file(DATA_FILE, as_attachment=True)

@admin_bp.route('/delete/<int:index>')
def delete(index):
    if not session.get('admin'):
        return redirect('/admin')

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline='') as f:
            reader = list(csv.reader(f))

        # Ensure file has rows and index is valid
        if len(reader) > 1 and 1 <= index + 1 < len(reader):  # +1 for header
            del reader[index + 1]  # remove correct row

            with open(DATA_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(reader)

            session['action_message'] = 'Deleted successfully.'
        else:
            session['action_message'] = 'Invalid record to delete.'
    else:
        session['action_message'] = 'No data found to delete.'

    return redirect('/dashboard')
