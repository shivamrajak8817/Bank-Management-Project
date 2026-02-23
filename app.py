import streamlit as st
import json
import random
import string
from pathlib import Path
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="DIGITAL BANK MANAGEMENT SYSTEM", layout="wide")

# ---------------- ADVANCED DARK UI ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0A0F1C !important;
    color: white !important;
}
section[data-testid="stSidebar"] {
    background-color: #111827 !important;
}
h1 {
    font-size:50px;
    background: linear-gradient(90deg,#00ADB5,#22C55E);
    -webkit-background-clip: text;
    color: transparent;
}
.stButton>button {
    background: linear-gradient(90deg,#00ADB5,#22C55E);
    color:white;
    border-radius:10px;
    height:45px;
    border:none;
}
input {
    background:#1F2937 !important;
    color:white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------
DATABASE = "data.json"

if Path(DATABASE).exists():
    with open(DATABASE, "r") as f:
        data = json.load(f)
else:
    data = []

def save_data():
    with open(DATABASE, "w") as f:
        json.dump(data, f)

def generate_account():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# ---------------- LOGIN SYSTEM ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown("<h1>DIGITAL BANK MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if password == "admin123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong Password")
else:

    # ---------------- HEADER ----------------
    st.markdown("<h1>DIGITAL BANK MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)

    # ---------------- DASHBOARD ----------------
    total_balance = sum(user["balance"] for user in data) if data else 0

    col1, col2 = st.columns(2)
    col1.metric("👥 Total Users", len(data))
    col2.metric("💰 Total Balance", f"₹ {total_balance}")

    st.markdown("### 📊 Banking Analytics")

    if data:
        df = pd.DataFrame(data)
        st.bar_chart(df["balance"])

    # ---------------- MENU ----------------
    menu = st.sidebar.selectbox("Navigation", [
        "Create Account",
        "Deposit",
        "Withdraw",
        "Transaction History"
    ])

    # ---------------- CREATE ----------------
    if menu == "Create Account":
        st.subheader("Create Account")

        name = st.text_input("Name")
        pin = st.text_input("4 Digit PIN", type="password")

        if st.button("Create"):
            if len(pin) == 4:
                acc = generate_account()
                data.append({
                    "name": name,
                    "pin": pin,
                    "account": acc,
                    "balance": 0
                })
                save_data()
                st.success(f"Account Created: {acc}")
                st.balloons()
            else:
                st.error("PIN must be 4 digits")

    # ---------------- DEPOSIT ----------------
    elif menu == "Deposit":
        st.subheader("Deposit Money")
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input("Amount", min_value=1)

        if st.button("Deposit"):
            user = next((u for u in data if u["account"] == acc and u["pin"] == pin), None)
            if user:
                user["balance"] += amount
                save_data()
                st.success("Money Deposited 💸")
            else:
                st.error("User Not Found")

    # ---------------- WITHDRAW ----------------
    elif menu == "Withdraw":
        st.subheader("Withdraw Money")
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input("Amount", min_value=1)

        if st.button("Withdraw"):
            user = next((u for u in data if u["account"] == acc and u["pin"] == pin), None)
            if user and amount <= user["balance"]:
                user["balance"] -= amount
                save_data()
                st.success("Money Withdrawn 🏧")
            else:
                st.error("Invalid User or Insufficient Balance")

    # ---------------- HISTORY ----------------
    elif menu == "Transaction History":
        st.subheader("All Accounts Data")
        st.json(data)

    # ---------------- LOGOUT ----------------
    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()
