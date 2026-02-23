import streamlit as st
import json
import random
import string
from pathlib import Path  

st.set_page_config(page_title="DIGITAL BANK MANAGEMENT SYSTEM", layout="wide")

st.markdown("""
<style>
/* FORCE WHITE BACKGROUND */
html, body, [class*="css"]  {
    background-color: #0A0F1C !important;
    color: white !important;
}
/* Sidebar Dark */
section[data-testid="stSidebar"] {
    background-color: #111827 !important;
}
/* Headings */
h1 { color: #00D9F5 !important; font-weight: 700; }
h2, h3 { color: #38BDF8 !important; }
/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#00ADB5,#22C55E);
    color: white;
    border-radius: 10px;
    height: 45px;
    border: none;
}
/* Inputs */
input, textarea {
    background-color: #1F2937 !important;
    color: white !important;
    border: 1px solid #374151 !important;
}
</style>
""", unsafe_allow_html=True)
