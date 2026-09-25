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
COACH_NOTE_FILE = "koc_notu.txt"
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    try: os.makedirs(UPLOAD_DIR)
    except: pass

def save_entry(entry, filename):
    df = pd.read_csv(filename) if os.path.exists(filename) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(filename, index=False)

# --- TASARIM ---
st.set_page_config(page_title="Kanca Koçluk v1.3", layout="wide")

if check_password():
    st.sidebar.title("⚓ KANCA v1.3")
    menu = st.sidebar.radio("Menü", ["🚀 Öğrenci Paneli", "📦 Kanca Kasası", "🧠 Koç Paneli"])

    # --- 1. ÖĞRENCİ PANELİ ---
    if menu == "🚀 Öğrenci Paneli":
        st.title("Günü Kancala, Şüheda!")
        
        # KOÇTAN GELEN NOTU GÖSTER
        if os.path.exists(COACH_NOTE_FILE):
            with open(COACH_NOTE_FILE, "r", encoding="utf-8") as f:
                koc_notu = f.read()
            st.markdown(f"""
                <div style="background-color:#16213E; padding:20px; border-radius:15px; border-left:5px solid #FF4B2B; margin-bottom:20px;">
                    <h4 style="margin:0; color:#FF4B2B;">🎧 Koçunun Notu:</h4>
                    <p style="margin:10px 0 0 0; font-size:18px;">{koc_notu}</p>
                </div>
            """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📊 Günlük Takip", "📸 Hata Yükle"])
        with tab1:
            with st.form("gunluk_form"):
                soru = st.number_input("Kaç soru çözdün?", min_value=0, value=100)
                mod = st.select_slider("Enerjin?", ["Bunalmış", "Yorgun", "Normal", "Enerjik", "Zımba!"])
                if st.form_submit_button("VERİYİ MÜHÜRLE"):
                    save_entry({"Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "Soru": soru, "Mod": mod}, DATA_FILE)
                    st.success("Verin kaydedildi!")

        with tab2:
            st.subheader("Yapamadığın Soruyu Kasaya At")
            uploaded_file = st.file_uploader("Soru Fotoğrafı Seç", type=['png', 'jpg', 'jpeg'])
            ders = st.selectbox("Ders", ["Matematik", "Fizik", "Kimya", "Biyoloji", "Türkçe"])
            not_ekle = st.text_input("Soru hakkında notun")
            if st.button("KASAYA KİLİTLE"):
                if uploaded_file is not None:
                    fname = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    file_path = os.path.join(UPLOAD_DIR, fname)
                    with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
                    save_entry({"Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "Ders": ders, "Dosya": file_path, "Not": not_ekle, "Durum": "Çözülmedi"}, VAULT_FILE)
                    st.success("Soru Kanca Kasası'na eklendi!")

    # --- 2. KANCA KASASI ---
    elif menu == "📦 Kanca Kasası":
        st.title("📦 Kanca Kasası")
        if os.path.exists(VAULT_FILE):
            kasa_df = pd.read_csv(VAULT_FILE)
            for index, row in kasa_df.iterrows():
                durum_emoji = "✅" if row['Durum'] == "Çözüldü" else "❌"
                with st.expander(f"{durum_emoji} {row['Tarih']} - {row['Ders']}"):
                    col_img, col_txt = st.columns([1, 2])
                    if os.path.exists(str(row['Dosya'])):
                        col_img.image(str(row['Dosya']), use_container_width=True)
                    col_txt.write(f"**Not:** {row['Not']}")
                    col_txt.write(f"**Durum:** {row['Durum']}")
                    if row['Durum'] == "Çözülmedi":
                        if col_txt.button("Çözüldü İşaretle", key=f"btn_{index}"):
                            kasa_df.at[index, 'Durum'] = "Çözüldü"
                            kasa_df.to_csv(VAULT_FILE, index=False)
                            st.rerun()
        else:
            st.info("Kasa henüz boş.")

    # --- 3. KOÇ PANELİ ---
    elif menu == "🧠 Koç Paneli":
        st.title("Strateji Merkezi")
        
        # ÖĞRENCİYE NOT BIRAKMA ALANI
        st.subheader("✍️ Şüheda'ya Mesaj Gönder")
        mevcut_not = ""
        if os.path.exists(COACH_NOTE_FILE):
            with open(COACH_NOTE_FILE, "r", encoding="utf-8") as f: mevcut_not = f.read()
        
        yeni_not = st.text_area("Öğrencinin ana sayfasında görünecek not:", value=mevcut_not)
        if st.button("Notu Güncelle ve Gönder"):
            with open(COACH_NOTE_FILE, "w", encoding="utf-8") as f: f.write(yeni_not)
            st.success("Not Şüheda'nın ekranına uçtu!")

        if os.path.exists(DATA_FILE):
            data = pd.read_csv(DATA_FILE)
            st.write("### Gelişim Grafiği")
            st.line_chart(data.set_index("Tarih")["Soru"])
