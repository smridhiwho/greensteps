# greensteps_app.py

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import datetime
import streamlit_authenticator as stauth

# ---------------- Database Setup ----------------
conn = sqlite3.connect('greensteps.db', check_same_thread=False)
c = conn.cursor()

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    habit TEXT,
    notes TEXT,
    eco_points REAL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()

# ---------------- Eco Habits & Points ----------------
eco_habits = {
    "Carpooling 🚗": 1.5,
    "Reused Container ♻️": 1.0,
    "Skipped Meat 🍃": 2.0,
    "Used Public Transport 🚲": 1.5,
    "No-Plastic Day 🛍️": 2.5,
    "Others (Custom) 📝": 1.0
}

# ---------------- Authentication ----------------
def register_user(email, password):
    try:
        c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(email, password):
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    return c.fetchone()

def get_user_id(email):
    c.execute('SELECT id FROM users WHERE email = ?', (email,))
    return c.fetchone()[0]

# ---------------- App UI ----------------
st.title("🌱 GreenSteps: Eco-Habit Tracker")

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# Login/Registration
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if menu == "Register":
    st.sidebar.subheader("Create Account")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Register"):
        if register_user(email, password):
            st.sidebar.success("Registered successfully! Please login.")
        else:
            st.sidebar.error("User already exists.")

if menu == "Login":
    st.sidebar.subheader("Login")
    email = st.sidebar.text_input("Email", key='login_email')
    password = st.sidebar.text_input("Password", type="password", key='login_pass')
    if st.sidebar.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.sidebar.success(f"Welcome {email}!")
        else:
            st.sidebar.error("Invalid credentials.")

# After login
if st.session_state.logged_in:
    st.success(f"Logged in as {st.session_state.user_email}")
    st.subheader("✅ Log Today's Eco-Actions")
    today = datetime.date.today().isoformat()
    user_id = get_user_id(st.session_state.user_email)

    # Check if already submitted today
    c.execute('SELECT * FROM logs WHERE user_id = ? AND date = ?', (user_id, today))
    already_logged = c.fetchone()

    if already_logged:
        st.info("You've already submitted for today. Come back tomorrow!")
    else:
        selected_habits = st.multiselect("Select habits you completed today:", list(eco_habits.keys()))
        notes = st.text_area("Any custom notes?")
        if st.button("Submit Today's Log"):
            for habit in selected_habits:
                points = eco_habits[habit]
                c.execute('INSERT INTO logs (user_id, date, habit, notes, eco_points) VALUES (?, ?, ?, ?, ?)', 
                          (user_id, today, habit, notes, points))
            conn.commit()
            st.success("Thanks for logging your green actions! 🌎")

    st.subheader("📊 Your Eco Impact")
    logs_df = pd.read_sql_query('SELECT date, habit, eco_points FROM logs WHERE user_id = ?', conn, params=(user_id,))

    if not logs_df.empty:
        points_per_day = logs_df.groupby('date')['eco_points'].sum().reset_index()
        fig = px.bar(points_per_day, x='date', y='eco_points', title="Daily Eco-Points")
        st.plotly_chart(fig)

        total_points = points_per_day['eco_points'].sum()
        st.metric("Total Eco-Points Earned", total_points)

        # Streaks (Simple version)
        days_logged = points_per_day['date'].nunique()
        st.metric("Days Contributed", days_logged)
        if days_logged >= 7:
            st.success("🏅 Badge Earned: 7-Day Streak!")
        if days_logged >= 30:
            st.success("🏆 Badge Earned: 30-Day Eco-Warrior!")

    st.subheader("🌍 Global Community Impact")
    global_logs = pd.read_sql_query('SELECT date, eco_points FROM logs', conn)
    if not global_logs.empty:
        global_points = global_logs.groupby('date')['eco_points'].sum().reset_index()
        fig2 = px.line(global_points, x='date', y='eco_points', title="Global Eco-Points Trend")
        st.plotly_chart(fig2)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.experimental_rerun()

else:
    st.info("Please login or register to continue.")

