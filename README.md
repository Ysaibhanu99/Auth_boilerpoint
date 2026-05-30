# Auth Boilerplate 🔐

A simple authentication system built with Flask and PostgreSQL (Neon). This was my Day 2 foundation project — the idea is to have a reusable login/register system that I can copy-paste into future projects instead of building it from scratch every time.

## What it does

- Register with username, email and password
- Login with username and password
- Dashboard page that only logged-in users can see
- Logout functionality
- Passwords are hashed (not stored in plain text!)
- Flash messages for errors and success

## Tech Stack

- **Backend:** Python + Flask
- **Database:** PostgreSQL (hosted on Neon)
- **Password Hashing:** werkzeug.security
- **Sessions:** Flask built-in sessions

## How to run it

1. Clone the repo
```bash
git clone https://github.com/Ysaibhanu99/Auth_boilerpoint.git
cd Auth_boilerpoint
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root folder with your own credentials
```
DATABASE_URL=your_neon_database_url_here
SECRET_KEY=any-random-string
```

4. Create the users table in your Neon SQL editor
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

5. Run the app
```bash
python app.py
```

6. Open `http://127.0.0.1:5000` in your browser

## Project Structure

```
Auth_BoilerPoint/
├── app.py              # All the routes (register, login, dashboard, logout)
├── db.py               # Database connection function
├── templates/
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
├── static/
│   └── style.css
├── .env                # Database URL and secret key (not pushed to git)
├── requirements.txt
└── .gitignore
```

## Routes

| Method | Route | What it does |
|--------|-------|-------------|
| GET | `/register` | Shows registration form |
| POST | `/register` | Creates new user account |
| GET | `/login` | Shows login form |
| POST | `/login` | Logs in the user |
| GET | `/dashboard` | Protected page — only for logged in users |
| GET | `/logout` | Logs out and clears session |

## What I learned

- How to hash passwords using `generate_password_hash` and `check_password_hash`
- How Flask sessions work (setting user data on login, clearing on logout)
- How to protect routes by checking if `user_id` is in the session
- Handling duplicate users with PostgreSQL UNIQUE constraints
- Using flash messages to show errors/success to the user

---

*Built as part of Foundation Block 2 — Authentication*
