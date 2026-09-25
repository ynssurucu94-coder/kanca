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

# --- VERİ VE DOSYA YÖNETİMİ ---
DATA_FILE = "kanca_veriler.csv"
VAULT_FILE = "kanca_kasa.csv"
UPLOAD_DIR = "uploads"

# Klasörü oluştururken hata almamak için kontrol
if not os.path.exists(UPLOAD_DIR):
    try:
        os.makedirs(UPLOAD_DIR)
    except:
        pass

def save_entry(entry, filename):
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(filename, index=False)

# --- TASARIM ---
st.set_page_config(page_title="Kanca Koçluk v1.2.1", layout="wide")

if check_password():
    st.sidebar.title("⚓ KANCA v1.2.1")
    menu = st.sidebar.radio("Menü", ["🚀 Öğrenci Paneli", "📦 Kanca Kasası (Hatalar)", "🧠 Koç Paneli"])

    # --- 1. ÖĞRENCİ PANELİ ---
    if menu == "🚀 Öğrenci Paneli":
        st.title("Günü Kancala, Şüheda!")
        tab1, tab2 = st.tabs(["📊 Günlük Takip", "📸 Hata Yükle"])
        
        with tab1:
            with st.form("gunluk_form"):
                soru = st.number_input("Kaç soru çözdün?", min_value=0, value=100)
                mod = st.select_slider("Enerjin?", ["Bunalmış", "Yorgun", "Normal", "Enerjik", "Zımba!"])
                if st.form_submit_button("VERİYİ MÜHÜRLE"):
                    save_entry({"Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "Soru": soru, "Mod": mod}, DATA_FILE)
                    st.success("Günlük verin kaydedildi!")

        with tab2:
            st.subheader("Yapamadığın Soruyu Kasaya At")
            uploaded_file = st.file_uploader("Soru Fotoğrafı Seç", type=['png', 'jpg', 'jpeg'])
            ders = st.selectbox("Ders", ["Matematik", "Fizik", "Kimya", "Biyoloji", "Türkçe"])
            not_ekle = st.text_input("Soru hakkında notun")
            
            if st.button("KASAYA KİLİTLE"):
                if uploaded_file is not None:
                    # Dosya ismini güvenli hale getir
                    fname = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    file_path = os.path.join(UPLOAD_DIR, fname)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    save_entry({
                        "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Ders": ders,
                        "Dosya": file_path,
                        "Not": not_ekle,
                        "Durum": "Çözülmedi"
                    }, VAULT_FILE)
                    st.success("Soru Kanca Kasası'na eklendi!")
                else:
                    st.error("Lütfen bir fotoğraf seçin.")

    # --- 2. KANCA KASASI (ARŞİV) ---
    elif menu == "📦 Kanca Kasası (Hatalar)":
        st.title("📦 Kanca Kasası")
        if os.path.exists(VAULT_FILE):
            kasa_df = pd.read_csv(VAULT_FILE)
            for index, row in kasa_df.iterrows():
                # Hata aldığın kısım burasıydı, düzelttik:
                with st.expander(f"{row['Tarih']} - {row['Ders']}"):
                    col_img, col_txt = st.columns([1, 2])
                    
                    # Dosya yolunu kontrol et ve resmi bas
                    path = str(row['Dosya'])
                    if os.path.exists(path):
                        col_img.image(path, use_container_width=True) # Parametre güncellendi
                    else:
                        col_img.warning("Resim bulunamadı.")
                        
                    col_txt.write(f"**Not:** {row['Not']}")
                    col_txt.write(f"**Durum:** {row['Durum']}")
        else:
            st.info("Kasa henüz boş.")

    # --- 3. KOÇ PANELİ ---
    elif menu == "🧠 Koç Paneli":
        st.title("Strateji Merkezi")
        if os.path.exists(DATA_FILE):
            data = pd.read_csv(DATA_FILE)
            st.write("### Genel Gelişim")
            st.line_chart(data.set_index("Tarih")["Soru"])
        else:
            st.warning("Henüz analiz edilecek veri yok.")
