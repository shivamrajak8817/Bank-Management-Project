import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bank.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    type TEXT,
    amount INTEGER,
    date TEXT
)
""")

conn.commit()

# ---------------- FUNCTIONS ----------------
def signup(name, email, pin):
    cursor.execute("INSERT INTO users(name,email,pin) VALUES(?,?,?)", (name,email,pin))
    conn.commit()

def login(email, pin):
    cursor.execute("SELECT * FROM users WHERE email=? AND pin=?", (email,pin))
    return cursor.fetchone()

def deposit(email, amount):
    cursor.execute("UPDATE users SET balance = balance + ? WHERE email=?", (amount,email))
    cursor.execute("INSERT INTO transactions(email,type,amount,date) VALUES(?,?,?,?)",
                   (email,"Deposit",amount,str(datetime.now())))
    conn.commit()

def withdraw(email, amount):
    cursor.execute("SELECT balance FROM users WHERE email=?", (email,))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        cursor.execute("UPDATE users SET balance = balance - ? WHERE email=?", (amount,email))
        cursor.execute("INSERT INTO transactions(email,type,amount,date) VALUES(?,?,?,?)",
                       (email,"Withdraw",amount,str(datetime.now())))
        conn.commit()
        return True
    else:
        return False

def get_balance(email):
    cursor.execute("SELECT balance FROM users WHERE email=?", (email,))
    return cursor.fetchone()[0]

def get_transactions(email):
    return pd.read_sql_query(f"SELECT * FROM transactions WHERE email='{email}'", conn)

# ---------------- UI ----------------
st.set_page_config(page_title="Fancy Bank App", layout="wide")

st.title("🏦 Fancy Banking System")

menu = st.sidebar.selectbox("Menu", ["Login","Signup"])

# ---------------- SIGNUP ----------------
if menu == "Signup":
    st.subheader("Create New Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    pin = st.text_input("4 Digit PIN", type="password")

    if st.button("Signup"):
        signup(name,email,pin)
        st.success("Account Created Successfully 🎉")

# ---------------- LOGIN ----------------
elif menu == "Login":
    st.subheader("Login")

    email = st.text_input("Email")
    pin = st.text_input("PIN", type="password")

    if st.button("Login"):
        user = login(email,pin)
        if user:
            st.session_state.user = email
            st.success("Login Successful")
        else:
            st.error("Invalid Login")

# ---------------- DASHBOARD ----------------
if "user" in st.session_state:

    email = st.session_state.user
    st.sidebar.success(f"Logged in as {email}")

    dashboard_menu = st.sidebar.selectbox(
        "Dashboard",
        ["Home","Deposit","Withdraw","Transactions","Logout"]
    )

    # HOME
    if dashboard_menu == "Home":
        st.header("Dashboard")

        balance = get_balance(email)

        col1,col2 = st.columns(2)

        col1.metric("💰 Balance", f"₹ {balance}")
        col2.metric("👤 User", email)

        df = get_transactions(email)
        if not df.empty:
            st.line_chart(df["amount"])

    # DEPOSIT
    elif dashboard_menu == "Deposit":
        st.header("Deposit Money")

        amount = st.number_input("Enter Amount", min_value=1)

        if st.button("Deposit"):
            deposit(email, amount)
            st.success("Money Deposited 💰")

    # WITHDRAW
    elif dashboard_menu == "Withdraw":
        st.header("Withdraw Money")

        amount = st.number_input("Enter Amount", min_value=1)

        if st.button("Withdraw"):
            success = withdraw(email, amount)
            if success:
                st.success("Money Withdrawn 💸")
            else:
                st.error("Insufficient Balance")

    # TRANSACTIONS
    elif dashboard_menu == "Transactions":
        st.header("Transaction History")

        df = get_transactions(email)
        st.dataframe(df)

    # LOGOUT
    elif dashboard_menu == "Logout":
        del st.session_state.user
        st.warning("Logged Out")