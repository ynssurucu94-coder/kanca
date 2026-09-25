import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

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

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def save_entry(entry, filename):
    df = pd.read_csv(filename) if os.path.exists(filename) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(filename, index=False)

# --- TASARIM ---
st.set_page_config(page_title="Kanca Koçluk v1.2", layout="wide")

if check_password():
    st.sidebar.title("⚓ KANCA v1.2")
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
            uploaded_file = st.file_uploader("Soru Fotoğrafı Seç veya Çek", type=['png', 'jpg', 'jpeg'])
            ders = st.selectbox("Ders", ["Matematik", "Fizik", "Kimya", "Biyoloji", "Türkçe"])
            not_ekle = st.text_input("Soru hakkında notun (isteğe bağlı)")
            
            if st.button("KASAYA KİLİTLE"):
                if uploaded_file is not None:
                    # Dosyayı kaydet
                    file_path = os.path.join(UPLOAD_DIR, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}")
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Veritabanına kaydet
                    save_entry({
                        "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Ders": ders,
                        "Dosya": file_path,
                        "Not": not_ekle,
                        "Durum": "Çözülmedi"
                    }, VAULT_FILE)
                    st.success("Soru Kanca Kasası'na başarıyla eklendi!")
                else:
                    st.error("Lütfen bir fotoğraf seçin.")

    # --- 2. KANCA KASASI (ARŞİV) ---
    elif menu == "📦 Kanca Kasası (Hatalar)":
        st.title("📦 Kanca Kasası")
        if os.path.exists(VAULT_FILE):
            kasa_df = pd.read_csv(VAULT_FILE)
            for index, row in kasa_df.iterrows():
                with st.expander(f"{row['Tarih']} - {row['Ders']} ({row['Durum']})"):
                    col_img, col_txt = st.columns([1, 2])
                    if os.path.exists(row['Dosya']):
                        col_img.image(row['Dosya'], use_column_width=True)
                    col_txt.write(f"**Not:** {row['Not']}")
                    if st.button("Çözüldü Olarak İşaretle", key=index):
                        st.info("Bu özellik bir sonraki güncellemede aktif olacak!")
        else:
            st.info("Kasa henüz boş. Öğrenci panelinden ilk hatanı yükle!")

    # --- 3. KOÇ PANELİ ---
    elif menu == "🧠 Koç Paneli":
        st.title("Strateji Merkezi")
        if os.path.exists(DATA_FILE):
            data = pd.read_csv(DATA_FILE)
            st.write("### Genel Gelişim")
            st.line_chart(data.set_index("Tarih")["Soru"])
            
            if os.path.exists(VAULT_FILE):
                kasa = pd.read_csv(VAULT_FILE)
                st.write(f"### 📦 Kasa Durumu: {len(kasa)} Bekleyen Soru")
                st.write(kasa[["Tarih", "Ders", "Not"]])
        else:
            st.warning("Henüz analiz edilecek veri yok.")
