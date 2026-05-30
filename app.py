from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# ──────────────────────────────────────────────
#  Home — redirect to login
# ──────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('login'))


# ──────────────────────────────────────────────
#  Register
# ──────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash)
            )
            conn.commit()
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception:
            conn.rollback()
            flash('Username or email already exists.', 'error')
            return redirect(url_for('register'))
        finally:
            cur.close()
            conn.close()

    return render_template('register.html')


# ──────────────────────────────────────────────
#  Login
# ──────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, username, email, password_hash FROM users WHERE username = %s", (username,))
            user = cur.fetchone()

            if user and check_password_hash(user[3], password):
                # Set session
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['email'] = user[2]
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'error')
                return redirect(url_for('login'))
        finally:
            cur.close()
            conn.close()

    return render_template('login.html')


# ──────────────────────────────────────────────
#  Dashboard (protected)
# ──────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    # Protected route — redirect if not logged in
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('login'))

    return render_template('dashboard.html',
                           username=session['username'],
                           email=session['email'])


# ──────────────────────────────────────────────
#  Logout
# ──────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


# ──────────────────────────────────────────────
#  Run
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)