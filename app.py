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

# --- VERİ YÖNETİMİ (HAFIZA SİSTEMİ) ---
DATA_FILE = "kanca_veriler.csv"

def save_data(new_entry):
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["Tarih", "Ogrenci", "Soru", "Mod"])
    
    # Yeni veriyi ekle (df.append yerine pd.concat kullanıyoruz yeni sürüm için)
    new_df = pd.DataFrame([new_entry])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Tarih", "Ogrenci", "Soru", "Mod"])

# --- TASARIM ---
st.set_page_config(page_title="Kanca Koçluk v1.1", layout="wide")

if check_password():
    st.sidebar.title("⚓ KANCA v1.1")
    menu = st.sidebar.radio("Menü", ["🚀 Öğrenci Paneli", "🧠 Koç Paneli", "🛡️ Veli Portalı"])
    
    all_data = load_data()

    if menu == "🚀 Öğrenci Paneli":
        st.title("Hoş geldin Şüheda!")
        st.info("Bugünkü kancanı atmaya hazır mısın?")
        
        with st.form("veri_formu"):
            soru = st.number_input("Bugün kaç soru çözdün?", min_value=0, value=100)
            mod = st.select_slider("Enerjin nasıl?", ["Bunalmış", "Yorgun", "Normal", "Enerjik", "Zımba!"])
            submit = st.form_submit_button("HEDEFİ KANCALA")
            
            if submit:
                entry = {
                    "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Ogrenci": "Şüheda",
                    "Soru": soru,
                    "Mod": mod
                }
                save_data(entry)
                st.balloons()
                st.success("Verin sisteme mühürlendi! Artık kalıcı.")

    elif menu == "🧠 Koç Paneli":
        st.title("Strateji Merkezi")
        if not all_data.empty:
            st.write("### Son Aktivite Geçmişi")
            st.dataframe(all_data.tail(10)) # Son 10 kaydı göster
            
            st.write("### Gelişim Grafiği")
            st.line_chart(all_data.set_index("Tarih")["Soru"])
            
            # Basit AI Analizi
            son_mod = all_data.iloc[-1]["Mod"]
            if son_mod in ["Bunalmış", "Yorgun"]:
                st.warning("⚠️ AI NOTU: Öğrenci yorgun görünüyor. Programı hafifletmeyi düşünün.")
        else:
            st.info("Henüz kaydedilmiş veri yok. Öğrenci panelinden ilk girişi yapın.")

    elif menu == "🛡️ Veli Portalı":
        st.title("Veli Paneli")
        if not all_data.empty:
            toplam_soru = all_data["Soru"].sum()
            st.metric("Toplam Çözülen Soru", toplam_soru)
            st.write("Süreç koç kontrolünde ilerliyor.")
        
