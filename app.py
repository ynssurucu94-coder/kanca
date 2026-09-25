import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- GÜVENLİK ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "kanca2024":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.text_input("Kanca Koçluk - Gizli Giriş", type="password", on_change=password_entered, key="password")
        return False
    return st.session_state["password_correct"]

# --- VERİ YÖNETİMİ ---
DATA_FILE = "kanca_veriler.csv"
VAULT_FILE = "kanca_kasa.csv"
COACH_NOTE_FILE = "koc_notu.txt"
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    try: os.makedirs(UPLOAD_DIR)
    except: pass

def save_entry(entry, filename):
    df = pd.read_csv(filename) if os.path.exists(filename) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(filename, index=False)

# --- LİG VE PUAN HESAPLAMA ---
def get_rank(points):
    if points < 500: return "⚓ Demir Atan"
    if points < 1500: return "🪝 Kancayı Takan"
    if points < 3500: return "🏹 Zıpkın"
    if points < 7000: return "🎓 Üstat"
    return "🔥 Kanca Efsanesi"

# --- TASARIM ---
st.set_page_config(page_title="Kanca Koçluk v1.4", layout="wide")

if check_password():
    st.sidebar.title("⚓ KANCA v1.4")
    menu = st.sidebar.radio("Menü", ["🚀 Öğrenci Paneli", "📦 Kanca Kasası", "🏆 Kanca Ligi", "🧠 Koç Paneli"])

    # --- 1. ÖĞRENCİ PANELİ ---
    if menu == "🚀 Öğrenci Pan
