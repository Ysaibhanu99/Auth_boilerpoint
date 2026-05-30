# PRD — Auth Boilerplate (Day 2 Foundation Project)

---

## 1. Purpose

Build a reusable Flask + Neon (PostgreSQL) authentication system covering
Register, Login, Session, Protected Route, and Logout.  
**Core goal:** A working auth module you will copy-paste into every future
project — including Smart Attendance — instead of rebuilding it from scratch.

---

## 2. Success Criteria

By end of Day 2, you should be able to say:

> "I can register a user with a hashed password, log in with session creation,
> block access to protected pages for logged-out users, and log out cleanly —
> and I understand every line."

---

## 3. Tech Stack

| Layer         | Technology                                   |
|---------------|----------------------------------------------|
| Backend       | Python + Flask                               |
| Database      | PostgreSQL (Neon)                            |
| DB Driver     | psycopg2-binary                              |
| Password Hash | werkzeug.security (ships with Flask, no extra install) |
| Sessions      | Flask built-in sessions (server-side via secret key) |
| Frontend      | Plain HTML + minimal CSS                     |

---

## 4. Database Schema

**Table: `users`**

```sql
CREATE TABLE users (
    id           SERIAL PRIMARY KEY,
    username     VARCHAR(50)  UNIQUE NOT NULL,
    email        VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT        NOT NULL,
    created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);
```

No other tables. No relations. Just this.

---

## 5. Routes

| Method | Route       | What it does                                         |
|--------|-------------|------------------------------------------------------|
| GET    | `/register` | Show registration form                               |
| POST   | `/register` | Validate input, hash password, insert user, redirect to `/login` |
| GET    | `/login`    | Show login form                                      |
| POST   | `/login`    | Verify credentials, set session, redirect to `/dashboard` |
| GET    | `/dashboard`| Protected page — redirect to `/login` if not logged in |
| GET    | `/logout`   | Clear session, redirect to `/login`                  |

6 routes total. Nothing else.

---

## 6. Pages / UI

### `register.html`
- Fields: Username, Email, Password, Confirm Password
- Submit button: "Register"
- Link at bottom: "Already have an account? Login"
- Show flash message if username/email already exists

### `login.html`
- Fields: Email, Password
- Submit button: "Login"
- Link at bottom: "Don't have an account? Register"
- Show flash message if credentials are wrong

### `dashboard.html`
- Shows: "Welcome, {username}" 
- Shows: "You are logged in as {email}"
- One button: "Logout"
- Nothing else — this page just proves the session works

**No styling ambition. Ugly is fine. Working is everything.**

---

## 7. Core Logic to Understand

### Password Hashing
```python
from werkzeug.security import generate_password_hash, check_password_hash

# On register — never store plain text
password_hash = generate_password_hash(password)

# On login — compare against stored hash
check_password_hash(stored_hash, entered_password)  # returns True/False
```

### Session — set and clear
```python
from flask import session

# On successful login
session['user_id'] = user['id']
session['username'] = user['username']

# On logout
session.clear()
```

### Protecting a route
```python
# At the top of any protected route — copy this pattern everywhere
if 'user_id' not in session:
    return redirect(url_for('login'))
```

These 3 patterns are what you're actually learning today.

---

## 8. Folder Structure

```
auth-boilerplate/
│
├── app.py               ← All routes
├── db.py                ← Connection function (same pattern as Expense Tracker)
│
├── templates/
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
│
├── static/
│   └── style.css        ← Optional, minimal only
│
├── .env                 ← DATABASE_URL + SECRET_KEY
├── requirements.txt
└── .gitignore
```

### `.env` file needs TWO variables today:
```
DATABASE_URL=postgresql://...your neon string...
SECRET_KEY=any-random-string-you-make-up
```

Flask sessions need a `SECRET_KEY` to sign cookies — this is new from Day 1.

---

## 9. Build Order (follow exactly)

```
Step 1 → Create users table in Neon SQL editor. Verify it exists.
Step 2 → Set up folder, copy db.py from Expense Tracker, update if needed.
Step 3 → Set SECRET_KEY in .env and load it in app.py.
Step 4 → Write GET /register + register.html form. Just the page, no logic yet.
Step 5 → Write POST /register — hash password, insert into DB, redirect to login.
         Test: register a user, check Neon table to confirm row exists with a hashed password.
Step 6 → Write GET /login + login.html form.
Step 7 → Write POST /login — query DB, check hash, set session, redirect to dashboard.
         Test: login with correct credentials, login with wrong credentials.
Step 8 → Write GET /dashboard — session check at top, show username from session.
         Test: access /dashboard logged in (works), access /dashboard logged out (redirects).
Step 9 → Write GET /logout — clear session, redirect to login.
         Test: login → dashboard → logout → try /dashboard again (should redirect).
Step 10 → Full end-to-end test: Register → Login → Dashboard → Logout → Try Dashboard → Blocked.
```

---

## 10. Strictly Out of Scope

Do not add any of these. Write them down for future projects instead.

- ❌ Forgot password / password reset
- ❌ Email verification
- ❌ OAuth (Google/GitHub login)
- ❌ Remember me / persistent sessions
- ❌ Role-based access (admin vs user) — that's Day 3
- ❌ Profile edit page
- ❌ Account deletion
- ❌ Any dashboard content beyond "welcome, {username}"
- ❌ Deployment (optional only if you finish early)

---

## 11. What This Teaches You

| Concept                        | Where you use it in future projects         |
|-------------------------------|----------------------------------------------|
| Password hashing (werkzeug)    | Every app with user accounts                |
| Flask SECRET_KEY               | Required for sessions in every Flask app    |
| Session set on login           | Smart Attendance — teacher/student login    |
| Session clear on logout        | Universal logout pattern                    |
| Protected route pattern        | Every page that requires login              |
| Flash messages for auth errors | Universal user feedback pattern             |
| Duplicate user check (UNIQUE)  | Any registration form ever                  |

---

## 12. The Real Deliverable

At the end of Day 2, you don't just have an auth system.  
You have a **template** — `auth-boilerplate/` — that you can drop into any
future project and have working login in under 30 minutes.

This is the most reused code in all of web development.

---

*PRD version: 1.0 | Project: Foundation Block 2 — Authentication*
